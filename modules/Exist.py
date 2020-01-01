class Exist:
    attacks = {}
    people = {}
    rooms = {}
    things = {}
    
    def __init__(self, pdict={}):
        if pdict == {}:
            self.name = ""
        else:
            for key in pdict:
                self.name = key
            pdict = pdict[self.name]
        
        self.items = pdict.get("items", {})

        # mood, selling, other stuff
        self.flags = pdict.get("flags", {})
        self.effects = {}

        self.events = pdict.get("events", {})
        self.dialogue = pdict.get("dialogue", {})
        self.description = pdict.get("description", "")

        self.story_points = pdict.get("story_point", {"start": None})

        self.all_attacks = {}
        self.all_people = {}
        self.all_rooms = {}
        self.all_things = {}

        self.class_specific(pdict)

    def class_specific(self, pdict):
        return None

    @classmethod
    def update_all_dicts(
            cls,
            all_attacks={}, all_people={},
            all_rooms = {}, all_things = {}
    ):
        cls.attacks.update(all_attacks)
        cls.rooms.update(all_rooms)
        cls.things.update(all_things)
        cls.people.update(all_people)
        return None

    def exists_yet(self, player):
        for event in player.events:
            for point in self.story_points:
                if event == point:
                    return True
        return False

    def is_alive(self):
        return True

    def __repr__(self):
        return self.name

    def interact(self, player, room):
        return None

    def get_key(self, player, room):
        if player.current_event in self.dialogue:
            return player.current_event
        for k in self.dialogue:
            if k in player.events:
                return k

    def do_dialogue(self, key, player, room, message=None):
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
        if "flags" in d:
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
        return False

    def is_alive(self):
        return True

    def do_description(self, player, room):
        d = self.interact(player, room)
        d["message"] = self.description
        return d
