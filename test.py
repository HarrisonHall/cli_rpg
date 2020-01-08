import unittest as ut
from modules import EventHandler
from modules import Party

def basic_interact(some_dict, room, commands):
    if commands is None:
        return some_dict.get("message", "")
    
    if commands == []:
        return some_dict.get("message", "")
    
    if not isinstance(some_dict, dict):
        return commands

    if "message" in some_dict:
        some_dict.pop("message")

    if "quit" in some_dict:
        some_dict.pop("quit")
        return commands

    if some_dict == {}:
        return commands

    l = list(some_dict.keys())
    choice = l[commands[0]]
    commands = commands[1:]
    if some_dict[choice]["fun"] == None:
        return commands
    basic_interact(some_dict[choice]["fun"](*some_dict[choice]["vals"]), room, commands)

class TestImport(ut.TestCase):
    
    def test_import_all(self):
        eh = EventHandler.EventHandler()
        return eh

    def test_party(self):
        party = Party.Party(debug=True)
        start_room = "Hallway"
        party.enter_room(start_room)
        return (party)

    def test_john(self):
        eh = self.test_import_all()
        party = self.test_party()
        
        commands = [0, 0, 0]
        while commands != []:
            interaction = eh.base_interaction(party.room, party)
            commands = basic_interact(interaction, party.room, commands)

    def test_demo(self):
        eh = self.test_import_all()
        party = self.test_party()
        
        commands = [1,2,0,4,3,3,0,2,4,1,1,2,2,3,3,0,2,0,4,3,3,0,1,2]
        while commands != []:
            interaction = eh.base_interaction(party.room, party)
            commands = basic_interact(interaction, party.room, commands)
            if isinstance(commands, str):
                print(commands)
                break

if __name__ == "__main__":
    ut.main()
