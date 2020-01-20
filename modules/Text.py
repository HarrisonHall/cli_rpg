from termcolor import colored
import curses as cs

class Text:
    curses = False
    term = False
    
    def __init__(self, message, color="white"):
        self.color = color
        self.message = []
        self.add_message(message, space="")

    def add_message(self, message, color="", space=" "):
        if message == "":
            return
        if self.term:
            if color == "":
                color = self.color
            if space != "":
                self.message.append([space])
            self.message.append([colored(message, color)])
            return None
        if self.curses:
            if color == "":
                color = self.color
            if space != "":
                self.message.append([space])
            self.message.append([message, self.ccolor(color)])
            return None
        if space != "":
            self.message.append([space])
        self.message.append([message])
        return None

    def add_listolists(self, listolists):
        if self.term or self.curses:
            for row in listolists:
                for pixel in row:
                    c = pixel[1]
                    self.add_message(
                        pixel[0], color=c, space=""
                    )
                self.add_message("\n", space="")
        return None

    @classmethod
    def use_term_color(self):
        self.term = True

    @classmethod
    def use_curses_color(self):
        self.curses = True

    def ccolor(self, color):
        return {
            "black": cs.COLOR_BLACK,
            "white": cs.COLOR_WHITE,
            "blue": cs.COLOR_BLUE,
            "cyan": cs.COLOR_CYAN,
            "green": cs.COLOR_GREEN,
            "red": cs.COLOR_RED,
            "magenta": cs.COLOR_MAGENTA,
            "yellow": cs.COLOR_YELLOW,
        }.get(color.lower(), cs.COLOR_WHITE)

    def __str__(self):
        mess = ""
        for l in self.message:
            mess += l[0]
        return mess

    def __repr__(self):
        if self.curses:
            return self.message
        mess = ""
        for l in self.message:
            mess += l[0]
        return mess

    def __getitem__(self, position):
        return self.message[position]
