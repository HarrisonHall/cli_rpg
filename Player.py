import Exist

class Player(Exist.Exist):
    def class_specific(self, pdict):
        self.name = "Bardwin"
        self.hp = 10
        self.max_hp = 10
        self.magic = 10
        self.armor = 2

        self.level = 1

        self.items = {
            "potion",
        }
        self.usable_attacks = {
            "Uppercut",
            "Swing",
            "Frost"
        }

        self.story_point = 0
        self.events = {
            "start": None,
            "begin": None,
        }
        self.current_event = "start"

    def interact(self):
        return {
            "About": {
                "fun": self.do_about,
                "vals": [],
            },
            "Items": {
                "fun": self.do_items,
                "vals": []
            },
            "Back": {
                "fun": None,
                "vals": [],
            }
        }

    def do_items(self):
        d = {}
        for item in self.items:
            d[item] = {
                "fun": None,
                "vals": []
            }
        d["Back"] = {
            "fun": self.interact,
            "vals": []
        }
        return d

    def do_about(self):
        print(
            f"Name: {self.name}\n"
            f"Current Event: {self.current_event}\n"
            f"HP: {self.hp}/{self.max_hp}\n"
            f"MAG: {self.magic}\n"
            f"ARM: {self.armor}\n"
            f"LVL: {self.level}"
        )
        return self.interact()


    def get_attacks(self, person, room):
        d = {}
        for attack in self.attacks:
            d[attack] = {
                "fun": self.attacks[attack].damage_and_effects,
                "vals": [self, person, room]
            }
        if not person.in_battle:
            d["Back"] = {
                "fun": person.interact,
                "vals": [self, room]
            }
        return d

    def __repr__(self):
        return f"{self.name} HP:{self.hp}/{self.max_hp}"
