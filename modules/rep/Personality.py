from modules import Exist

class Personality():
    def __init__(self, pdict):
        # Rapports is a -10 to +10 scale of how likable
        # someone is to another.
        self.rapports = pdict.get("rapports", {})
        
        # Personality scale from 0 to 10 for each trait.
        self.personality = pdict.get(
            "personality",
            {
                "extraversion": 5,
                "neuroticism": 5,
                "agreeableness": 5,
                "conscientiousness": 5,
                "openness": 5,
            }
        )

    def openness(self):
        return self.personality["openness"]

    def extraversion(self):
        return self.personality["extraversion"]

    def neuroticism(self):
        return self.personality["neuroticism"]

    def agreeableness(self):
        return self.personality["agreeableness"]

    def conscientiousness(self):
        return self.personality["conscientiousness"]

    def base_rapport(self):
        s = 0
        for trait in self.personality:
            s += self.personality[trait] - 5
        return s

    def add_rapport(self, person, value):
        count = self.get_rapport_count(person) + 1
        self.rapports[person.name] = {
            "count": count,
            "val": self.get_rapport(person) + (value / count)
        }
        if value > 0:
            return f"{person.name}'s rapport has increased."
        elif value < 0:
            return f"{person.name}'s rapport has decreased."
        return ""

    def get_rapport(self, person):
        if person.name in self.rapports:
            return self.rapports[person.name]["val"]
        else:
            return self.base_rapport()

    def get_rapport_count(self, person):
        if person.name in self.rapports:
            return self.rapports[person.name]["count"]
        else:
            return 0

    def is_creeped_out(self, person):
        if self.get_rapport(person) < 0:
            if self.agreeableness() + self.openness() < self.neuroticism():
                return True
        return False

    def is_seducable(self, person):
        if self.get_rapport(person) > 0:
            if person.openness() > self.conscientiousness() + self.neuroticism():
                return True
        return False

    def is_friend(self, person):
        if self.get_rapport(self, person) > self.neuroticism():
            return True
        return False

    def is_aggressive(self, person):
        if self.extraversion() + self.neuroticism() > self.openness() + self.conscientiousness() + self.agreeableness():
            return True
        return False
