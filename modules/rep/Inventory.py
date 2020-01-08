from modules import Exist

class Inventory():
    def __init__(self, person, pdict={}):
        self.items = pdict.get("items", {})
        self.money = pdict.get("money", 0)
        self.person = person

    def give_item(self, person, room, item, count):
        person.inventory.add_item(item, count)
        if item in Exist.Exist.items:
            for event in Exist.Exist.items[item].events:
                val = Exist.Exist.items[item].events[event]
                person.add_flag(event, val)
        self.remove_item(item, count)
        return None

    def sell_item(self, person, room, item, count, cost_per):
        if count * cost_per > person.inventory.money:
            return False
        person.give_item(item, count)
        self.remove_item(item, count)
        return True

    def add_item(self, item, count):
        if item in self.items:
            self.items[item]["count"] = self.items[item].get("count", 0) + count
        else:
            self.items[item] = {
                "count": count
            }
        return None

    def remove_item(self, item, count):
        self.add_item(item, -count)
        if self.items[item]["count"] <= 0:
            self.items.pop(item)
        return None

    def get_count(self, item):
        return self.items.get(item, {}).get("count", 0)

    def get_inventory(self, player=None):
        tot = {}
        if player == None:
            for item in self.items:
                tot[item] = self.items[item]["count"]
        else:
            for item in self.items:
                if item in Exist.Exist.items:
                    if len(
                            player.flags.similar_flags(
                                Exist.Exist.items[item].exists)
                    ) > 0:
                        tot[item] = self.items[item]["count"]
                else:
                    tot[item] = self.items[item]["count"]
        return tot

    def __repr__(self):
        mess = ""
        for item in items:
            mess += item + ","
        return mess
