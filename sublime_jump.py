import sublime
import sublime_plugin
import re
import string
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
        self.jump_target_index = 0
        self.placeholder_chars = placeholder_chars

    def __iter__(self):
        return self

    def has_next(self):
        return self.jump_target_index < len(self.all_jump_targets)

    def next(self):
        if not self.has_next():
            raise StopIteration

        jump_group = dict()

        for placeholder_char in self.placeholder_chars:
            if self.has_next():
                jump_group[placeholder_char] = self.all_jump_targets[self.jump_target_index]
                self.jump_target_index += 1
            else:
                break

        return jump_group

    def reset(self):
        self.jump_target_index = 0

    def find_all_jump_targets_in_visible_region(self, character):
        visible_region_begin = self.visible_region_begin()
        visible_text = self.visible_text()
        matching_regions = []
        escaped_character = self.escape_character(character)

        for char_at in (match.start() for match in re.finditer(escaped_character, visible_text)):
            char_point = char_at + visible_region_begin
            matching_regions.append(sublime.Region(char_point, char_point + 1))

        return matching_regions

    def visible_region_begin(self):
        return self.view.visible_region().begin()

    def visible_text(self):
        # TODO enhance to be aware of collapsed text blocks
        visible_region = self.view.visible_region()
        return self.view.substr(visible_region)

    def escape_character(self, character):
        if (REGEX_ESCAPE_CHARS.find(character) >= 0):
            return '\\' + character
        else:
            return character


class SublimeJumpCommand(sublime_plugin.WindowCommand):
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
        placeholder_chars = settings.get('placeholder_chars', 'string')
        self.active_view = self.window.active_view()
        self.select_text = select_text

        self.jump_group_iterator = JumpGroupIterator(self.active_view, character, placeholder_chars)

        if self.jump_group_iterator.has_next():
            self.prompt_for_next_jump_group()
        else:
            sublime.status_message("Sublime Jump: unable to find any instances of " + character + " in visible region")

    def prompt_for_next_jump_group(self):
        if not self.jump_group_iterator.has_next():
            self.jump_group_iterator.reset()

        self.current_jump_group = self.jump_group_iterator.next()
        self.prompt_for_jump()

    def prompt_for_jump(self):
        self.activate_current_jump_group()
        try:
            self.window.show_input_panel("Pick jump target", "", self.selected_jump_target, None, self.deactivate_current_jump_group)
        except:
            self.deactivate_current_jump_group()

    def selected_jump_target(self, selection):
        if len(selection) == 0:
            self.prompt_for_next_jump_group()
        else:
            self.deactivate_current_jump_group()
            self.jump_to(selection)

    def jump_to(self, selection):
        winning_selection = self.winning_selection_from(selection)

        if winning_selection is not None:
            view_sel = self.active_view.sel()
            view_sel.clear()
            view_sel.add(winning_selection)
            self.active_view.show(winning_selection)

    def winning_selection_from(self, selection):
        winning_region = self.current_jump_group[selection]

        if winning_region is not None:
            winning_point = winning_region.begin()
            if self.select_text:
                for selection in self.active_view.sel():
                    pprint(selection)
                    return sublime.Region(winning_point, selection.begin())

            else:
                return winning_point

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
