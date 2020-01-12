from modules import Exist
from modules import Background

class Room(Exist.Exist):
    def class_specific(self, pdict={}):
        self.new_rooms = pdict.get("new_rooms", {})

        self.new_people = pdict.get("people", {})
        self.new_things = pdict.get("things", {})
        self.background = Background.Background(
            seed = self.name,
            orderness = pdict.get("orderness", 50),
            brightness = pdict.get("brightness", 50),
            noisiness = pdict.get("noisiness", 50),
            f=pdict.get("f","")
        )

    def enter(self):
        """return Text for entering room."""
        return f"{self.description}"

    def get_background(self):
        return self.background.get_background()

    def __repr__(self):
        return f"{self.name} (Room)"

