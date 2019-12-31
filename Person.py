import Exist
from random import choices

class Person(Exist.Exist):
    def class_specific(self, pdict):
        self.hp = pdict.get("hp", 5)  # current life
        self.max_hp = pdict.get("max_hp", self.hp)
        self.magic = pdict.get("magic", 1)  # magic
        self.armor = pdict.get("armor", 1)

        self.in_battle = pdict.get("in_battle", False)

        self.race = pdict.get("race", "human")

        self.usable_attacks = pdict.get("attacks", {})

        self.death_message = pdict.get(
            "death_message",
            f"{self.name} has died."
        )

    def will_sell(self):
        return self.flags.get("will_sell", False)

    def is_alive(self):
        return (self.hp > 0)

    def is_dead(self):
        return (self.hp <= 0)

    def interact(self, player, room):
        if not self.in_battle:
            key = self.get_key(player, room)
            return {
            "Dialogue": {
                "fun": self.do_dialogue,
                "vals": [key, player, room]
            },
                "Description": {
                    "fun": self.do_description,
                    "vals": [player, room]
                },
                "Attack": {
                    "fun": self.do_attack,
                    "vals": [player, room]
                },
                "Back": {
                    "fun": None,
                    "vals": []
                }
            }
        else: # battle
            return self.do_attack(player, room)

    def do_attack(self, player, room):
        if self.is_alive():
            return player.get_attacks(self, room)
        else:
            return {}

    def attack_back(self, player):
        if self.is_dead():
            return ""
        if self.usable_attacks == {}:
            return f"{self.name} can't attack back."
        attack = choices(
            list(self.usable_attacks.keys()),
            list(self.usable_atttacks.values())
        )[0]
        self.attacks[]

    def do_damage(self, damage, now_in_battle=True):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
        if self.is_dead():
            return self.death_message
        else:
            mess = (
                self.name + " has taken " +
                "{:.2f}".format(damage) + " damage."
            )
            if now_in_battle:
                self.in_battle = True
                mess += f"\n{self.name} is now in battle."
            return mess

    def __repr__(self):
        if self.is_dead():
            return f"XDEADX {self.name}"
        return f"{self.name} ___DEBUG___ HP {self.hp}"
