from modules import Party
from modules import EventHandler
from modules import Exist
from modules import Text
from sys import argv, exit
import curses

global text_buf
global choice_buf

class WindowHandler:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.term_height, self.term_width = stdscr.getmaxyx()
        
        self.first_win = Pane(10, self.term_width-19, 0, 0)
        self.battle_win = Pane(1, self.term_width-19, self.first_win.h, 0, draw_border=True)
        self.text_win = Pane(
            self.term_height-19,self.term_width-19,
            self.first_win.h + self.battle_win.h,
            0
        )
        self.buffer_win = Pane(
            1, self.term_width,
            self.first_win.h+self.battle_win.h+self.text_win.h,
            0,
            draw_border=True
        )
        self.choice_win = Pane(
            6, self.term_width,
            self.first_win.h + self.battle_win.h + self.text_win.h + self.buffer_win.h,
            0,
            draw_border=False
        )
        self.announcement_win = Pane(
            1, self.term_width,
            self.first_win.h + self.battle_win.h + self.text_win.h + self.buffer_win.h + self.choice_win.h,
            0,
        )
        self.map_win = Pane(11, 19, 0, self.term_width - 19, draw_border=False)
        self.status_win = Pane(self.term_height-19, 19, self.map_win.h, self.term_width - 19)

    def refresh(self) -> None:
        for window in [
                self.first_win,
                self.battle_win,
                self.text_win,
                self.buffer_win,
                self.choice_win,
                self.announcement_win,
                self.map_win,
                self.status_win
        ]:
            window.refresh()
        return None

    def __del__(self):
        """Remove return to avoid bugs, keep to debug."""
        return
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()
