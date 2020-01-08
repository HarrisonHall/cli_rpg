from modules import Exist

class Item(Exist.Exist):
    def class_specific(self, pdict):
        self.hp = pdict.get("hp", 0)
        self.magic = pdict.get("magic", 0)
        self.usage_message = pdict.get("usage_message", f"{self.name} was used.")

        self.exit_flag = pdict.get("exit", False)

        self.events = pdict.get("events", {})
        self.exists = pdict.get("exists", {
            "start": None
        })
        self.value = pdict.get("value", 1)

    def interact(self, player):
        if self.exit_flag:
            return {
                "quit": True
            }
        player.hp = min(player.hp + self.hp, player.max_hp)
        player.magic += self.magic
        return {
            "message": self.usage_message
        }
