# SublimeJump

SublimeJump is a (Sublime Text 2)[http://www.sublimetext.com/2] plugin that allows you to move the cursor to any character in your current view.

It's heavily inspired by (EasyMotion)[http://www.vim.org/scripts/script.php?script_id=3526] (vim), and (AceJump)[http://www.emacswiki.org/emacs/AceJump] (emacs).

After pressing the SublimeJump shortcut, you then press the character that you'd like to jump to.  SublimeJump will then replace all currently visible instances of that character with one of `a-zA-Z0-9`.  Press the key for the one you want and your cursor will be moved right to it. 

## Installation

After SublimeJump is officially released, it will be put in Package Control, but it's not ready for primetime yet so installation is currently manual.

Manual installation should be as easy as cloning this git repository into your Sublime `Packages` directory.  On OSX:

    cd ~/Application\ Support/Sublime\ Text\ 2/Packages
    git clone git://github.com/tednaleid/SublimeJump.git

## Usage

To use the plugin, press the SublimeJump shortcut followed by the case-sensitive character that you'd like to jump to.  By default, the shortcut is `cmd-;` on OSX and `ctrl-;` on Linux/Windows.

So if you were editing this class, and your cursor is at the end of the file

![SublimeJump Begin](https://raw.github.com/tednaleid/SublimeJump/add_images/images/sublimejump_begin.png)

if you wanted to go to the `r` in the `realpart` in the method signature, instead of hitting the up arrow twice and scrolling over to the r (or grabbing your mouse), you could press `cmd-;` followed by `r`.  That will transform your file into this:

![SublimeJump Middle](https://raw.github.com/tednaleid/SublimeJump/add_images/images/sublimejump_middle.png)

with each instance of `r` turned into one of `a-zA-Z0-9`.  It then prompts you for the one you want to go to, just press `a` and hit enter and your cursor will be at the beginning of `realpart` in the signature (and all characters will revert to their previous value).

![SublimeJump Middle](https://raw.github.com/tednaleid/SublimeJump/add_images/images/sublimejump_end.png)

It is currently untested on Windows and Linux.  It is also very alpha, so save early and often if you decide to use it.

## TODO Features/Bugs

- move on_change as you type in the window
- if there are more than 62 matches for the case sensitive character on the screen, allow expanded selection with enter (and make selection expand out from current cursor position)
- possibly change coloration while in jump mode to highlight matched characters and de-emphasize unmatched ones
- any other non-kludgy input method that allows a single character to be typed without hitting enter?
- make "." character work correctly
- get working with selection (respect visual vintage mode? if shift pressed when using keystroke make it a selection?)
- if there's only one on the screen jump to it
