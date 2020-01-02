from json import load
from modules import Exist, Player, Person
from modules import Thing, Room, Attack
from modules import Item
from os import listdir
from sys import argv, exit
from os.path import isdir

def interact(some_dict, room):
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
            print(some_dict)
            return None

    if "message" in some_dict:
        print(some_dict["message"])
        some_dict.pop("message")

    if "quit" in some_dict:
        exit()

    if some_dict == {}:
        return None
    
    c = ""
    l = list(some_dict.keys())
    print()
    while not is_valid(c):
        for i, l1 in enumerate(l):
            print(f"{i}) {l1}")
        c = input(">> ")
        if not is_valid(c):
            print("Not valid.")
    choice = some_dict[l[int(c)]]
    if choice["fun"] is not None:
        interact(choice["fun"](*choice["vals"]), room)
    return None

def get_current_stuff(room, player):
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
        "fun": exit,
        "vals": []
    }
    return current

def goto_room(new_room, player):
    print(f"ENTER: {new_room}")
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
    for w in argv:
        if w in ["v"]:
            print(f"Spells: {player.spells}")
            print(f"People: {people}")
            print(f"Places: {rooms}")
            exit()

    goto_room(current_place, player)
    while True:
        options = get_current_stuff(player.room, player)
        interact(options, player.room)
