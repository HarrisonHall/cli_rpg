import datetime

class Logger:
    def __init__(self, f="", title=""):
        if f == "":
            self._f = self.get_file_name()
        else:
            self._f = f

        self._fp = open(self._f, "a")
        
        self.log("x"*50)
        self.log("NEW GAME")
        if title != "":
            self.log(f"TITLE: {title}")
        self.log("x"*50)

    def log(self, message):
        new_message = self.get_time_str() + message.replace("\n","") + "\n"
        self._fp.write(new_message)

    def get_time_str(self):
        return datetime.datetime.now().strftime("%H:%M:%S::")

    def get_file_name(self):
        return "logs/" + datetime.datetime.now().strftime("%d-%m-%y") + ".log"

    def flush(self):
        self._fp.close()
        self._fp.open(self._f, "a")

    def __del__(self):
        self.log("GAME ENDED")
        self._fp.close()
