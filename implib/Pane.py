from modules import Party
from modules import EventHandler
from modules import Exist
from modules import Text
from sys import argv, exit
import curses


class Pane:
    def __init__(
            self, h : int, w : int, y : int, x : int,
            draw_border=True
    ):
        self.draw_border = draw_border
        self.h = h
        self.w = w
        self.y = y
        self.x = x
        self.win = curses.newwin(h,w,y,x)
        self.clear()

    def clear(self) -> None:
        """Clear the buffer."""
        self.buf = [
            [
                [" "] for i in range(self.w)
            ] for j in range(self.h)
        ]
        return None

    def refresh(self) -> None:
        """Refresh the pane on the screen."""
        self.win.clear()
        for i, row in enumerate(self.buf):
            for j, item in enumerate(row):
                #print(f"{self.w} {self.h} {i} {j} '{item[0]}'| ", end="")
                #print(i, j, item[0], 1)
                #print(*[curses.color_pair(t) for t in item[1:]])
                atts = [curses.color_pair(t) for t in item[1:]]
                if len(atts) > 0:
                    try:
                        self.win.addnstr(
                            i, j, item[0], 1, *atts
                        )
                    except Exception:
                        pass
                else:
                    try:
                        self.win.addnstr(
                            i, j, item[0], 1
                        )
                    except Exception:
                        pass
        self.border()
        self.win.refresh()
        return None

    def border(self) -> None:
        """Draw a border around the pane."""
        if not self.draw_border:
            return None
        if self.h == 1:
            for i in list(range(self.w)):
                if i == 0:
                    self.addnstr(0, i, "·")
                elif i == self.w-1:
                    self.addnstr(0, i, "·")
                else:
                    self.addnstr(0, i, " ")
            return None
        for i, row in enumerate(self.buf):
            for j, item in enumerate(row):
                if i in [0, self.h -1]:
                    self.addnstr(i, j, "=")
                if j in [0, self.w -1]:
                    self.addnstr(i, j, "‖")
                if i in [0] and j in [0, self.w-1]:
                    self.addnstr(i, j, "∇")
                if i in [self.h-1] and j in [0, self.w-1]:
                    self.addnstr(i, j, "Δ")
        return None

    def addnstr(
            self,
            i : int,
            j : int,
            char : str,
            length=1,
            *attrs
    ) -> None:
        """Safely add string to pane."""
        if len(attrs) == 0:
            try:
                self.win.addnstr(i, j, char, length)
            except Exception as e:
                pass
        else:
            try:
                self.win.addnstr(i, j, char, length, attrs)
            except Exception as e:
                pass
        return None

    def add(self, text, clear=False) -> None:
        """Generic, text can be Text.Text or str"""
        if clear:
            self.clear()
        if isinstance(text, str):
            self.add_str(text)
        if isinstance(text, Text.Text):
            self.add_textobj(text)
        if self.draw_border:
            self.add_row()
        return None

    def add_str(self, text : str) -> None:
        i = 1 if self.draw_border else 0
        while text != "":
            if text[0] == "\n":
                self.add_row()
                i = 1 if self.draw_border else 0
                text = text[1:]
                continue
            elif i >= self.w - (1 if self.draw_border else 0):
                self.add_row()
                i = 1 if self.draw_border else 0
                continue
            else:
                #print(f"|{len(self.buf)} {i}|",end="")
                self.buf[-1][i] = [text[0]]
            text = text[1:]
            i += 1
        return None

    def add_textobj(self, text : Text.Text) -> None:
        self.add_row()
        i = 1 if self.draw_border else 0
        for character_list in text:
            #Exist.Exist.class_log(str(character_list))
            char = character_list[0]
            attrs = character_list[1:]
            if char == "\n":
                self.add_row()
                i = 1 if self.draw_border else 0
                continue
            elif i >= self.w - (1 if self.draw_border else 0):
                self.add_row()
                i = 1 if self.draw_border else 0
                self.buf[-1][i] = character_list
            else:
                self.buf[-1][i] = character_list
            i += 1
        return None

    def add_row(self) -> None:
        self.buf = self.buf[1:] + [[[" "] for w in range(self.w)]]
        return None

    def add_choices(self, text) -> None:
        return None

    def nodelay(self, flag : bool) -> None:
        """Has to do with getting characters"""
        self.win.nodelay(flag)
        return None
