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
        self.layout_d = pdict.get("layout", {})

    def make_layout(self) -> dict:
        for thing in self.layout_d:
            if "square" in thing:
                p1 = self.layout_d[thing][0]
                p2 = self.layout_d[thing][1]
                for i in range(p1[1], p2[1]+1):
                    for j in range(p1[0], p2[0]+1):
                        if (
                                (i == p1[1] or i == p2[1]) or
                                (j == p1[0] or j == p2[0])
                        ):
                            self.layout[(i,j)] = Text.Text(
                                "█", color="black"
                            )
                            Exist.Exist.class_log("TEST")
            elif "wall" in thing:
                for pos in self.layout_d[thing]:
                    self.layout[
                        (pos[1],pos[0])
                    ] = Text.Text("█", color="black")
            else:
                for pos in self.layout_d[thing]:
                    self.layout[
                        (pos[1], pos[0])
                    ] = self.get_character(thing)
        return self.layout

    def get_character(self, thing):
        if thing in self.new_rooms:
            if thing in self.rooms:
                r = self.rooms[thing]
                return Text.Text(r.single, color=r.color)
            return Text.Text("⊓", color="magenta")
        if thing in self.new_people:
            if thing in self.people:
                p = self.people[thing]
                return Text.Text(p.single, color=p.color)
            return Text.Text("☺", color="black")
        if thing in self.new_things:
            if thing in self.things:
                t = self.things[thing]
                return Text.Text(t.single, color=t.color)
            return Text.Text("&", color="yellow")
        return Text.Text("?", color="cyan")

    def enter(self):
        """return Text for entering room."""
        return f"{self.description}"

    def get_background(self):
        return self.background.get_background()

    def get_mapping(self, h, w, cx, cy):
        self.make_layout()
        m = Text.Text("")
        for i in range(cy-h//2,cy+h//2+1):
            for j in range(cx-w//2,cx+w//2+1):
                if i == cy and j == cx:
                    m.add_message("X","black",space="")
                else:
                    if (i, j) in self.layout:
                        m = m + self.layout.get((i,j))
                    else:
                        m.add_message("·", color=self.color, space="")
        Exist.Exist.class_log(str(m.message))
        return m

    def __repr__(self):
        return f"{self.name} (Room)"

