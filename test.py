import sys
from pprint import pprint
from classes import Field, EnemyField, BattleField, EnemyBattleField, Ship, Player, Enemy

SHIP_LENGTH = (4, 3, 3, 2, 2, 2, 1, 1, 1, 1)

def ask_yes_no(question):        
    """Ask a yes or no question."""
    response = None
    while response not in ("y", "n"):
        response = input(question + " [y/n]: ").lower()
    return response

##def player_fire(battlefield):
##    shoot = True
##    while shoot:
##        # try
##        print(enemy_battlefield)
##        target = input("Enter cell number to fire: ").upper()
##        field = enemy_battlefield.mapping[target]
##        shoot = field.to_shoot()
##        if shoot:
##            if shoot == "already shot":
##                print("You have already shot to that field. Choose another field")
##            elif field.ship.is_alive:
##                print("Got it!")
##            else:
##                print("Ship is crushed!")
##            print("Your move again!")
##        else:
##            print("Missed!")

def enemy_fire(battlefield):
    shoot = True
    while shoot:
        input("Enemy's move")
        field = battlefield.get_random_fields(1)[0]
        print("I'l try to shoot to {}".format(field.name))
##        field = enemy_battlefield.mapping[target]
        shoot = field.to_shoot()
        if shoot:
            if shoot == "already shot":
                print("You have already shot to that field. Choose another field")
            elif field.ship.is_alive:
                print("Got it!")
            else:
                print("Ship is crushed!")
            print("Your move again!")
        else:
            print("Missed!")

enemy_battlefield = EnemyBattleField()
enemy = Enemy(enemy_battlefield)
enemy_ships = enemy.make_ships()

player_battlefield = BattleField()
player = Player(player_battlefield)
player_ships = player.make_ships()

print(player_battlefield.get_map)
print("Enemy")
for i in enemy_ships:
    print(i.parts)
my_turn = ask_yes_no("Would you like to move first?")
if my_turn == "y":
    my_turn = True
else:
    my_turn = False

game_over = None
while not game_over:
    if my_turn:
        player.fire(enemy_battlefield)
        live_parts = {ship.is_alive for ship in enemy_ships}
        if not any(live_parts):
            game_over = True    
    else:
        enemy.fire(player_battlefield)
        live_parts = {ship.is_alive for ship in player_ships}
        if not any(live_parts):
            game_over = True
            
    my_turn = not my_turn
            
input("\nPress the enter to exit.")


