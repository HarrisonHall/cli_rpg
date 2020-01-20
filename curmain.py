from modules import Party
from modules import EventHandler
from modules import Exist
from modules import Text
from sys import argv, exit
import curses

from implib.WindowHandler import WindowHandler
from implib.Pane import Pane
from implib.Interaction import make_colors, interact


if __name__ == "__main__":
    current_place = "Hallway"
    party = Party.Party(debug=True)

    print("CLI RPG DEMO BY HARRISON HALL")

    eh = EventHandler.EventHandler()
    Exist.Exist.debug = True
    Exist.Exist.start_log()
    Text.Text.use_curses_color()
    print("DONE LOADING\n---")

    stdscr = curses.initscr()
    curses.start_color()
    curses.curs_set(0)
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)
    make_colors()
    #curses.resizeterm(35,90)
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    wh = WindowHandler(stdscr)
    wh.text_win.add("CURSES RPG DEMO\nBY HARRISON HALL")

    eh.enter_room(party, current_place)
    while True:
        options = eh.base_interaction(party.room, party)
        interact(options, party.room, wh, stdscr, eh, party)
