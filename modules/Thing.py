from modules import Exist

class Thing(Exist.Exist):
    def class_specific(self, pdict):
        return None

    def interact(self, player, room):
        return {
            "Description": {
                "fun": self.do_description,
                "vals": [player, room]
            },
            "Dialogue": {
                "fun": self.do_dialogue,
                "vals": ["start", player, room]
            },
            "Back": {
                "fun": None,
                "vals": []
            }
        }
