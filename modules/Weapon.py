from modules import Exist

class Weapon(Exist.Exist):
    """
    Weapons act as an interface between a person and an attack.

    Weapons can modify attacks too.
    """
    def class_specific(self, pdict):
        self.usage_message = pdict.get("usage_message", f"{self.name} was used.")

        self.associated_attacks = pdict.get("attacks", {})

        self.effects = pdict.get("effects", {})

        self.magic_cost = pdict.get("magic", 0)
        self.energy_cost = pdict.get("energy", 0)
        self.extra_damage = pdict.get("damage", 0)
        self.damage_multiplier = pdict.get("damage_multiplier", 1)

    def interact(self, player):
        """
        To be used in inventory later on.
        """
        return  None

    def get_attacks(self, caster, target, room):
        d = {}
        for attack in self.associated_attacks:
            if attack in self.attacks:
                a = self.attacks[attack]
                d[f"{self.name} || {a}"] = {
                    "fun": self.modify_attack,
                    "vals": [caster, target, room, a]
                }
        return d

    def modify_attack(self, caster, target, room, attack, caster_is_player=True):
        if not self.can_use_weapon_and_attack(caster, attack):
            if caster_is_player:
                d = target.interact(caster, room)
            else:
                d = caster.interact(target, room)
            d["message"] = "Cannot use weapon or attack."
            return d
        else:
            caster.energy -= self.energy_cost
            caster.magic -= self.magic_cost
            d = {
                "effects": self.effects,
                "extra_damage": self.extra_damage,
                "damage_multiplier": self.damage_multiplier
            }
            if caster_is_player:
                return attack.damage_and_effects(caster, target, room, mod=d)
            else:
                return attack.damage_and_effects_back(caster, target, room, mod=d)

    def can_use_weapon_and_attack(self, caster, attack):
        if caster.energy < self.energy_cost + attack.energy:
            return False
        if caster.magic < self.magic_cost + attack.magic:
            return False
        return True
