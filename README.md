# Sublime EasyMotion

EasyMotion is a [Sublime Text 2](http://www.sublimetext.com/2) plugin that allows you to move the cursor to any character in your current view.

It's heavily inspired by [Vim's EasyMotion](http://www.vim.org/scripts/script.php?script_id=3526), and [Emacs' AceJump](http://www.emacswiki.org/emacs/AceJump) plugins.

After pressing the EasyMotion shortcut (default `cmd-;`/`ctrl-;`), you then press the character that you'd like to jump to.  EasyMotion will then replace all currently visible instances of that character with one of `a-zA-Z0-9`.  Press the key for the one you want and your cursor will be moved right to it. 

## Installation

### Install via PackageControl
If you have the [PackageControl](http://wbond.net/sublime_packages/package_control) plugin installed, you can use that to install `EasyMotion`.

Just type `cmd-shift-p` (`ctrl-shift-p` on win/linux) to bring up the command pallate then type `install` and pick `Package Control: Install Package` from the dropdown.

Then type `EasyMotion` and choose the EasyMotion plugin from the dropdown.  Hit `enter` and it will install.

### Manual Installation

Manual installation should be as easy as cloning this git repository into your Sublime `Packages` directory.  On OSX:

    cd ~/Application\ Support/Sublime\ Text\ 2/Packages
    git clone git://github.com/tednaleid/sublime-EasyMotion.git

## Usage

### Jump to any visible character

    cmd-;   <character>   // OSX
    ctrl-;  <character>   // Linux/Windows
    
it will label all instances of that character with a unique value in `a-zA-Z0-9`, type the label you want and it will jump you to it.

#### Example

The cursor is at the end of the file and we want to jump to the beginning of the `realpart` variable on line 3

![EasyMotion Begin](https://raw.github.com/tednaleid/sublime-EasyMotion/add_images/images/sublimejump_begin.png)

Instead of hitting the up arrow twice and scrolling over to the r (or grabbing your mouse), you could press `cmd-;` followed by `r`.  That will transform your file into this (notice that each instance of `r` has been turned into one of `a-zA-Z0-9`):

![EasyMotion Middle](https://raw.github.com/tednaleid/sublime-EasyMotion/add_images/images/sublimejump_middle.png)

Press `e` and your cursor will jump right there:

![EasyMotion Middle](https://raw.github.com/tednaleid/sublime-EasyMotion/add_images/images/sublimejump_end.png)

If your target character occurs more than 62 times in the visible area, it will decorate them in batches.  

So if we search this for the letter `l` using `cmd-;`+`l`

![Many Matches Start](https://raw.github.com/tednaleid/sublime-EasyMotion/add_images/images/many_matches_start.png)

The first batch of 62 targets will look like this:

![Many Matches First](https://raw.github.com/tednaleid/sublime-EasyMotion/add_images/images/many_matches_first.png)

**Just hit `enter` and it will highlight the next group of matches.**  

![Many Matches Second](https://raw.github.com/tednaleid/sublime-EasyMotion/add_images/images/many_matches_second.png)

Keep hitting `enter` and it will continue to cycle through them in groups of 62.

### Select all text between cursor and any visible character

    cmd-shift-;  <character>  // OSX
    ctrl-shift-; <character>  // Linux/Windows

it will label all instances of that character with a unique value in `a-zA-Z0-9`, type it and it will select all text between your current cursor position and the chosen jump target.

#### Example

So in the same situation as above, if we had hit `cmd-shift-;` followed by `r` and picked the `e` target that occurs at the start of the `imagpart` variable on line 3, we would end up with this:

![EasyMotion Select](https://raw.github.com/tednaleid/sublime-EasyMotion/add_images/images/sublimejump_select.png)


## User Modifiable Preferences

### Remapping the Sublime EasyMotion keyboard shortcut

You can remap your keys to be something other than the defaults by entering an override value into your "User - KeyBindings" (under Sublime Text 2 -> Preferences on OSX), just make sure to copy the existing key bindings exactly and change only the first item in the `keys` stanza, otherwise it won't work.  So if you wanted the jump command to be `ctrl-,`, you'd use:


    [
        { 
            "keys": ["ctrl+,", "<character>"], 
            "command": "easy_motion",
            "args": {"select_text": false} 
        },
        { 
            "keys": ["ctrl+shift+,", "<character>"], 
            "command": "easy_motion",
            "args": {"select_text": true} 
        }
    ]


### Overriding the placeholder characters used for jumping

Add this to your "User Settings" file (found at "Sublime Text 2 -> Preferences -> Settings - User" on OSX) and change the string to contain whatever characters you'd like to use:

    // define the characters that we can jump to, in the order that they'll appear, they should be unique
    "placeholder_chars" : "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
example using only QWERTY home-row replacements:

    "placeholder_chars" : "jkl;asdfHGJKL:ASDFHG"

### Override the highlight color for jump targets
    
If the highlight color used for jump targets isn't bold enough if your color scheme, you can override it by changing this "User Setting":

    // defines syntax highlighting scope that will be used to highlight matched jump targets
    // other examples include: keyword, string, number
    "jump_target_scope" : "entity.name.class"

