# SublimeJump

SublimeJump is a [Sublime Text 2](http://www.sublimetext.com/2) plugin that allows you to move the cursor to any character in your current view.

It's heavily inspired by [EasyMotion](http://www.vim.org/scripts/script.php?script_id=3526) (vim), and [AceJump](http://www.emacswiki.org/emacs/AceJump) (emacs).

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

if you wanted to go to the beginning of the `realpart` variable on line 3, instead of hitting the up arrow twice and scrolling over to the r (or grabbing your mouse), you could press `cmd-;` followed by `r`.  That will transform your file into this (notice that each instance of `r` has been turned into one of `a-zA-Z0-9`):

![SublimeJump Middle](https://raw.github.com/tednaleid/SublimeJump/add_images/images/sublimejump_middle.png)

Press `e` and hit enter and your cursor will jump right there:

![SublimeJump Middle](https://raw.github.com/tednaleid/SublimeJump/add_images/images/sublimejump_end.png)

If your target character occurs frequently within the view, it will only decorate the first 62 of them (`a-z` + `A-Z` + `0-9`).  If the one you want to go to isn't highlighted, just hit enter and it will highlight the next group of matches.  Keep hitting enter and it will continue to cycle through them in groups of 62.

It is currently untested on Windows and Linux.  It is also very alpha, so save early and often if you decide to use it.
