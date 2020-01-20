from modules import Exist
from modules import Background
from modules import Text

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

        self.layout = {}

    def make_layout(self):
        for t, d in zip([self.new_rooms],[Exist.Exist.rooms]):
            for O in t:
                if O in d:
                    self.layout[
                        (d[O].xpos, d[O].ypos)
                    ] = Text.Text(d[O].single, color=d[O].color)
        return None

    def enter(self):
        """return Text for entering room."""
        return f"{self.description}"

    def get_background(self):
        return self.background.get_background()

    def get_mapping(self, h, w, cx, cy):
        self.make_layout
        m = Text.Text("")
        for i in range(cy-h//2,cy+h//2+1):
            for j in range(cx-w//2,cx+w//2+1):
                if i == cy and j == cx:
                    m.add_message("X","black",space="")
                else:
                    if (i, j) in self.layout:
                        m = m + self.layout.get((i,j))
                    else:
                        m.add_message("·", space="")
        Exist.Exist.class_log(str(m.message))
        return m

    def __repr__(self):
        return f"{self.name} (Room)"

