from modules import Exist

class Thing(Exist.Exist):
    def class_specific(self, pdict):
        return None

    def interact(self, player, room):
        return {
            "Description": {
                "fun": self.do_description,
                "vals": [player, room]
            },
            "Dialogue": {
                "fun": self.do_dialogue,
                "vals": ["start", player, room]
            },
            "Inventory": {
                "fun": self.do_inventory,
                "vals": [player, room]
            },
            "Back": {
                "fun": None,
                "vals": []
            }
        }

    def do_inventory(self, player, room):
        d = {}
        for item in self.inventory:
            key = self.inventory[item].get("exists", "start")
            if self.thing_exists_yet(player, key):
                item_rep = f"{item} ({self.inventory[item].get('count',1)})"
                d[item_rep] = {
                    "fun": self.give_item,
                    "vals": [player, room, item, 1]
                }
        if len(self.inventory) > 1:
            d["Take all"] = {
                "fun": self.give_item,
                "vals": [player, room, "all", -1]
            }
        d["Back"] = {
            "fun": self.interact,
            "vals": [player, room]
        }
        return d
