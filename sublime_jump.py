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

    def run(self, character=None):
        sublime.status_message("Sublime Jump to " + character)

        self.jump_target_scope = sublime.load_settings("SublimeJump.sublime-settings").get('jump_target_scope', 'string')
        self.active_view = self.window.active_view()

        visible_region = self.active_view.visible_region()

        self.found_char_regions = self.find_all_in_region(visible_region, character)

        self.jump_character = character

        if len(self.found_char_regions) > 0:
            self.prompt_for_jump()
        else:
            sublime.status_message("Sublime Jump: unable to find any instances of " + character + " in visible region")

    def find_all_in_region(self, region, character):
        '''
            Finds all occurrences of text in given region and returns an array of matching regions
        '''
        search_text = self.active_view.substr(region)
        matching_regions = []
        region_begin = region.begin()
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
        if (self.edit is None):
            self.edit = self.active_view.begin_edit()

        for char_region, placeholder_char in (zip(self.found_char_regions, PLACEHOLDER_CHARS)):
            self.active_view.replace(self.edit, char_region, placeholder_char)

        self.active_view.add_regions("jump_match_regions", self.found_char_regions, self.jump_target_scope, "dot")

    def restore_found_chars(self):
        # alternatively it would be good to just end the edit and then undo it so that we havent dirtied the save state of the file
        for char_region in self.found_char_regions:
            self.active_view.replace(self.edit, char_region, self.jump_character)

        self.active_view.erase_regions("jump_match_regions")
        self.active_view.end_edit(self.edit)
        self.edit = None
