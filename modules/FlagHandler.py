from modules.rep import Flag

class FlagHandler:
    def __init__(self, flags):
        self._flags = {}
        for flag in flags:
            self.add_flag(flag, flags[flag])

    def add_flag(self, name, value):
        f = Flag.Flag(name, value)
        self._flags[f.name] = f

    def check_flag(self, flag):
        if flag in self._flags:
            return True
        return False

    def check_value(self, flag):
        if self.check_flag(flag):
            return self._flags[flag]
        return None

    def remove_flag(self, flag):
        if flag in self._flags:
            f = self._flags.pop(flag)
            del f
        return None

    def similar_flags(self, other_flags):
        return set(self._flags) & set(other_flags)

    def __repr__(self):
        return str(self._flags)
