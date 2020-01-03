from modules import Exist

class Personality(Exist.Exist):
    def __init__(self, pdict):
        self.rapports = pdict.get("rapports", {})
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

    def add_rapport(self, person, flag, value):
        if person.name not in self.rapports:
            self.rapports[person.name] = {
                "count": 1,
                flag: value
            }
        else:
            if flag in self.rapports[person.name]:
                self.rapports[person.name][flag] += value
            else:
                self.rapports[person.name][flag] = value

    def is_creeped_out(self, person):
        if person.name not in self.personality:
            if self.agreeableness() + self.openness() < self.neuroticism():
                return True
        else:
            rapport = self.rapports[person.name]
            
        return False

    def is_seducable(self, person):
        if person.name not in self.personality:
            if person.openness() > self.conscientiousness() + self.neuroticism():
                return True
        else:
            return False
