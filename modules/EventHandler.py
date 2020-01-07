from json import load
from os import listdir
from os.path import isdir

from modules import Exist
from modules import Party
from modules import Person
from modules import Thing
from modules import Room
from modules import Attack
from modules import Item
from modules import Weapon
from modules import Event

class EventHandler:
    """
    EventHandler is a class designed for managing the events,
    environment, and interactions of the game. 
    
    In order to make this usable, an interaction handler is
    required to generate input and display output.
    """
    rooms = {}
    people = {}
    things = {}
    attacks = {}
    items = {}
    weapons = {}
    events = {}
    
    def __init__(self, directory="base"):
        self.read_files(directory)

    def read_files(self, directory):
        self.objs_from_dirs(Person.Person, self.people,
                            f"{directory}/people")
        self.objs_from_dirs(Room.Room, self.rooms,
                       f"{directory}/rooms")
        self.objs_from_dirs(Thing.Thing, self.things,
                       f"{directory}/things")
        self.objs_from_dirs(Attack.Attack, self.attacks,
                       f"{directory}/attacks")
        self.objs_from_dirs(Item.Item, self.items,
                       f"{directory}/items")
        self.objs_from_dirs(Weapon.Weapon, self.weapons,
                       f"{directory}/weapons")
        self.objs_from_dirs(Event.Event, self.events,
                       f"{directory}/events")
        Exist.Exist.update_all_dicts(
            all_attacks=self.attacks, all_people=self.people,
            all_things=self.things, all_rooms=self.rooms,
            all_items=self.items, all_weapons=self.weapons
        )
        Exist.Exist.debug = True
        Exist.Exist.start_log()

    def read_save(self, fname):
        # TODO
        return None

    def objs_from_dirs(self, the_class, obj_dict, dir_name):
        for file1 in listdir(dir_name):
            cur_name = f"{dir_name}/{file1}"
            if isdir(cur_name):
                self.objs_from_dirs(the_class, obj_dict, cur_name)
                continue
            f = open(cur_name, "r")
            new_obj = the_class(pdict=load(f))
            obj_dict.update({
                new_obj.name : new_obj
            })
            f.close()

    def base_interaction(self, room, party):
        for event in self.events:
            e = self.events[event]
            if not e.complete:
                if e.requirements_met(party, room):
                    return e.interact(party, room)
        current = {}
        player = party.current_player
        for person in room.new_people: # TODO CEHCK IF IN PARTY
            r = room.new_people[person]
            if not party.check_flag(r.get("exists","begin")):
                continue
            if person in self.people:
                if self.people[person].exists_yet(party):
                    current[self.people[person]] = {
                        "fun": self.people[person].interact,
                        "vals": [player, room]
                    }
            else:
                pass
        for thing in room.new_things:
            if not party.check_flag(
                    room.new_things[thing].get("exists","begin")
            ):
                continue
            if thing in self.things:
                if self.things[thing].exists_yet(party):
                    current[thing] = {
                        "fun": self.things[thing].interact,
                        "vals": [player, room],
                    }
            else:
                pass
        for room2 in room.new_rooms:
            if not party.check_flag(
                    room.new_rooms[room2].get("exists", "begin")
            ):
                continue
            if room2 in self.rooms:
                if self.rooms[room2].exists_yet(party):
                    current[self.rooms[room2]] = {
                        "fun": self.enter_room,
                        "vals": [party, room2]
                    }
        current[party] = {
            "fun": party.interact,
            "vals": [],
        }
        return current

    def enter_room(self, party, new_room):
        party.enter_room(new_room)
