import sublime
import sublime_plugin
import re
import string
from itertools import izip_longest 
from pprint import pprint

REGEX_ESCAPE_CHARS = '\\+*()[]{}^$?|:].,'


class JumpGroupIterator:
    '''
       given a list of region jump targets matching the given character, can emit a series of
       JumpGroup dictionaries
    '''
    def __init__(self, view, character, placeholder_chars):
        self.view = view
        self.all_jump_targets = self.find_all_jump_targets_in_visible_region(character)
        self.interleaved_jump_targets = self.interleave_jump_targets_from_cursor()
        self.jump_target_index = 0
        self.placeholder_chars = placeholder_chars

    def __iter__(self):
        return self

    def interleave_jump_targets_from_cursor(self):
        sel = self.view.sel()[0]  # multi select not supported, doesn't really make sense
        sel_begin = sel.begin()
        sel_end = sel.end()
        before = []
        after = []

        # split them into two lists radiating out from the cursor position
        for target in self.all_jump_targets:
            if target.begin() < sel_begin:
                # add to beginning of list so closest targets to cursor are first
                before.insert(0, target)
            elif target.begin() > sel_end:
                after.append(target)

        # now interleave the two lists together into one list
        return [target for targets in izip_longest(before, after) for target in targets if target is not None]

    def has_next(self):
        return self.jump_target_index < len(self.interleaved_jump_targets)

    def next(self):
        if not self.has_next():
            raise StopIteration

        jump_group = dict()

        for placeholder_char in self.placeholder_chars:
            if self.has_next():
                jump_group[placeholder_char] = self.interleaved_jump_targets[self.jump_target_index]
                self.jump_target_index += 1
            else:
                break

        return jump_group

    def reset(self):
        self.jump_target_index = 0

    def find_all_jump_targets_in_visible_region(self, character):
        visible_region_begin = self.visible_region_begin()
        visible_text = self.visible_text()
        folded_regions = self.get_folded_regions(self.view)
        matching_regions = []
        escaped_character = self.escape_character(character)

        for char_at in (match.start() for match in re.finditer(escaped_character, visible_text)):
            char_point = char_at + visible_region_begin
            char_region = sublime.Region(char_point, char_point + 1)
            if not self.region_list_contains_region(folded_regions, char_region):
                matching_regions.append(char_region)

        return matching_regions

    def region_list_contains_region(self, region_list, region):

        for element_region in region_list:
            if element_region.contains(region):
                return True
        return False

    def visible_region_begin(self):
        return self.view.visible_region().begin()

    def visible_text(self):
        visible_region = self.view.visible_region()
        return self.view.substr(visible_region)

    def escape_character(self, character):
        if (REGEX_ESCAPE_CHARS.find(character) >= 0):
            return '\\' + character
        else:
            return character

    def get_folded_regions(self, view):
        '''
        No way in the API to get the folded regions without unfolding them first
        seems to be quick enough that you can't actually see them fold/unfold
        '''
        folded_regions = view.unfold(view.visible_region())
        view.fold(folded_regions)
        return folded_regions


class EasyMotionCommand(sublime_plugin.WindowCommand):
    '''
       We want a WindowCommand and not a TextComand so that we can control the edit/undo item so the user
       can't "undo" back to a state where we've transformed their selection to a-zA-Z0-9
    '''

    active_view = None
    edit = None
    jump_target_scope = None
    jump_group_iterator = None
    current_jump_group = None
    select_text = False

    def run(self, character=None, select_text=False):
        sublime.status_message("SublimeJump to " + character)

        settings = sublime.load_settings("Preferences.sublime-settings")

        self.jump_target_scope = settings.get('jump_target_scope', 'string')
        placeholder_chars = settings.get('placeholder_chars', 'abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        self.active_view = self.window.active_view()
        self.select_text = select_text

        self.jump_group_iterator = JumpGroupIterator(self.active_view, character, placeholder_chars)

        if self.jump_group_iterator.has_next():
            self.prompt_for_next_jump_group()
        else:
            sublime.status_message("EasyMotion: unable to find any instances of " + character + " in visible region")

    def prompt_for_next_jump_group(self):
        if not self.jump_group_iterator.has_next():
            self.jump_group_iterator.reset()

        self.current_jump_group = self.jump_group_iterator.next()
        self.prompt_for_jump()

    def prompt_for_jump(self):
        self.activate_current_jump_group()
        try:
            self.window.show_input_panel("Pick jump target", "", self.enter_pressed, self.picked_target, self.finish_easy_motion)
        except:
            self.deactivate_current_jump_group()

    def enter_pressed(self, selection):
        # shouldn't get here unless the user hit enter, other selections should go through on_change branch
        self.prompt_for_next_jump_group()

    def picked_target(self, selection):
        if len(selection) > 0:
            # this will get used when hide_panel calls through to jump_to_winning_selection
            # can't call directly because of race condition
            self.winning_selection = self.winning_selection_from(selection)
            self.window.run_command("hide_panel")

    def winning_selection_from(self, selection):
        winning_region = None
        if selection in self.current_jump_group:
            winning_region = self.current_jump_group[selection]

        if winning_region is not None:
            if self.select_text:
                for current_selection in self.active_view.sel():
                    if winning_region.begin() < current_selection.begin():
                        return sublime.Region(current_selection.end(), winning_region.begin())
                    else:
                        return sublime.Region(current_selection.begin(), winning_region.end())
            else:
                return sublime.Region(winning_region.begin(), winning_region.begin())

    def activate_current_jump_group(self):
        '''
            Start up an edit object if we don't have one already, then create all of the jump targets
        '''
        if (self.edit is not None):
            # normally would call deactivate_current_jump_group here, but apparent ST2 bug prevents it from calling undo correctly
            # instead just decorate the new character and keep the same edit object so all changes get undone properly
            self.active_view.erase_regions("jump_match_regions")
        else:
            self.edit = self.active_view.begin_edit()

        for placeholder_char in self.current_jump_group.keys():
            self.active_view.replace(self.edit, self.current_jump_group[placeholder_char], placeholder_char)

        self.active_view.add_regions("jump_match_regions", self.current_jump_group.values(), self.jump_target_scope, "dot")

    def finish_easy_motion(self):
        '''
        We need to clean up after ourselves by restoring the view to it's original state, if the user did
        press a jump target that we've got saved, jump to it as the last action
        '''
        self.deactivate_current_jump_group()
        self.jump_to_winning_selection()

    def deactivate_current_jump_group(self):
        '''
            Close out the edit that we've been messing with and then undo it right away to return the buffer to
            the pristine state that we found it in.  Other methods ended up leaving the window in a dirty save state
            and this seems to be the cleanest way to get back to the original state
        '''
        if (self.edit is not None):
            self.active_view.end_edit(self.edit)
            self.window.run_command("undo")
            self.edit = None

        self.active_view.erase_regions("jump_match_regions")

    def jump_to_winning_selection(self):
        if self.winning_selection is not None:
            self.active_view.run_command("jump_to_winning_selection", {"begin": self.winning_selection.begin(), "end": self.winning_selection.end()})


class JumpToWinningSelection(sublime_plugin.TextCommand):
    def run(self, edit, begin, end):
        winning_region = sublime.Region(long(begin), long(end))
        sel = self.view.sel()
        sel.clear()
        sel.add(winning_region)
