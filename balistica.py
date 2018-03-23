import curses
import json

from shell import Shell

from curses import KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT

Y_MAX = 40
X_MAX = 80

"""import math

TIMEOUT = 100
INIT_VELOCITY = 3 # m/s
SHOT_ANGLE = 45 # degrees"""

# create standard screen
stdscr = curses.initscr()
# properly initialize the screen
curses.noecho() # don't echo chars as typed
curses.cbreak() # character break mode
curses.curs_set(0) # hide the cursor

# check for colour support
if curses.has_colors():
    curses.start_color()

# Optionally enable Function keys
# stdscr.keypad(1)

# Initialize colour combinations FG and BG
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)

# BEGIN PROGRAM
stdscr.addstr('BALISTICA', curses.A_REVERSE)
stdscr.chgat(-1, curses.A_REVERSE)

# change R to green`
#stdscr.chgat(curses.LINES-1, 7, 1, curses.A_BOLD | curses.color_pair(2))
# change Q to red
#stdscr.chgat(curses.LINES-1, 34, 1, curses.A_BOLD | curses.color_pair(1))

# window to hold all quotes
quote_window = curses.newwin(Y_MAX, X_MAX, 1, 0)
quote_window.keypad(True)
quote_window.timeout(100)
# subwindow to clearly display quotes
#quote_text_window = quote_window.subwin(curses.LINES-6, curses.COLS-4, 3, 2)
#quote_text_window.addstr("Press R to get your first quote!")

# Draw border around main quote window
quote_window.box()

# Update internal window data structs
stdscr.noutrefresh()
quote_window.noutrefresh()

# redraw the screen
curses.doupdate()

the_shell = Shell(int(Y_MAX / 2),
                  int(X_MAX / 2),
                  quote_window,
                  Y_MAX - 1,
                  X_MAX - 1)

try:
    # EVENT LOOP!
    while True:

        quote_window.clear()
        quote_window.box()
        the_shell.render()
        event = quote_window.getch()

        if event == 27:
            break

        if event in [KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT]:
            the_shell.change_direction(event)

        if event == 32:
            key = -1
            while key != 32:
                key = quote_window.getch()

        if event == ord('q') or event == ord('Q'):
            break

        stdscr.addstr(curses.LINES-1, 0, "Shell Coordinates: [%d, %d]" % the_shell.coord)

        #the_shell.update()

        # Refresh windows from bottom up to avoid flickering...
        stdscr.noutrefresh()
        quote_window.noutrefresh()
        #quote_text_window.noutrefresh()
        curses.doupdate()
except Exception as exc:
    raise
finally:
    # restore terminal settings
    curses.nocbreak()
    # stdscr.keypad(0)
    curses.echo()
    curses.curs_set(1)

    # REstore the terminal to former self
    curses.endwin()
