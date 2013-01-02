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

### Jump to any visible character

    cmd-;   <character>   // OSX
    ctrl-;  <character>   // Linux/Windows
    
it will label all instances of that character with a unique value in `a-zA-Z0-9`, type it and it will jump you to it.

#### Example

The cursor is at the end of the file and we want to jump to the beginning of the `realpart` variable on line 3

![SublimeJump Begin](https://raw.github.com/tednaleid/SublimeJump/add_images/images/sublimejump_begin.png)

Instead of hitting the up arrow twice and scrolling over to the r (or grabbing your mouse), you could press `cmd-;` followed by `r`.  That will transform your file into this (notice that each instance of `r` has been turned into one of `a-zA-Z0-9`):

![SublimeJump Middle](https://raw.github.com/tednaleid/SublimeJump/add_images/images/sublimejump_middle.png)

Press `e` and hit enter and your cursor will jump right there:

![SublimeJump Middle](https://raw.github.com/tednaleid/SublimeJump/add_images/images/sublimejump_end.png)

If your target character occurs more than 62 times in the visible area, it will decorate them in batches.  Just hit `enter` and it will highlight the next group of matches.  Keep hitting enter and it will continue to cycle through them in groups of 62.

### Select all text between cursor and any visible character

    cmd-shift-;  <character>  // OSX
    ctrl-shift-; <character>  // Linux/Windows

it will label all instances of that character with a unique value in `a-zA-Z0-9`, type it and it will select all text between your current cursor position and the chosen jump target.

So in the same example as above, if we had hit `cmd-shift-;` followed by `r` and picked the `e` target that occurs at the start of the `imagpart` variable on line 3, we would end up with this:

![SublimeJump Select](https://raw.github.com/tednaleid/SublimeJump/add_images/images/sublimejump_select.png)
