

change matching characters to set of a-z0-9 characters, store in map of char -> region (extending out from cursor?), also store original character (if doing mixed case)

get a character input from the user
    maybe use show_input_panel, but use the on_change method to accept the first character typed
    and to make the panel go away (or re-appear if enter is hit after expanding the selection)

if next keypress is enter, move matching character set out

else if a-z0-9 move cursor to associated character

make sure that undo level is closed in finally so that undoing doesn't do anything but move the cursor




# ideas for gathering second input
- spin off thread, which spins off window command to get user and does on change
- spin off thread, which changes mode and listens for "character" then closes stuff in same edit
- no new thread, just make a window command that then spins off a text command, probably hits undo problem
- try to overload shortcut with f6, <character>, <selection> but that could fail if the user needs to do multi selection
- create listener that listens for on_modified message (issues here with pasting, etc probably not a good solution)
   https://github.com/cbumgard/SublimeListenr
- forward search takes input and continues to move cursor, could be mode thing though
    http://www.sublimetext.com/forum/viewtopic.php?f=6&t=10033
    http://www.sublimetext.com/forum/viewtopic.php?f=6&t=10103