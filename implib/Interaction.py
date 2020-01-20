from modules import Party
from modules import EventHandler
from modules import Exist
from modules import Text
from sys import argv, exit
import curses


def do_exit(stdscr):
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
    exit()


def interact(
        some_dict : dict,
        room : "?",
        wh : "WindowHandler",
        stdscr,
        eh : "EventHandler",
        party : Party.Party
) -> None:
    """Should be looped to make a playable game."""
    def is_valid(character :str) -> bool:
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
            choice["fun"](*choice["vals"]), room, wh, stdscr, eh, party
        )
    return None


def get_choices(
        d : dict,
        a : int,
        b : int,
        chars : list,
        eh : "EventHandler",
        print_c=True
) -> Text.Text:
    m = Text.Text("")
    choices = list(d.keys())
    Exist.Exist.class_log(f"{d.keys()}, a{a}, b{b}")
    for i in range(len(choices)):
        if i == a:
            m.add_message("w↑: ",space="")
        elif i == b:
            m.add_message("s↓: ",space="")
        else:
            m.add_message(" "*4,space="")
        if i >= a and i <= b:
            #if len(chars) == 1 + abs(b-a):
            m.add_message(f"{chars[i-a]}) ")
            m = m + eh.as_text(str(choices[i]))
        if i < len(choices) - 1 and i != b:
            m.add_message("\n",space="")
    Exist.Exist.class_log(str(m.message))
    return m


def get_option(
        d : dict,
        a : int,
        b : int,
        char : str,
        chars : list
) -> str:
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


def make_colors() -> bool:
    print(curses.can_change_color())
    if curses.can_change_color():
        curses.init_color(1, 98, 114, 164)
        curses.init_color(2, 139, 233, 253)
        curses.init_color(3, 80, 250, 123)
        curses.init_color(4, 255, 184, 108)
        return True
    return False
