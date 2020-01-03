from modules import Person

class Party():
    def __init__(self, debug=True):
        self.players = []
        if debug:
            self.players.append(self.debug_player1())
        self.current_player = self.players[0]

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
                        "Potion": {
                            "count": 1
                        }
                    },
                    "attacks": {
                        "all": {}
                    },
                    "story_point": 0,
                    "events": {
                        "start": None,
                        "begin": None
                    },
                    "current_event": "start"
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
            "Back": {
                "fun": None,
                "vals": [],
            }
        }

    def __repr__(self):
        mess = "PARTY"
        return mess

    def do_flags(self):
        message = ""
        for player in self.players:
            for flag in player.events:
                message += f"{flag}\n"
        return message

    def events(self):
        e = {}
        for player in self.players:
            e.update(player.events)
        return e

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
