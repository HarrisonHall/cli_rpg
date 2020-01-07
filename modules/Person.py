from modules import Exist
from random import choices

class Person(Exist.Exist):
    def class_specific(self, pdict, in_party=False):
        self.hp = pdict.get("hp", 5)  # current life
        self.max_hp = pdict.get("max_hp", self.hp)
        self.magic = pdict.get("magic", 1)  # magic
        self.energy = pdict.get("energy", 10)
        self.armor = pdict.get("armor", 1)

        self.level = pdict.get("level", 2)

        self.in_battle = pdict.get("in_battle", False)

        self.race = pdict.get("race", "human")

        self.usable_weapons = pdict.get("weapons", {
            "hand": None
        })

        self.usable_attacks = pdict.get("attacks", {})
        if "all" in self.usable_attacks:
            self.usable_attacks = self.attacks

        self.death_message = pdict.get(
            "death_message",
            f"{self.name} has died."
        )

        self.events = pdict.get("events", {
            "start": None,
            "begin": None
        })
        self.current_event = pdict.get("current_event", "start")

        self.in_party = in_party

    def will_sell(self):
        return self.flags.get("will_sell", False)

    def is_alive(self):
        """True if hp > 0"""
        return (self.hp > 0)

    def is_dead(self):
        """True if hp <= 0"""
        return (self.hp <= 0)

    def interact(self, player, room):
        if self.in_party:
            return self.party_interaction(player, room)
        
        key = self.get_key(player, room)
        d = {}
        d["About"] = {
            "fun": self.do_about,
            "vals": [player, room]
        }
        d["Description"] = {
            "fun": self.do_description,
            "vals": [player, room]
        }
        d["Dialogue"] = {
            "fun": self.do_dialogue,
            "vals": [key, player, room]
        }
        if self.is_dead():
            d["Inventory"] = {
                "fun": self.do_inventory,
                "vals": [player, room]
            }
        if not self.is_dead():
            d["Attack"] = {
                "fun": self.do_attack,
                "vals": [player, room]
            }
        if not self.in_battle or self.is_dead():
            d["Back"] = {
                "fun": None,
                "vals": []
            }
        return d

    def party_interaction(self, party, room):
        return {
            "About": {
                "fun": self.do_about,
                "vals": [self, room]
            },
            "Inventory": {
                "fun": self.do_inventory,
                "vals": [self, room]
            },
            "Flags": {
                "fun": self.do_flags,
                "vals": []
            },
            "Back": {
                "fun": None,
                "vals": []
            }
        }

    def do_about(self, player, room):
        """
        Text about player
        """
        if self.in_party:
            self.debug_print("DEBUG ON")
            self.log("TEST LOG")
        d = self.interact(player, room)
        d["message"] = self.status_message()
        return d

    def status_message(self):
        return (
            f"NAME: {self.name}\n"
            f"RACE: {self.race}\n"
            f"ARM: {self.armor}\n"
            f"DESC: {self.description}"
        )

    def get_attacks(self, person, room):
        d = {}
        for attack in self.usable_attacks:
            if attack in self.attacks:
                d[self.attacks[attack]] = {
                    "fun": self.attacks[attack].damage_and_effects,
                    "vals": [self, person, room]
                }
        for weapon in self.usable_weapons:
            if weapon in self.weapons:
                d.update(self.weapons[weapon].get_attacks(self, person, room))
        if not person.in_battle: # todo and player in battle?
            d["Back"] = {
                "fun": person.interact,
                "vals": [self, room]
            }
        return d
    
    def do_attack(self, player, room):
        if self.is_alive():
            dattacks = player.get_attacks(self, room)
            dattacks["Back"] = {
                "fun": self.interact,
                "vals": [player, room]
            }
            return dattacks
        else:
            return {}

    def attack_back(self, player, room):
        if self.is_dead():
            return ""
        if self.usable_attacks == {}:
            return f"{self.name} can't attack back."
        attack = choices(
            list(self.usable_attacks.keys()),
            list(self.usable_attacks.values())
        )[0]
        mess = f"{self.name} uses {attack}\n"
        mess += self.attacks[attack].damage_and_effects_back(self, player, room)
        return mess

    def do_damage(self, damage, now_in_battle=True):
        mess = ""
        if self.in_party:
            self.hp -= damage
            if self.hp <= 0:
                self.hp = 0
            else:
                mess += (
                    "\n" + self.name + " has taken " +
                    "{:.2f}".format(damage) + " damage."
                )
            return mess
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
        if self.is_dead():
            return mess + "\n" + self.death_message
        else:
            mess += (
                "\n" + self.name + " has taken " +
                "{:.2f}".format(damage) + " damage."
            )
            if now_in_battle and not self.in_battle and damage >= 0:
                self.in_battle = True
                mess += f"\n{self.name} is now in battle."
        mess += self.manage_effects()
        return mess

    def manage_effects(self):
        mess = ""
        tot_effects = {}
        tot_effects.update(self.effects)
        for effect in self.effects:
            self.effects[effect] += 1
        for effect in self.effects:
            if effect == "in_battle":
                if not self.in_battle:
                    self.in_battle = True
                    mess += f"{self.name} now in battle."
                if self.effects["in_battle"] >= 3:
                    tot_effects.pop("in_battle")
            elif effect == "seduce":
                pass
            elif effect == "creep":
                pass
            elif effect == "sadden":
                pass
        self.effects = tot_effects
        return mess

    def do_inventory(self, player, room):
        d = {}
        for item in self.inventory:
            key = self.inventory[item].get("exists", "start")
            if self.thing_exists_yet(player, key):
                item_rep = f"{item} ({self.inventory[item].get('count',1)})"
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

    def do_flags(self):
        d = self.interact(self, None)
        mess = str(self.flags)
        d["message"] = mess
        return d

    def __repr__(self):
        if self.is_dead():
            return f"X {self.name}"
        return self.name
