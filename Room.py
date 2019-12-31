import Exist

class Room(Exist.Exist):
    def class_specific(self, pdict={}):
        self.new_rooms = pdict.get("new_rooms", {})

        self.new_people = pdict.get("people", {})
        self.new_things = pdict.get("things", {})

    def enter(self):
        return f"{self.description}"

    def __repr__(self):
        return f"{self.name} (Room)"

