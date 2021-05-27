#Qtile config file

from typing import List  # noqa: F401

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import subprocess
import json

subprocess.Popen(["picom"])
subprocess.Popen(["nvidia-settings","--load-config-only"])

SCREEN_RIGHT_INDEX =1
SCREEN_LEFT_INDEX = 2
SCREEN_MID_INDEX = 0

SCREEN_LEFTOF = {
        SCREEN_RIGHT_INDEX:SCREEN_MID_INDEX,
        SCREEN_MID_INDEX:SCREEN_LEFT_INDEX,
        SCREEN_LEFT_INDEX:SCREEN_LEFT_INDEX
        }
SCREEN_RIGHTOF = {
        SCREEN_LEFT_INDEX:SCREEN_MID_INDEX,
        SCREEN_MID_INDEX:SCREEN_RIGHT_INDEX,
        SCREEN_RIGHT_INDEX:SCREEN_RIGHT_INDEX
        }
SCREEN_NAME = {
        SCREEN_LEFT_INDEX:"SCREEN LEFT",
        SCREEN_MID_INDEX:"SCREEN MIDDLE",
        SCREEN_RIGHT_INDEX:"SCREEN RIGHT"
        }

mod = "mod4"
terminal = "kitty"

def log(*args):
    with open("/home/arizona/Downloads/qtile.log","a") as myFile:
        print(*args, file=myFile)

def focusLeft(qtile):
    currentGroup = qtile.current_screen.group
    # currentLayout = currentGroup.layout
    currentLayout = qtile.current_layout
    screenIndex = qtile.current_screen.index
    columnIndex = currentLayout.current
    prevWin =  currentLayout.focus_previous(qtile.current_window)
    if prevWin is not None:
        currentGroup.focus(prevWin)
        return
    else :
        targetIndex = SCREEN_LEFTOF[screenIndex]
        qtile.focus_screen(targetIndex)
        leftGroup = qtile.screens[targetIndex].group
        leftLayout = leftGroup.layout
        leftGroup.focus(leftLayout.focus_last())
        return

def focusRight(qtile):
    currentGroup = qtile.current_screen.group
    # currentLayout = currentGroup.layout
    currentLayout = qtile.current_layout
    screenIndex = qtile.current_screen.index
    columnIndex = currentLayout.current
    nextWin =  currentLayout.focus_next(qtile.current_window)
    if nextWin is not None:
        currentGroup.focus(nextWin)
        return
    else :
        targetIndex = SCREEN_RIGHTOF[screenIndex]
        qtile.focus_screen(targetIndex)
        rightGroup = qtile.screens[targetIndex].group
        rightLayout = rightGroup.layout
        targetClient = rightLayout.focus_first()
        rightGroup.focus(targetClient)
        return
    
def moveLeft(qtile):
    currentGroup = qtile.current_screen.group
    currentLayout = qtile.current_layout
    currentWindow = qtile.current_window
    screenIndex = qtile.current_screen.index
    columnIndex = currentLayout.current
    if currentWindow is None:
        return
    elif currentWindow is currentLayout.focus_first():
        targetIndex = SCREEN_LEFTOF[screenIndex]
        qtile.focus_screen(targetIndex)
        leftGroup = qtile.screens[targetIndex].group
        currentWindow.togroup(leftGroup.name)
        colIndex = None
        for i, col in enumerate(leftGroup.layout.columns):
           if currentWindow in col: 
                colIndex = i
                break
        lastColIndex =len(leftGroup.layout.columns)-1
        isLastColumn = colIndex == lastColIndex
        if not isLastColumn:
            leftGroup.layout.swap_column(colIndex,lastColIndex)
        return
    else:
        currentLayout.cmd_shuffle_left()
        return

def moveRight(qtile):
    currentGroup = qtile.current_screen.group
    currentLayout = qtile.current_layout
    currentWindow = qtile.current_window
    screenIndex = qtile.current_screen.index
    columnIndex = currentLayout.current
    if currentWindow is None:
        return
    elif currentWindow is currentLayout.focus_last():
        targetIndex = SCREEN_RIGHTOF[screenIndex]
        qtile.focus_screen(targetIndex)
        rightGroup = qtile.screens[targetIndex].group
        currentWindow.togroup(rightGroup.name)
        colIndex = None
        for i, col in enumerate(rightGroup.layout.columns):
           if currentWindow in col: 
                colIndex = i
                break
        isFirstColumn = colIndex == 0
        if not isFirstColumn:
            rightGroup.layout.swap_column(colIndex,0)
        return
    else:
        currentLayout.cmd_shuffle_right()
        return

keys = [
    # Switch between windows
    # Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "h", lazy.function(focusLeft), desc="Move focus to left"),
    Key([mod], "l", lazy.function(focusRight), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.function(moveLeft),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.function(moveRight),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "shift"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "shift"], "e", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn("rofi -combi-modi window,drun,ssh -theme solarized -font \"hack 10\" -show combi"
        ),
        desc="Spawn a command using a prompt widget"),

    Key([mod], "b", lazy.spawn("gtk-launch google-chrome.desktop"), desc="Launch Chrome"),
]

groups = [Group(i) for i in "123456789"]


def changeWorkspace(qtile, wsIndex):
    screens = qtile.screens
    groupMap = qtile.groups_map
    # Screen Indices
    right = screens[SCREEN_RIGHT_INDEX]
    left = screens[SCREEN_LEFT_INDEX]
    mid = screens[SCREEN_MID_INDEX]
    # There are groups from 1-9
    # That means there are 3 workspaces 1-3
    i = wsIndex -1
    left.set_group(groupMap[str(i*3+1)])
    mid.set_group(groupMap[str(i*3+2)])
    right.set_group(groupMap[str(i*3+3)])


for i in range(1,4):
    keys.extend([
        Key([mod], str(i), lazy.function(changeWorkspace, i),
            desc="Switch to workspace {}".format(i)),
    ])

for i in groups:
    keys.extend([
        # # mod1 + shift + letter of group = move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            desc="move focused window to group {}".format(i.name)),
    ])


layouts = [
    layout.Columns(border_focus_stack='#d75f5f'),
    # layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='sans',
    fontsize=14,
    padding=3,
)
extension_defaults = widget_defaults.copy()

def myScreen(): 
    return Screen(
            bottom=bar.Bar(
                [
                    widget.AGroupBox(),
                    widget.CurrentLayout(),
                    widget.GroupBox(),
                    widget.WindowName(),
                    widget.Chord(
                        chords_colors={
                            'launch': ("#ff0000", "#ffffff"),
                        },
                        name_transform=lambda name: name.upper(),
                    ),
                    widget.Systray(),
                    widget.Clock(format='%Y-%m-%d %a %I:%M %p'),
                    widget.QuickExit(),
                ],
                24,
            ),
            wallpaper="/home/arizona/Documents/Bash Scripts/auto-wallpaper/wallpaper.jpg",
            wallpaper_mode="stretch"
        )

screens = [myScreen(),myScreen(),myScreen()]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = True
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
