# keyfig (WIP)

`keyfig` is a format for writing your key bindings for your window manager.  `keyfig` is also a command line utility to generate configuration files based on your key bindings.  This project allows you to store keybinds in one place, and generate the right configuration needed for any window manager.  This is helpful for

* those who use multiple window managers, so they can avoid maintaining multiple configurations
* those who want to share keybindings with someone else of a different window manager
* those who want to experiment with or change window managers, to help ease the changing process

## yml spec

The user defines all their keybinds in a single `yml` file.  The format will provide some liberties to avoid duplication, such as providing multiple keybinds for the same action, or some basic templating to avoid duplicating for each workspace (shift+1, shift+2, etc.).

In addition theres some shorthand for particular outputs.  Not every keybind is just running a command in bash.  In these instances, there will be a specific shorthand per wm.  For instance, moving focus in herbstluft looks like this:
```
hc keybind $Mod-k focus up 
```
The user could just say that an "herbstluftwm" action is "focus left".  Compare this to an xmonad configuration where it is instead `windows W.focusUp`
```
, ((modMask, xK_k), windows W.focusUp)
```
The keyfig format allows you to specify per WM how to define both of these under one keybind in one location.
```
- name: FocusUp
  keys:
  - modifiers: [ "mod" ]
    key: "k"
  action:
    herbstluftwm: "focus up"
    xmonad: "windows W.focusUp"
```
There should also be a "terminal command" option, which is common and can be handled across multiple WM without needing to specify.  For instance, look at a command that spawns a terminal.
```
- name: Start Terminal
  keys:
  - modifiers: [ "mod" ]
    key: "enter"
  action:
    command: "alacritty"
```
Which would create
```
hc keybind $Mod-Return spawn alacritty
```
for herbstluftwm and
```
, ((modMask, xK_enter), spawn alacritty)
```
for xmonad.  Okay, a better example might include i3 or sxhkd.

## `keyfig` utility

This utility will take an input yml file and convert it to a variety of formats.  These formats align with those expected in your window manager.  You should be able to make standalone output too, where things like variables declarations (for bash-based configs) or imports (those needed in a standalone haskell keybinds.hs).

In addition, the `keyfig` could also read existing configurations and do a best effort to extract existing keybinds from an existing configuration.  Even if not complete, it would be a good starting point for people wanting to integrate into keyfig.

There can be other utility functions, like verifying that a yml file is formatted correctly or syntactically correct.  Maybe it also checks to see how many keybinds are defined (which is different based on wm) and list specific wms noted in the config.

It can also check to make sure that there aren't duplicate/overlapping key bindings (well, inform you, maybe its intentional).

Because this is a standard format, other tools could be built on top.  For instance, it would be cool to have a program visualize your key configuration on a keyboard in your browser, and allow you manage which layers have things assigned already, etc.  If that was the case, then this tool would be beneficially for those that only use a single WM.

It would also be nice to change the mod key when you configure it, since I know thats a point of contention between configurations.  It'd be nice to try someone's configuration and be able to modify it easily, especially for configurations like sxhkd which don't have a "mod" key, or a way to generically assign one.  You have to specify alt/super at every instance.  Of course, if it were ambiguous what the mod key was, then it would fail.  Perhaps the better option is to have it swap super/alt across configurations?  Or some other command.  That might be useful, in case you want to take someone else's configuration and make some modifications because you use alt instead of super, or ijkl vs hjkl vs jkl;.
