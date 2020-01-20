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

    def refresh(self):
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

    def __del__(self):
        return
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

class Pane:
    def __init__(
            self, h : int, w : int, y : int, x : int,
            draw_border=True
    ):
        self.draw_border = draw_border
        self.h = h
        self.w = w
        self.y = y
        self.x = x
        self.win = curses.newwin(h,w,y,x)
        self.clear()

    def clear(self):
        self.buf = [
            [
                [" "] for i in range(self.w)
            ] for j in range(self.h)
        ]

    def refresh(self):
        self.win.clear()
        for i, row in enumerate(self.buf):
            for j, item in enumerate(row):
                #print(f"{self.w} {self.h} {i} {j} '{item[0]}'| ", end="")
                #print(i, j, item[0], 1)
                #print(*[curses.color_pair(t) for t in item[1:]])
                atts = [curses.color_pair(t) for t in item[1:]]
                if len(atts) > 0:
                    try:
                        self.win.addnstr(
                            i, j, item[0], 1, *atts
                        )
                    except Exception:
                        pass
                else:
                    try:
                        self.win.addnstr(
                            i, j, item[0], 1
                        )
                    except Exception:
                        pass
        self.border()
        self.win.refresh()

    def border(self) -> None:
        if not self.draw_border:
            return None
        if self.h == 1:
            for i in list(range(self.w)):
                if i == 0:
                    self.addnstr(0, i, "·")
                elif i == self.w-1:
                    self.addnstr(0, i, "·")
                else:
                    self.addnstr(0, i, " ")
            return None
        for i, row in enumerate(self.buf):
            for j, item in enumerate(row):
                if i in [0, self.h -1]:
                    self.addnstr(i, j, "=")
                if j in [0, self.w -1]:
                    self.addnstr(i, j, "‖")
                if i in [0] and j in [0, self.w-1]:
                    self.addnstr(i, j, "∇")
                if i in [self.h-1] and j in [0, self.w-1]:
                    self.addnstr(i, j, "Δ")
        return None

    def addnstr(self, i, j, char, length=1, *attrs):
        if len(attrs) == 0:
            try:
                self.win.addnstr(i, j, char, length)
            except Exception as e:
                pass
        else:
            try:
                self.win.addnstr(i, j, char, length, attrs)
            except Exception as e:
                pass
        return None

    def add(self, text, clear=False):
        if clear:
            self.clear()
        if isinstance(text, str):
            self.add_str(text)
        if isinstance(text, Text.Text):
            self.add_textobj(text)
        if self.draw_border:
            self.add_row()
        return None

    def add_str(self, text : str) -> None:
        #self.add_row()
        i = 1 if self.draw_border else 0
        while text != "":
            if text[0] == "\n":
                self.add_row()
                i = 1 if self.draw_border else 0
                text = text[1:]
                continue
            elif i >= self.w - (1 if self.draw_border else 0):
                self.add_row()
                i = 1 if self.draw_border else 0
                continue
            else:
                #print(f"|{len(self.buf)} {i}|",end="")
                self.buf[-1][i] = [text[0]]
            text = text[1:]
            i += 1
        return None

    def add_textobj(self, text : Text.Text) -> None:
        self.add_row()
        i = 1 if self.draw_border else 0
        for character_list in text:
            #Exist.Exist.class_log(str(character_list))
            char = character_list[0]
            attrs = character_list[1:]
            if char == "\n":
                self.add_row()
                i = 1 if self.draw_border else 0
                continue
            elif i >= self.w - (1 if self.draw_border else 0):
                self.add_row()
                i = 1 if self.draw_border else 0
                self.buf[-1][i] = character_list
            else:
                self.buf[-1][i] = character_list
            i += 1
        return None

    def add_row(self) -> None:
        self.buf = self.buf[1:] + [[[" "] for w in range(self.w)]]
        return None

    def add_choices(self, text):
        return None

    def nodelay(self,flag):
        self.win.nodelay(flag)
        return None

def do_exit(stdscr):
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
    exit()


def interact(some_dict, room, wh, stdscr, eh):
    def is_valid(character):
        if character.isdigit():
            if int(character) in range(len(some_dict.keys())):
                return True
        return False
    
    if not isinstance(some_dict, dict):
        if isinstance(some_dict, str):
            if "end" in some_dict:
                return None
        if some_dict is None:
            return None
        else:
            #print(some_dict)
            return None

    wh.map_win.add(room.get_mapping(wh.map_win.h, wh.map_win.w, 0, 0))

    wh.refresh()

    if "message" in some_dict:
        wh.text_win.add(some_dict["message"])
        some_dict.pop("message")

    wh.status_win.add("STATUS", clear=True)
    for player in party.players:
        wh.status_win.add(player.status_message(), clear=False)
        wh.status_win.add(" ")

    if "quit" in some_dict:
        do_exit(stdscr)
        
    if some_dict == {}:
        return None
    
    c = ""
    l = list(some_dict.keys())
    wh.choice_win.nodelay(True)
    i = 0
    j = 5
    chars = ["e", "d", "c", "r", "f", "v"]
    r = True
    while not is_valid(c):
        if r:
            wh.choice_win.add(get_choices(some_dict, i, j, chars, eh), clear=True)
            wh.refresh()
            r = False
        c = wh.choice_win.win.getch()
        try:
            c = chr(c)
        except:
            c =""
        if "w" in c.lower():
            r = True
            if i > 0:
                i -= 1
                j -= 1
        if "s" in c.lower():
            r = True
            if j < len(l)-1:
                i += 1
                j += 1
        if "q" in c:
            curses.nocbreak()
            stdscr.keypad(False)
            curses.echo()
            curses.endwin()
            curses.curs_set(1)
            exit()
        c = get_option(some_dict, i, j, c, chars)
    wh.choice_win.nodelay(False)
    num = l[int(c)]
    choice = some_dict[num]
    wh.text_win.add(f"⇒ {num}")
    if choice["fun"] is not None:
        interact(
            choice["fun"](*choice["vals"]), room, wh, stdscr, eh
        )
    return None

def get_choices(d, a : int, b : int, chars, eh, print_c=True):
    m = Text.Text("")
    choices = list(d.keys())
    for i in range(len(choices)):
        if i == a:
            m.add_message("w↑: ",space="")
        elif i == b:
            m.add_message("s↓: ",space="")
        else:
            m.add_message(" "*4,space="")
        if i >= a and i <= b:
            if len(chars) == 1 + abs(b-a):
                m.add_message(f"{chars[i-a]}) ")
            m = m + eh.as_text(str(choices[i]))
            if i < len(choices) - 1:
                m.add_message("\n",space="")
    Exist.Exist.class_log(str(m.message))
    return m

def get_option(d, a, b, char, chars):
    choices = list(d.keys())
    xlist = []
    for i in range(len(choices)):
        if i >= a and i <= b:
            xlist.append(chars[i-a])
        else:
            xlist.append("69")
    for i, choice in enumerate(xlist):
        if choice == char:
            return str(i)
    return "-1"

def make_colors():
    print(curses.can_change_color())
    if curses.can_change_color():
        curses.init_color(1, 98, 114, 164)
        curses.init_color(2, 139, 233, 253)
        curses.init_color(3, 80, 250, 123)
        curses.init_color(4, 255, 184, 108)


current_place = "Hallway"
party = Party.Party(debug=True)

print("CLI RPG DEMO BY HARRISON HALL")

eh = EventHandler.EventHandler()
Exist.Exist.debug = True
Exist.Exist.start_log()
Text.Text.use_curses_color()
print("DONE LOADING\n---")



if __name__ == "__main__":
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
        interact(options, party.room, wh, stdscr, eh)
