class Event:
    """
    Implicit quest that has a set of requirements and
    variables to deterime what happens when it occurs.
    """
    def __init__(self, pdict={}):
        for key in pdict:
            self.name = key
            pdict = pdict[self.name]
            break
        self.requirements = pdict.get(
            "requirements",
            {
                "flags": [],
                "inventory": [],
                "party": [],
                "room": ""
            }
        )
        self.occurance = pdict.get(
            "occurance",
            {
                "dialogue": [],
                "goto_room": "",
                "get_items": {
                    
                },
                "remove_items": {
                    
                },
                "completed_flags": {}
            }
        )
        self.complete = False

    def interact(self, party, room):
        message = ""
        for sentence in self.occurance.get("dialogue", []):
            message += sentence + "\n"
        if "goto_room" in self.occurance:
            party.enter_room(self.occurance.get("goto_room"))
        for item in self.occurance.get("get_items", {}):
            amount = self.occurance["get_items"][item]
            party.current_player.add_item(item, amount)
        for item in self.occurance.get("remove_items", {}):
            amount = self.occurance["remove_items"][item]
            party.current_player.remove_item(item, amount)
        for flag in self.occurance.get("completed_flags", {}):
            val = self.occurance["completed_flags"][flag]
            party.add_flag(flag, val)
        return {
            "message": message
        }

    def requirements_met(self, party, room):
        if self.complete:
            return True
        # Not met yet
        for flag in self.requirements.get("flags", {}):
            if flag not in party.get_flags():
                return False
        for item in self.requirements.get("inventory", {}):
            if item in party.get_inventory():
                if self.requirements["inventory"][item] < party.get_inventory()[item]:
                    return False
            else:
                return False
        for member in self.requirements.get("party", {}):
            if member not in [name for m in party.players]:
                return False
        room = self.requirements.get("room", "")
        if room != "":
            if party.room != self.requirements["room"]:
                return False

        # Now met, now complete
        self.complete = True
        cf = self.occurance.get("completed_flags", {})
        for flag in cf:
            party.add_flag(flag, cf[flag])
        return True
