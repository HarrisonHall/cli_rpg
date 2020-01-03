# Modules

## `Exist.py`
Most modules are subclasses under `Exist`, as most in-game things 
do in fact exist.

### `Party.py`
A handler for a set of persons with special properties that can 
be controlled by a player.

### `Person.py`
A person.

### `Thing.py`
An inanimate thing.

### `Attack.py`
An attack.

### `Room.py`
A room.

### `Weapon.py`
Weapons.

## `LogLog.py`
A portable logging system.
* Logs are stored in `logs/`, these are ignored by `.gitignore`
* If enabled, logs are called by any 
`<exist-inherited-object>.log(message)`

## `Personality.py`
Handler for a `Person`s personality and how people interact.

## `EventHandler.py`
Handler for events that occur in a story. 
