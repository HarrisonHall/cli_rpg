from modules import Exist
from modules.exist import Person

class Party():
    def __init__(self, debug=False):
        self.players = []
        if debug:
            self.add_member(self.debug_player1())
            self.add_member(self.debug_player2())
        self.current_player = self.players[0]
        self.room = ""

    def debug_player1(self):
        player = Person.Person(
            {
                "Äaä Berd" : {
                    "hp": 10,
                    "max_hp": 10,
                    "magic": 10,
                    "armor": 2,
                    "room": None,
                    "race": "Lentarde",
                    "level": 1,
                    "inventory": {
                        "items": {
                            "Potion": {
                                "count": 1
                            }
                        },
                        "money": 5 
                    },
                    "attacks": {
                        "Fire Blast": None,
                        "Frost": None,
                        "Lick": None,
                        "Wink": None,
                        "Harrass": None,
                    },
                    "story_point": 0,
                    "flags": {
                        "start": None,
                        "begin": None
                    },
                    "current_event": "start",
                    "weapons": {
                        "Standard Rapier": None,
                        "Hand": None
                    }
                }
            },
            in_party=True
        )
        return player

    def debug_player2(self):
        player = Person.Person(
            {
                "Sara Q'Dwel" : {
                    "hp": 5,
                    "max_hp": 5,
                    "magic": 5,
                    "armor": 3,
                    "race": "Mutt",
                    "level": 2,
                    "inventory": {
                        "items": {
                            "Elixir": {
                                "count": 1
                            }
                        }
                    },
                    "attacks": {
                        "Uppercut": None,
                        "Pout": None,
                        "Lick": None,
                        "Harrass": None
                    },
                    "story_point": 0,
                    "flags": {
                        "start": None,
                        "begin": None
                    },
                    "current_event": "start",
                    "weapons": {
                        "Hand": None
                    }
                }
            },
            in_party=True
        )
        return player

    def interact(self):
        return {
            "About": {
                "fun": self.do_about,
                "vals": [],
            },
            "Flags": {
                "fun": self.do_flags,
                "vals": []
            },
            "Set Lead": {
                "fun": self.do_lead,
                "vals": []
            },
            "Manage Members": {
                "fun": self.members,
                "vals": []
            },
            "Back": {
                "fun": None,
                "vals": [],
            }
        }

    def __repr__(self):
        mess = "Party"
        return mess

    def add_member(self, person):
        self.players.append(person)
        person.in_party = True

    def do_flags(self):
        d = self.interact()
        message = ""
        for player in self.players:
            message += str(player) + "\n"
            message += str(player.flags) + "\n"
        d["message"] = message
        return d

    def add_flag(self, flag, value):
        for member in self.players:
            member.add_flag(flag, value)

    def events(self):
        e = {}
        for player in self.players:
            e.update(player.events)
        return e

    def enter_room(self, new_room):
        self.room = Exist.Exist.rooms[new_room]

    def do_lead(self):
        d = {}
        for player in self.players:
            d[f"Set {player.name} as lead"] = {
                "fun": self.set_lead,
                "vals": [player]
            }
        d["Back"] = {
            "fun": self.interact,
            "vals": []
        }
        return d

    def set_lead(self, player):
        d = self.interact()
        d["message"] = f"{player.name} set as lead."
        self.current_player = player
        return d

    def do_about(self):
        l = self.interact()
        l["message"] = "ABOUT PARTY TODO"
        return l

    def members(self):
        d = {}
        for player in self.players:
            d[player] = {
                "fun": player.interact,
                "vals": [self, None]
            }
        d["Back"] = {
            "fun": self.interact,
            "vals": []
        }
        return d

    def check_flag(self, flag):
        for player in self.players:
            if player.check_flag(flag):
                return True
        return False

    def get_inventory(self):
        inv = {}
        for member in self.players:
            minv = member.inventory.get_inventory()
            for i in minv:
                if i in inv:
                    inv[i] += minv[i]
                else:
                    inv[i] = minv[i]
        return inv
