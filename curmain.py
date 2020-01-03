from json import load
from modules import Exist, Player, Person
from modules import Thing, Room, Attack
from modules import Item
from os import listdir
from sys import argv, exit
from os.path import isdir
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
        self.win.border()
        self.win.refresh()

    def add_to_buf(self, text, clear=False):
        if clear:
            self.buf = []
        l = text.split("\n")
        for line in l:
            self.buf.append(line)
            if len(self.buf) > self.h - 2:
                self.buf = self.buf[3:]

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

def do_exit(stdscr):
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
    exit()


def interact(some_dict, room, wins, stdscr):
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
    char_win.add_to_buf(player.status_message(), clear=True)

    if "quit" in some_dict:
        do_exit(stdscr)
        
    if some_dict == {}:
        return None
    
    c = ""
    l = list(some_dict.keys())
    text_win.add_to_buf("")
    while not is_valid(c):
        choice_win.add_choices_to_buf([f"{i}) {l1}" for i, l1 in enumerate(l)])
        refresh_wins(wins)
        c = chr(choice_win.win.getch())
        if "q" in c:
            curses.nocbreak()
            stdscr.keypad(False)
            curses.echo()
            curses.endwin()
            exit()
        if not is_valid(c):
            text_win.add_to_buf("Not valid.")
    choice = some_dict[l[int(c)]]
    if choice["fun"] is not None:
        interact(choice["fun"](*choice["vals"]), room, wins, stdscr)
    return None

def get_current_stuff(room, player, stdscr):
    current = {}
    for person in room.new_people:
        r = room.new_people[person]
        if r.get("exists","begin") not in player.events:
            continue
        if person in people:
            if people[person].exists_yet(player):
                current[people[person]] = {
                    "fun": people[person].interact,
                    "vals": [player, room]
                }
        else:
            pass
            #print(f"{person} not in people")
    for thing in room.new_things:
        if room.new_things[thing].get("exists","begin") not in player.events:
            continue
        if thing in things:
            if things[thing].exists_yet(player):
                current[thing] = {
                    "fun": things[thing].interact,
                    "vals": [player, room],
                }
        else:
            pass
            #print(f"{thing} not in things")
    for room2 in room.new_rooms:
        if room.new_rooms[room2].get("exists", "begin") not in player.events:
            continue
        if room2 in rooms:
            if rooms[room2].exists_yet(player):
                current[rooms[room2]] = {
                    "fun": goto_room,
                    "vals": [room2,player]
                }
        
    current[player] = {
        "fun": player.interact,
        "vals": [],
    }
    current["exit"] = {
        "fun": do_exit,
        "vals": [stdscr]
    }
    return current

def goto_room(new_room, player):
    #print(f"ENTER: {new_room}")
    player.room = rooms[new_room]

current_place = "Hallway"
player = Player.Player()

print("CLI RPG DEMO BY HARRISON HALL")
print(f"Player is {player.name}")

def objs_from_dirs(the_class, obj_dict, dir_name):
    for file1 in listdir(dir_name):
        cur_name = f"{dir_name}/{file1}"
        if isdir(cur_name):
            objs_from_dirs(the_class, obj_dict, cur_name)
            continue
        print(f"FILE {cur_name}")
        f = open(cur_name, "r")
        new_obj = the_class(pdict=load(f))
        obj_dict.update({
            new_obj.name : new_obj   
        })
        f.close()

rooms = {}
people = {}
things = {}
attacks = {}
items = {}
objs_from_dirs(Person.Person, people, "base/people")
objs_from_dirs(Room.Room, rooms, "base/rooms")
objs_from_dirs(Thing.Thing, things, "base/things")
objs_from_dirs(Attack.Attack, attacks, "base/attacks")
objs_from_dirs(Item.Item, items, "base/items")
Exist.Exist.update_all_dicts(
    all_attacks=attacks, all_people=people,
    all_things=things, all_rooms=rooms,
    all_items=items
)
print("DONE LOADING\n---")



if __name__ == "__main__":
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    h1 = int(curses.LINES*3/4)
    w1 = int(curses.COLS*3/4)
    h2 = h1
    w2 = curses.COLS - w1
    h3 = curses.LINES - h1
    w3 = curses.COLS
    
    text_win = window(h1,w1, 0, 0)
    char_win = window(h2, w2, 0, w1)
    choice_win = window(h3, w3, h1, 0)
    text_win.add_to_buf("CURSES RPG DEMO\nBY HARRISON HALL")

    for w in argv:
        if w in ["v"]:
            print(f"Spells: {player.spells}")
            print(f"People: {people}")
            print(f"Places: {rooms}")
            exit()
    

    goto_room(current_place, player)
    while True:
        options = get_current_stuff(player.room, player, stdscr)
        interact(options, player.room, [text_win, choice_win, char_win], stdscr)
