# Modules
## `Exist.py`
Most modules are subclasses under `Exist`, as most in-game things do in fact exist.
### `Player.py` -> `Party.py`
Player is a placeholder for what a party will eventually be. Parties will be 
a set of multiple `Person`s and how that is handled.
### `Person.py`
A person.
### `Thing.py`
An inanimate thing.
### `Attack.py`
An attack.
### `Room.py`
A room.
## `LogLog.py`
A portable logging system.
* Logs are stored in `logs/`, these are ignored by `.gitignore`
* If enabled, logs are called by any `<exist-inherited-object>.log(message)`
## `Personality.py`
Handler for a `Person`s personality and how people interact.

