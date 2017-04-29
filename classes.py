"""Module with classes to make players, fields, battlefields, ships"""

import sys
from random import choice
from collections import OrderedDict
from time import sleep


class Field(object):
    """A playing field."""
    LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    NUMBERS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

    def __init__(self, letter, number):
        self.letter = letter
        self.number = number
        self.name = letter+number
        self.ship = None
        self.shot = False
        self.free = True
        self.part_of_ship = False

    def __str__(self):
        if self.shot and self.part_of_ship:
            return "@"
        elif self.shot:
            return "."
        elif self.part_of_ship:
            return "X"
        else:
            return " "

    def __repr__(self):
        return self.name

    def to_shoot(self):
        """Make a shot to this field"""
        if self.shot:
            return "already shot"
        self.shot = True
        if self.part_of_ship:
            self.ship.live_parts.remove(self)
            return True
        #battlefield.shot.append(self)

    def involve(self):
        """Make this field involve that means that it is not possible
           to stand there ships"""
        self.free = False

    @property
    def is_free(self):
        return self.free

    @property
    def is_shot(self):
        return self.shot

    @property
    def is_part_of_ship(self):
        return self.part_of_ship

class EnemyField(Field):
    def __str__(self):
        if self.shot:
            if self.part_of_ship:
                return "X"
            return "."
        return " "

class BattleField(object):
    """A battlefield with fields and ships"""

    ROW_LENGTH = 10
    COLUMN_LENGTH = 10

    def __init__(self):
        self.fields = []
        self.matrix = []
        self.mapping = OrderedDict()
        self.shot = []

        for count, number in enumerate(Field.NUMBERS):
            self.matrix.append(list())
            for letter in Field.LETTERS:
                new_field = Field(letter, number)
                self.matrix[count].append(new_field)
                new_field.y = len(self.matrix) - 1
                new_field.x = len(self.matrix[count]) - 1
                self.mapping.update({new_field.name:new_field})
                self.fields.append(new_field)

    def __str__(self):
        return self.get_map

    def __repr__(self):
        return self.get_map

    @property
    def get_map(self):
        drew_map = """
           Player's battlefield            

    A   B   C   D   E   F   G   H   I   J  
  +---+---+---+---+---+---+---+---+---+---+
 1| {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |
  +---+---+---+---+---+---+---+---+---+---+
 2| {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |
  +---+---+---+---+---+---+---+---+---+---+
 3| {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |
  +---+---+---+---+---+---+---+---+---+---+
 4| {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |
  +---+---+---+---+---+---+---+---+---+---+
 5| {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |
  +---+---+---+---+---+---+---+---+---+---+
 6| {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |
  +---+---+---+---+---+---+---+---+---+---+
 7| {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |
  +---+---+---+---+---+---+---+---+---+---+
 8| {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |
  +---+---+---+---+---+---+---+---+---+---+
 9| {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |
  +---+---+---+---+---+---+---+---+---+---+
10| {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |
  +---+---+---+---+---+---+---+---+---+---+
  """.format(*self.mapping.values())
        return drew_map

    def get_halo(self, field):
        range_y = (field.y - 1, field.y, field.y + 1)
        range_x = (field.x - 1, field.x, field.x + 1)
        halo = [self.matrix[y][x] for y in range_y for x in range_x\
                     if x in range(10) and y in range(10)]
        return halo

    def get_random_fields(self, ship_size):

##        ROW_LENGTH = 10
##        COLUMN_LENGTH = 10
        ship_fields = []
        while len(ship_fields) < ship_size:
            horizontal_ship = choice((True, False))
            if horizontal_ship:
                row_number = choice(range(self.COLUMN_LENGTH))
                row = self.matrix[row_number]
                ship_head = choice(row[:-ship_size]).x
                ship_tail = ship_head + ship_size
                ship = row[ship_head:ship_tail]
                ship_fields = [ship_field for ship_field in ship if ship_field.is_free]
            else:
                column_number = choice(range(self.ROW_LENGTH))
                column = [row[column_number] for row in self.matrix]
                ship_head = choice(column[:-ship_size]).y
                ship_tail = ship_head + ship_size
                ship = column[ship_head:ship_tail]
                ship_fields = [ship_field for ship_field in ship if ship_field.is_free]

        return ship_fields

class EnemyBattleField(BattleField):
    """Enemy's battlefield with fields and ships"""

    def __init__(self):
        self.fields = []
        self.matrix = []
        self.mapping = OrderedDict()
        self.shot = []

        for count, number in enumerate(EnemyField.NUMBERS):
            self.matrix.append(list())
            for letter in EnemyField.LETTERS:
                new_field = EnemyField(letter, number)
                self.matrix[count].append(new_field)
                new_field.y = len(self.matrix) - 1
                new_field.x = len(self.matrix[count]) - 1
                self.mapping.update({new_field.name:new_field})
                self.fields.append(new_field)

    @property
    def get_map(self):
        return super().get_map.replace("Player's battlefield", "Enemy's battlefield")

class Ship(object):

    SHIP_LENGTH = (4, 3, 3, 2, 2, 2, 1, 1, 1, 1)

    def __init__(self, ship_fields, battlefield):
        self.parts = [battlefield.mapping[field] for field in ship_fields]
        self.size = len(self.parts)
        for field in self.parts:
            field.part_of_ship = True
            field.ship = self
        for name in self.parts:
            halo = battlefield.get_halo(name)
            for field in halo:
                field.involve()
        self.live_parts = list(self.parts)

    def __str__(self):
        return str(self.parts)

    def __repr__(self):
        return str(self.parts)

    @property
    def is_alive(self):
        return bool(self.live_parts)

    @classmethod
    def automake_ships(cls, battlefield):
        ships = []
        for size in cls.SHIP_LENGTH:
            fields = [field.name for field in battlefield.get_random_fields(size)]
            ships.append(cls(fields, battlefield))
        return ships

    @classmethod
    def make_ship(cls, ship_size, battlefield):
        while True:
            try:
                if ship_size == 1:
                    ship_fields = input(
                        "Enter cell number for your single-funnel ship:\n"
                        .format(ship_size)).upper()
                else:
                    ship_fields = input(
                        "Enter {0} cell numbers separated by space for your {0}-funnel ship:\n"
                        .format(ship_size)).upper()
                print()
                ship_fields = ship_fields.split(" ")
                ship_fields.sort()
                if len(ship_fields) != ship_size:
                    print("Your ship must consist of {} fields but you typed {}"
                          .format(ship_size, len(ship_fields)))
                    continue
                parts = [battlefield.mapping[field] for field in ship_fields]
            except KeyboardInterrupt:
                print("KeyboardInterrupt. System exit!")
                sys.exit()
            except KeyError:
                print("Invalid names. Try again")
                continue
            is_fields_free = set()
            ship_letters = ""
            ship_numbers = ""
            for part in parts:
                ship_letters += part.letter
                ship_numbers += part.number
                is_fields_free.add(part.is_free)
            if (ship_numbers not in "12345678910" and ship_letters not in "ABCDEFGHIJ")\
                or (ship_numbers.count(ship_numbers[0]) != len(ship_numbers)\
                and ship_letters.count(ship_letters[0]) != len(ship_letters)):
                print("You ship must be continuous!")
                continue
            elif False in is_fields_free:
                print("You can not use this fields. They are involved. Choose other fields")
            else:
                break
        ship = cls(ship_fields, battlefield)
        return ship

class Player(object):
    def __init__(self):
        self.battlefield = None
        self.ships = None

    def make_battlefield(self):
        self.battlefield = BattleField()

    def make_ships(self):
        make_ships_automatically = Player.ask_yes_no("Do you want arrange you ships automatically?")
        if make_ships_automatically == "y":
            player_ships = Ship.automake_ships(self.battlefield)
        else:
            player_ships = []
            for size in Ship.SHIP_LENGTH:
                print(self.battlefield.get_map)
                ship = Ship.make_ship(size, self.battlefield)
                player_ships.append(ship)
        self.ships = player_ships

    @staticmethod
    def shoot_near_drowned_ship(battlefield, last_field):
        halo = set()
        ship = last_field.ship.parts
        for field in ship:
            field_halo = battlefield.get_halo(field)
            for cell in field_halo:
                halo.add(cell)
        for field in halo:
            field.to_shoot()

    def fire(self, opponent):
        shoot = True
        while shoot:
##            victory = opponent.is_checkmate()
##            if victory:
##                return True
            print(self.join_maps(opponent.battlefield))
            while True:
                try:
                    target = input("Enter a field name to fire: ").upper()
                    field = opponent.battlefield.mapping[target]
                    break
                except KeyError:
                    print("Invalid field name. Try again")
                except KeyboardInterrupt:
                    print("KeyboardInterrupt. System exit!")
                    sys.exit()
            print()
            shoot = field.to_shoot()
            if shoot:
                if shoot == "already shot":
                    print("You have already shot to that field ({}). "
                          "Choose another field".format(field.name))
                elif field.ship.is_alive:
##                    print(self.join_maps(opponent.battlefield))
                    print("Got it!")
                else:
                    self.shoot_near_drowned_ship(opponent.battlefield, field)
                    print("Ship is crushed!")
                    victory = opponent.is_checkmate()
                    if victory:
                        return True
                print("Your move again!")
                input("Press Enter to continue...")
            else:
                print("Missed!")

    def is_checkmate(self):
        still_live = {ship.is_alive for ship in self.ships}
        if not True in still_live:
            return True

    def join_maps(self, opponent_battlefield):
        splitted_map_self = self.battlefield.get_map.split("\n")
        splitted_map_opponent = opponent_battlefield.get_map.split("\n")

        new_map = ""
        for self_line, opponent_line in zip(splitted_map_self, splitted_map_opponent):
            new_map += self_line + "      " + opponent_line + "\n"

        return new_map

    @staticmethod
    def ask_yes_no(question):
        """Ask a yes or no question."""
        response = None
        while response not in ("y", "n"):
            response = input(question + " [y/n]: ").lower()
        return response

class Enemy(Player):

    def make_ships(self):
        self.ships = Ship.automake_ships(self.battlefield)

    def make_battlefield(self):
        self.battlefield = EnemyBattleField()

    def fire(self, opponent):
        shoot = True
        while shoot:
            victory = opponent.is_checkmate()
            if victory:
                return True
            input("Enemy's move\nPress Enter to continue...\n")
            field = self.choose_field_to_shoot(opponent.battlefield)
            print("I'll try to shoot to {}".format(field.name))
            shoot = field.to_shoot()
            sleep(3)
            if shoot:
##                if shoot == "already shot":
##                    print("You have already shot to that field. Choose another field")
                if field.ship.is_alive:
                    print("Got it!")
                else:
                    print("Ship is crushed!")
                    self.shoot_near_drowned_ship(opponent.battlefield, field)
                print("My move again!")
            else:
                print("Missed!")
            input("Press Enter to continue...\n")

##    def fire(self, battlefield):
##        shoot = True
##        while shoot:
##            input("Enemy's move")
##            field = self.choose_field_to_shoot(battlefield)
##            print("I'l try to shoot to {}".format(field.name))
##            shoot = field.to_shoot()
##            if shoot:
##                if shoot == "already shot":
##                    print("You have already shot to that field. Choose another field")
##                elif field.ship.is_alive:
##                    print("Got it!")
##                else:
##                    print("Ship is crushed!")
##                print("Your move again!")
##            else:
##                print("Missed!")
    @staticmethod
    def choose_field_to_shoot(battlefield):
        free_fields = list(filter(lambda field: not field.is_shot, battlefield.fields))
        field = choice(free_fields)
        return field
