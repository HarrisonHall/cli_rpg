from modules import Party
from modules import EventHandler
from modules import Exist
from modules import Text
from sys import argv, exit
import curses

global text_buf
global choice_buf

class window:
    def __init__(self, h, w, y, x):
        self.h = h
        self.w = w
        self.y = y
        self.x = x
        self.win = curses.newwin(h,w,y,x)
        self.buf = []

    def print_list(self):
        start = 1
        self.win.clear()
        for line in self.buf:
            self.win.addnstr(start, 1, line, self.w-2)
            start += 1
        self.border()
        self.win.refresh()

    def border(self):
        self.win.border()
        return None

    def add_to_buf(self, text, clear=False):
        if isinstance(text, Text.Text):
            self.add_to_buf("Added Text Obj")
        if clear:
            self.buf = []
        l = text.split("\n")
        if text.endswith("\n"):
            l.append("ENDED WITH NEWLINE")
        for line in l:
            while len(line) > 0:
                self.buf.append(line[:self.w-2])
                line = line[self.w-2:]
                if len(self.buf) > self.h - 2:
                    self.buf = self.buf[1:]

    def add_choices_to_buf(self, choice_list, clear=True):
        if clear:
            self.buf = []
        i = 0
        while i < len(choice_list):
            total = ""
            to_add = choice_list[i]
            i += 1
            if i in range(len(choice_list)):
                to_add2 = choice_list[i]
                i += 1
                if len(to_add) > self.w // 2:
                    if len(to_add2) > self.w // 2:
                        total = to_add[:self.w] + to_add2[:self.w]
                    total = to_add[:self.w] + to_add2
                spaceing = " "*(self.w//2 - len(to_add))
                total = to_add + spaceing + to_add2
            else:
                total = to_add
            self.add_to_buf(total)

    def nodelay(self,flag):
        self.win.nodelay(flag)
        return None

def do_exit(stdscr):
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
    exit()


def interact(some_dict, room, wins, stdscr, eh):
    def is_valid(character):
        if character.isdigit():
            if int(character) in range(len(some_dict.keys())):
                return True
        return False

    def refresh_wins(ws):
        for win in wins:
            win.print_list()
    
    if not isinstance(some_dict, dict):
        if isinstance(some_dict, str):
            if "end" in some_dict:
                return None
        if some_dict is None:
            return None
        else:
            #print(some_dict)
            return None

    refresh_wins(wins)
    text_win = wins[0]
    choice_win = wins[1]
    char_win = wins[2]

    if "message" in some_dict:
        text_win.add_to_buf(some_dict["message"])
        some_dict.pop("message")

    char_win.add_to_buf("STATUS", clear=True)
    for player in party.players:
        char_win.add_to_buf(player.status_message(), clear=False)
        char_win.add_to_buf(" ")

    if "quit" in some_dict:
        do_exit(stdscr)
        
    if some_dict == {}:
        return None
    
    c = ""
    l = list(some_dict.keys())
    #text_win.add_to_buf("")
    choice_win.nodelay(True)
    choice_win.add_choices_to_buf([f"{i}) {l1}" for i, l1 in enumerate(l)])
    refresh_wins(wins)
    while not is_valid(c):
        c = choice_win.win.getch()
        try:
            c = chr(c)
        except:
            c =""
        if "q" in c:
            curses.nocbreak()
            stdscr.keypad(False)
            curses.echo()
            curses.endwin()
            exit()
    choice_win.nodelay(False)
    num = l[int(c)]
    choice = some_dict[num]
    text_win.add_to_buf(f"{c}) {num}")
    if choice["fun"] is not None:
        interact(
            choice["fun"](*choice["vals"]), room, wins, stdscr, eh
        )
    return None

current_place = "Hallway"
party = Party.Party(debug=True)

print("CLI RPG DEMO BY HARRISON HALL")

eh = EventHandler.EventHandler()
Exist.Exist.debug = True
#Exist.Exist.start_log()
print("DONE LOADING\n---")



if __name__ == "__main__":
    stdscr = curses.initscr()
    curses.resizeterm(35,90)
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    """
    h1 = int(curses.LINES*3/4)
    w1 = int(curses.COLS*3/4)
    h2 = h1
    w2 = curses.COLS - w1
    h3 = curses.LINES - h1
    w3 = curses.COLS
    """
    h1 = 10
    w1 = 60
    h2 = 25
    w2 = 30
    h3 = 9
    w3 = 90
    h4 = 1
    w4 = 90

    """
    text_win = window(h1,w1, 0, 0)
    char_win = window(h2, w2, 0, w1)
    choice_win = window(h3, w3, h1, 0)
    """
    text_win = window(h1,w1, 15, 0)
    char_win = window(h2, w2, 0, w1)
    choice_win = window(h3, w3, h2, 0)
    buffer_win = window(h4, w4, h2 + h3, 0)
    text_win.add_to_buf("CURSES RPG DEMO\nBY HARRISON HALL")

    eh.enter_room(party, current_place)
    while True:
        options = eh.base_interaction(party.room, party)
        interact(options, party.room, [text_win, choice_win, char_win], stdscr, eh)
