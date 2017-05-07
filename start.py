"""Main program"""

import textwrap
from classes import Player, Enemy


def ask_yes_no(question):
    """Ask a yes or no question."""
    response = None
    while response not in ("y", "n"):
        response = input(question + " [y/n]: ").lower()
    return response


def rules_and_agreements():
    """Print out information for player"""
    info = """
    Hello, player!

    It is a well-known game called Battleship or Sea Battle.
    Before start please read the next rules and agreements:

      -Ships in this game can only be linear

      -Ships can not occupy squares next to each other

      -Player's ship part is designated as "X"

      -Player's damaged ship part is designated as "@"

      -Enemy's founded (damaged) ship part is designated as "X"

      -Missed shots is designated as "."

      -To make a shot you have to write letter followed by number (i.e. "d7")

      -To arrange a ship (if manually ship arrangement was
       chosen) you have to write its field names separated by space
       i.e. "a1 a2 a3 a4" (four-funnel) or "h4 h6 h5" (three-funnel) etc.


    Enjoy the game!
    """
    print(textwrap.dedent(info))


def main():
    """Run main program"""
    rules_and_agreements()
    enemy = Enemy()
    enemy.make_battlefield()
    enemy.make_ships()

    player = Player()
    player.make_battlefield()
    player.make_ships()

    print(player.battlefield.get_map)
    my_turn = ask_yes_no("Would you like to move first?")
    if my_turn == "n":
        my_turn = False

    game_over = None
    while not game_over:
        if my_turn:
            game_over = player.fire(enemy)
            if game_over:
                enemy.says_after_losing()
        else:
            game_over = enemy.fire(player)
            if game_over:
                enemy.says_after_victory()
        my_turn = not my_turn

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit.")
