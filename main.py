from modules import Party
from modules import EventHandler
from modules import Exist
from sys import argv, exit


def interact(some_dict, room, eh):
    def is_valid(character):
        if character.isdigit():
            if int(character) in range(len(some_dict.keys())):
                return True
        return False
    
    if not isinstance(some_dict, dict):
        if isinstance(some_dict, str):
            if "end" in some_dict:
                return None
        if some_dict is None:
            return None
        else:
            print(some_dict)
            return None

    if "message" in some_dict:
        print(some_dict["message"])
        some_dict.pop("message")

    if "quit" in some_dict:
        exit()

    if some_dict == {}:
        return None
    
    c = ""
    l = list(some_dict.keys())
    print()
    while not is_valid(c):
        for i, l1 in enumerate(l):
            print(f"{i}) {l1}")
        c = input(">> ")
        if 'q' in c:
            exit()
        if not is_valid(c):
            print("Not valid.")
    choice = some_dict[l[int(c)]]
    if choice["fun"] is not None:
        interact(choice["fun"](*choice["vals"]), room, eh)
    return None


current_place = "Hallway"
party = Party.Party(debug=True)

print("CLI RPG DEMO BY HARRISON HALL")

eh = EventHandler.EventHandler()
Exist.Exist.debug = True
Exist.Exist.start_log()
print("DONE LOADING\n---")


if __name__ == "__main__":
    eh.enter_room(party, current_place)
    while True:
        options = eh.base_interaction(party.room, party)
        interact(options, party.room, eh)
