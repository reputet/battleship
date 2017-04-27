import sys
from pprint import pprint
from classes import Field, BattleField, Ship

##point = Field("A", "5")
##f = BattleField()
##n = Field("A", "1")
##foo = f.mapping["G6"]
##bar = f.mapping["F1"]
##
####for key, value in f.mapping.items():
####	if key not in ("D3", "D4", "D5", "D6", "C4", "E4", "F4"):
####		value.involve()
##
####ships = []
####ships_length = (4, 3, 3, 2, 2, 2, 1, 1, 1, 1)
####for ship_length in ships_length:
####        fields = f.get_random_fields(ship_length)
####        ships.append(Ship(fields, f))
##
##fields = ["B3", "C3", "D3", "E3"]
##f2 = BattleField()
###s2 = Ship(fields, f2)
##ships = Ship.automake_ships(f2)
##f2.get_map()
##
##f3 = BattleField()
##ship = Ship.make_ship(2, f3)

def ask_yes_no(question):        
    """Ask a yes or no question."""
    response = None
    while response not in ("y", "n"):
        response = input(question + " [y/n]: ").lower()
    return response


enemy_battlefield = BattleField()
enemy_ships = Ship.automake_ships(enemy_battlefield)

player_battlefield = BattleField()
first = ask_yes_no("Do you want arrange you ship automatically?")
if first == "y":
    player_ships = Ship.automake_ships(player_battlefield)
else:
    SHIP_LENGTH = (4, 3, 3, 2, 2, 2, 1, 1, 1, 1)
    player_ships = []
    for size in SHIP_LENGTH:
        print(player_battlefield.get_map)
        ship = Ship.make_ship(size, player_battlefield)
        player_ships.append(ship)
print(player_battlefield.get_map)

        
input("\nPress the enter to exit.")


