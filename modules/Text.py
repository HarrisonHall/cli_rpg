from termcolor import colored
import curses as cs

class Text:
    curses = False
    term = False
    
    def __init__(self, message, color="white"):
        if self.term:
            self.message = colored(message, color)
        else:
            self.message = message
        self.color = color

    def add_message(self, message, color="", space=" "):
        if self.term:
            if color == "":
                color = self.color
            self.message += space + colored(message, color)
            return None
        self.message += space + message
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

    def __str__(self):
        if self.term:
            return self.message
        if self.curses:
            return self.message
        return self.message

    def __repr__(self):
        if self.term:
            return self.message
        if self.curses:
            return self.message
        return self.message
