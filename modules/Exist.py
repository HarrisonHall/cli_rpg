class Exist:
    attacks = {}
    people = {}
    rooms = {}
    things = {}
    items = {}
    
    def __init__(self, pdict={}):
        if pdict == {}:
            self.name = ""
        else:
            for key in pdict:
                self.name = key
            pdict = pdict[self.name]
        
        self.inventory = pdict.get("inventory", {})

        # mood, selling, other stuff
        self.flags = pdict.get("flags", {})
        self.effects = {}

        self.events = pdict.get("events", {})
        self.dialogue = pdict.get("dialogue", {})
        self.description = pdict.get("description", "")

        self.story_points = pdict.get("story_point", {"start": None})

        self.class_specific(pdict)

    def class_specific(self, pdict):
        """Reserved for everything that inherits from Exist."""
        return None

    @classmethod
    def update_all_dicts(
            cls,
            all_attacks={}, all_people={},
            all_rooms = {}, all_things = {},
            all_items={}
    ):
        """Update dictionaries of all objects.
        
        All objects that inhert from Exist have the same mappings.
        """
        cls.attacks.update(all_attacks)
        cls.rooms.update(all_rooms)
        cls.things.update(all_things)
        cls.people.update(all_people)
        cls.items.update(all_items)
        return None

    def exists_yet(self, player):
        """Returns True if player contains event in story_point."""
        for event in player.events:
            for point in self.story_points:
                if event == point:
                    return True
        return False

    def thing_exists_yet(self, player, key):
        """Returns True if specific thing shares event with key."""
        for event in player.events:
            if event == key:
                print(event, key)
                return True
        return False

    def __repr__(self):
        return self.name

    def interact(self, player, room):
        """Base interaction does nothing."""
        return None

    def get_key(self, player, room):
        """
        Finds most likely key between player and object.
        
        TODO: special circumstances for room.
        """
        if player.current_event in self.dialogue:
            return player.current_event
        for k in self.dialogue:
            if k in player.events:
                return k

    def do_dialogue(self, key, player, room, message=None):
        """
        Dialogue handling.
        """
        if self.is_dead():
            return {
                "message": f"{self.name} is dead."
            }
        if key not in self.dialogue:
            l = self.interact(player, room)
            l["message"] = "INVALID KEY"
            return l
        d = self.dialogue[key]
        if message == None:
            update = {
                "message": f"{self.name}: {d['say']}"
            }
        else:
            update = {
                "message": f"{message}\n{self.name}: {d['say']}"
            }
        if "event" in d:
            player.events[d["event"]] = None
            player.current_event = d["event"]
        if "events" in d:
            for event in d["events"]:
                player.events[event] = d["events"][event]
        if "flags" in d:
            if "give" in d["flags"]:
                for item in d["flags"]["give"]:
                    self.give_item(player, room, item, d["flags"]["give"][item])
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
        d["message"] = self.description
        return d

    def give_item(self, player, room, item, count):
        """Give item to a player."""
        if item == "all":
            tot = {}
            tot.update(self.inventory)
            for item in self.inventory:
                key = self.inventory[item].get("exists", "start")
                if self.thing_exists_yet(player, key):
                    player.add_item(item, self.inventory[item].get("count", 1))
                    tot.pop(item)
            self.inventory = tot
        else:
            player.add_item(item, count)
            self.inventory[item]["count"] = self.inventory[item].get("count", 1) - count
            if self.inventory[item]["count"] <= 0:
                self.inventory.pop(item)
        r = self.do_inventory(player, room)
        r["message"] = "Item(s) added."
        return r
