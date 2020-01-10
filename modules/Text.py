from termcolor import colored
import curses as cs

class Text:
    curses = False
    term = False
    
    def __init__(self, message, color="white"):
        #self.message = colored(message, color)
        self.message = message
        self.color = color

    def add_message(self, message, color="", space=" "):
        self.message += space + message
        return self
        if color == "":
            color = self.color
        self.message += space + colored(self.message, color)
        return self

    @classmethod
    def use_term_color(self):
        self.term = True

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
