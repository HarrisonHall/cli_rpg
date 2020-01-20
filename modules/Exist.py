from modules.tools import Logger
from modules.rep import Personality
from modules.rep import Inventory
from modules import FlagHandler
from modules import Text

class Exist:
    attacks = {}
    people = {}
    rooms = {}
    things = {}
    items = {}
    weapons = {}
    debug = False
    LOGGING = False
    logger = None
    
    def __init__(self, pdict={}, debug=False, in_party=False):
        self.debug = debug
        if pdict == {}:
            self.name = ""
        else:
            for key in pdict:
                self.name = key
            pdict = pdict[self.name]
        
        self.inventory = Inventory.Inventory(self, pdict=pdict.get("inventory", {}))

        # mood, selling, other stuff
        self.flags = FlagHandler.FlagHandler(
            pdict.get("flags", {})
        )
        self.flags.add_flag(self.name, None)
        self.effects = {}

        self.dialogue = pdict.get("dialogue", {})
        self.description = pdict.get("description", "")

        self.story_points = pdict.get("story_point", {"start": None})
        self.personality = Personality.Personality(pdict)

        rep = pdict.get("representation", {})
        self.color = rep.get("color", "white")
        self.single = rep.get("single", self.name[0])[0]
        self.interaction_image = rep.get("interact", [])

        self.xpos = pdict.get("xpos", -1000)
        self.ypos = pdict.get("ypos", -1000)

        if in_party:
            self.class_specific(pdict, in_party=True)
            self.in_party = True
        else:
            self.in_party = False
            self.class_specific(pdict)

    def __repr__(self):
        return self.name

    def as_text(self):
        return Text.Text(self.name, self.color)

    @classmethod
    def update_all_dicts(
            cls,
            all_attacks={}, all_people={},
            all_rooms = {}, all_things = {},
            all_items={}, all_weapons={}
    ):
        """Update dictionaries of all objects.
        
        All objects that inhert from Exist have the same mappings.
        """
        cls.attacks.update(all_attacks)
        cls.rooms.update(all_rooms)
        cls.things.update(all_things)
        cls.people.update(all_people)
        cls.items.update(all_items)
        cls.weapons.update(all_weapons)
        return None

    @classmethod
    def start_log(cls):
        cls.LOGGING = True
        cls.logger = Logger.Logger()

    @classmethod
    def class_log(cls, message):
        if cls.LOGGING:
            cls.logger.log(message)

    def log(self, message):
        if self.LOGGING:
            self.logger.log(message)

    def exists_yet(self, player):
        """Returns True if player contains event in story_point."""
        for point in self.story_points:
            if player.check_flag(point):
                return True
        return False

    def thing_exists_yet(self, player, key):
        """Returns True if specific thing shares event with key."""
        if player.check_flag(key):
            return True
        return False

    def interact(self, player, room):
        """Base interaction does nothing."""
        return None

    def get_key(self, player, room):
        """
        Finds most likely key between player and object.
        
        TODO: special circumstances for room.
        This function needs to be overhaulled before story.
        """
        if player.current_event in self.dialogue:
            return player.current_event
        for k in self.dialogue:
            if k in player.events:
                return k

    def add_flag(self, flag, value):
        self.flags.add_flag(flag, value)

    def check_flag(self, flag):
        return self.flags.check_flag(flag)

    def do_dialogue(self, key, player, room, message=None):
        """
        Dialogue handling.
        """
        mess = Text.Text("")
        if self.is_dead():
            return {
                "message": mess.add_message(
                    f"{self.name} is dead."
                )
            }
        if key not in self.dialogue:
            l = self.interact(player, room)
            l["message"] = mess.add_message("INVALID KEY")
            return l
        d = self.dialogue[key]
        if message == None:
            update = {
                "message": mess.add_message(
                    f"{self.name}: {d['say']}"
                )
            }
        else:
            update = {
                "message": mess.add_message(
                    f"{message}\n{self.name}: {d['say']}"
                )
            }
        if "event" in d:
            player.add_flag(d["event"], None)
            player.current_event = d["event"]
        if "events" in d:
            for event in d["events"]:
                player.add_flag(event, d["events"][event])
        if "flags" in d:
            if "give" in d["flags"]:
                for item in d["flags"]["give"]:
                    self.give_item(
                        player,
                        room,
                        item,
                        d["flags"]["give"][item]
                    )
            if "end" in d["flags"]:
                r = self.interact(player, room)
                r.update(update)
                return r
        if "next" in d:
            r = self.do_dialogue(
                d["next"], player,
                room, message=update["message"]
            )
            return r
        if "choices" in d:
            r = {}
            for choice in d["choices"]:
                r[choice] = {
                    "fun": self.do_dialogue,
                    "vals": [d["choices"][choice], player, room]
                }
            r.update(update)
            return r
        r = self.interact(player, room)
        r.update(update)
        return r

    def is_dead(self):
        """The basis for existance is not death."""
        return False

    def is_alive(self):
        """The essence of existance is life."""
        return True

    def do_description(self, player, room):
        """Add message of description to interaction."""
        d = self.interact(player, room)
        d["message"] = Text.Text(self.description, color=self.color)
        return d

    def give_item(self, player, room, item, count):
        """Give item to a player."""
        self.personality.add_rapport(player, 1)
        inv = self.inventory.get_inventory(player=player)
        if item == "all":
            for item in inv:
                self.inventory.give_item(
                    player, room, item,
                    count
                )
        else:
            self.inventory.give_item(
                player, room, item,
                count
            )
        r = self.do_inventory(player, room)
        r["message"] = Text.Text("Item(s) added.")
        return r

    def sell_item(self, player, room, item, count, cost_per):
        possible = self.inventory.sell_item(player, room, item, count, cost_per)
        d = self.interact(player, room)
        if not possible:
            d["message"] = Text.Text("Not enough money.")
        d["message"] = Text.Text("Sold")
        return d

    def do_inventory(self, player, room):
        d = {}
        inv = self.inventory.get_inventory(player=player)
        if self.in_party:
            d[f"Money ${self.inventory.money}"] = {
                "fun": self.do_inventory,
                "vals": [player, room]
            }
        for item in inv:
            key = "start"
            item_rep = (
                f"{item} ({self.inventory.get_count(item)})"
            )
            if self.in_party:
                if item in self.items:
                    d[item_rep] = {
                        "fun": self.items[item].interact,
                        "vals": [self]
                    }
                else:
                    d[item_rep] = {
                        "fun": None,
                        "vals": []
                    }
            else:
                d[item_rep] = {
                    "fun": self.give_item,
                    "vals": [player, room, item, 1]
                }
        if not self.in_party:
            if len(self.inventory.get_inventory(player)) > 1:
                d["Take all"] = {
                    "fun": self.give_item,
                    "vals": [player, room, "all", -1]
                }
        d["Back"] = {
            "fun": self.interact,
            "vals": [player, room]
        }
        return d


    def add_item(self, item, count):
        self.inventory.add_item(item, count)
        return None

    def remove_item(self, item, count):
        self.inventory.remove_item(item, count)
        return None

    def class_specific(self, pdict):
        """Reserved for everything that inherits from Exist."""
        return None

    def debug_print(self, message):
        """
        Print to console (if debug).

        Alternatively .log(message) should be used.
        """
        if Exist.debug:
            print(message)
