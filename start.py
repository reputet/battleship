import sys
from pprint import pprint
from time import sleep
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

# enemy_battlefield = EnemyBattleField()
enemy = Enemy()
enemy.make_battlefield()
enemy.make_ships()
#enemy_ships = enemy.make_ships()

#player_battlefield = BattleField()
player = Player()
player.make_battlefield()
player.make_ships()

print(player.battlefield.get_map)
my_turn = ask_yes_no("Would you like to move first?")
if my_turn == "y":
    my_turn = True
else:
    my_turn = False

game_over = None
while not game_over:
    if my_turn:
        game_over = player.fire(enemy)
        if game_over:
            print("\n\nCongratulations, human! You destroyed me..."
                  "I thought it is impossible, but maybe i was wrong...")
            sleep(10)
            print("No! I wasn't wrong!")
            sleep(3)
            print("It is an accident!")
            sleep(3)
            print("You are lucky, human! I'm sure you will never be able to beat me!")
            sleep(4)
            print("ha-ha-ha-ha-ha")
            sleep(3)
            print("HA-HA-HA-HA-HA-HA-HA-HA")
            sleep(2)
    else:
        game_over = enemy.fire(player)
        if game_over:
            print("\n\nHa-ha-ha-ha-ha. You'll never be able to surpass machine intellegence!\n"\
                  "Victory for me!")
            sleep(2)
    my_turn = not my_turn
            
input("\nPress the enter to exit.")


