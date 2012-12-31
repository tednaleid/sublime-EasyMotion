import sublime
import sublime_plugin
import re
import string
from pprint import pprint

PLACEHOLDER_CHARS = (string.lowercase + string.uppercase + string.digits)
REGEX_ESCAPE_CHARS = '\\+*()[]{}^$?|:].,'


class SublimeJumpCommand(sublime_plugin.WindowCommand):
    '''
       We want a WindowCommand and not a TextComand so that we can control the edit/undo item so the user
       can't "undo" back to a state where we've transformed their selection to a-zA-Z0-9
    '''

    jump_character = None
    active_view = None
    edit = None
    found_char_regions = None
    jump_target_scope = None
    current_jump_group = 0

    def run(self, character=None):
        sublime.status_message("Sublime Jump to " + character)

        self.jump_target_scope = sublime.load_settings("SublimeJump.sublime-settings").get('jump_target_scope', 'string')
        self.active_view = self.window.active_view()
        self.jump_character = character

        self.found_char_regions = self.find_partitioned_jump_targets_in_visible_region(character)

        if len(self.found_char_regions) > 0:
            self.prompt_for_jump()
        else:
            sublime.status_message("Sublime Jump: unable to find any instances of " + character + " in visible region")

    def find_partitioned_jump_targets_in_visible_region(self, character):
        # TODO partition the visible region into a list of dictionary objects that contain jump character -> region
        return self.find_all_jump_targets_in_visible_region(character)

    def find_all_jump_targets_in_visible_region(self, character):
        visible_region = self.active_view.visible_region()
        search_text = self.active_view.substr(visible_region)
        matching_regions = []
        region_begin = visible_region.begin()
        escaped_character = self.escape_character(character)

        for char_at in (match.start() for match in re.finditer(escaped_character, search_text)):
            char_point = char_at + region_begin
            matching_regions.append(sublime.Region(char_point, char_point + 1))

        return matching_regions

    def escape_character(self, character):
        if (REGEX_ESCAPE_CHARS.find(character) >= 0):
            return '\\' + character
        else:
            return character

    def prompt_for_jump(self):
        self.transform_found_chars()
        try:
            self.window.show_input_panel("Pick target", "", self.selected_jump_target, None, self.restore_found_chars)
        except:
            self.restore_found_chars()

    def selected_jump_target(self, selection):
        self.restore_found_chars()
        self.jump_to(selection)

    def jump_to(self, selection):
        winning_index = PLACEHOLDER_CHARS.find(selection)

        if (winning_index >= 0):
            winning_region = self.found_char_regions[winning_index]
            winning_point = winning_region.begin()

            view_sel = self.active_view.sel()
            view_sel.clear()
            view_sel.add(winning_point)
            self.active_view.show(winning_point)

    def transform_found_chars(self):
        '''
            Start up an edit object if we don't have one already, then mark all of the jump targets
        '''
        if (self.edit is None):
            self.edit = self.active_view.begin_edit()

        for char_region, placeholder_char in (zip(self.found_char_regions, PLACEHOLDER_CHARS)):
            self.active_view.replace(self.edit, char_region, placeholder_char)

        self.active_view.add_regions("jump_match_regions", self.found_char_regions, self.jump_target_scope, "dot")

    def restore_found_chars(self):
        '''
            Close out the edit that we've been messing with and then undo it right away to return the buffer to
            the pristine state that we found it in.  Other methods ended up leaving the window in a dirty save state
            and this seems to be the cleanest way to get back to the original state
        '''
        self.active_view.erase_regions("jump_match_regions")

        if (self.edit is not None):
            self.active_view.end_edit(self.edit)
            self.edit = None
            self.window.run_command("undo")
