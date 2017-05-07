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
        self.x_position = None
        self.y_position = None
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

    def involve(self):
        """Make this field involve that means that it is not possible
           to stand there ships"""
        self.free = False

    @property
    def is_free(self):
        """Check if you could use this field to arrange a ship"""
        return self.free

    @property
    def is_shot(self):
        """Check if the field is shot"""
        return self.shot

    @property
    def is_part_of_ship(self):
        """Check if the field is part of some ship"""
        return self.part_of_ship


class EnemyField(Field):
    """A field that used for enemy purposes"""
    def __str__(self):
        if self.shot:
            if self.part_of_ship:
                return "X"
            return "."
        return " "


class BattleField(object):
    """A player's battlefield with fields and ships"""

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
                new_field.y_position = len(self.matrix) - 1
                new_field.x_position = len(self.matrix[count]) - 1
                self.mapping.update({new_field.name: new_field})
                self.fields.append(new_field)

    def __str__(self):
        return self.get_map

    def __repr__(self):
        return self.get_map

    @property
    def get_map(self):
        """Return battlefield in ASCII presentation to print"""
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
        """Return all fields around given"""
        range_y =\
            (field.y_position - 1, field.y_position, field.y_position + 1)
        range_x =\
            (field.x_position - 1, field.x_position, field.x_position + 1)
        halo = [self.matrix[y][x] for y in range_y for x in range_x
                if x in range(10) and y in range(10)]
        return halo

    def get_random_fields(self, ship_size):
        """Return list of random fields that are free to arrange ships"""
        ship_fields = []
        while len(ship_fields) < ship_size:
            horizontal_ship = choice((True, False))
            if horizontal_ship:
                row_number = choice(range(self.COLUMN_LENGTH))
                row = self.matrix[row_number]
                ship_head = choice(row[:-ship_size]).x_position
                ship_tail = ship_head + ship_size
                ship = row[ship_head:ship_tail]
                ship_fields = [ship_field for ship_field
                               in ship if ship_field.is_free]
            else:
                column_number = choice(range(self.ROW_LENGTH))
                column = [row[column_number] for row in self.matrix]
                ship_head = choice(column[:-ship_size]).y_position
                ship_tail = ship_head + ship_size
                ship = column[ship_head:ship_tail]
                ship_fields = [ship_field for ship_field
                               in ship if ship_field.is_free]

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
                new_field.y_position = len(self.matrix) - 1
                new_field.x_position = len(self.matrix[count]) - 1
                self.mapping.update({new_field.name: new_field})
                self.fields.append(new_field)

    @property
    def get_map(self):
        return super().get_map.replace("Player's battlefield",
                                       "Enemy's battlefield")


class Ship(object):
    """A ship that consist of fields"""
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
        """Check if the ship still have at lest one live (no shot) field"""
        return bool(self.live_parts)

    @classmethod
    def automake_ships(cls, battlefield):
        """Automatically arrange all ships"""
        ships = []
        for size in cls.SHIP_LENGTH:
            fields = [field.name for field
                      in battlefield.get_random_fields(size)]
            ships.append(cls(fields, battlefield))
        return ships

    @classmethod
    def make_ship(cls, ship_size, battlefield):
        """Arrangement of ship manually"""
        while True:
            try:
                if ship_size == 1:
                    ship_fields = input(
                        "Enter cell number for your single-funnel ship:\n"
                        .format(ship_size)).upper()
                else:
                    ship_fields = input(
                        "Enter {0} cell numbers separated by space"
                        "for your {0}-funnel ship:\n"
                        .format(ship_size)).upper()
                print()
                ship_fields = ship_fields.split(" ")
                ship_fields.sort()
                if len(ship_fields) != ship_size:
                    print("Your ship must consist of"
                          "{} fields but you typed {}"
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
            if ((ship_numbers not in "12345678910" and
                ship_letters not in "ABCDEFGHIJ") or
                (ship_numbers.count(ship_numbers[0]) != len(ship_numbers) and
                ship_letters.count(ship_letters[0]) != len(ship_letters))):
                print("You ship must be continuous!")
                continue
            elif False in is_fields_free:
                print("You can not use this fields."
                      "They are involved. Choose other fields")
            else:
                break
        ship = cls(ship_fields, battlefield)
        return ship


class Player(object):
    """A player (human)"""
    def __init__(self):
        self.battlefield = None
        self.ships = None

    def make_battlefield(self):
        """Make player's battlefield"""
        self.battlefield = BattleField()

    def make_ships(self):
        """Offer to arrange ships automatically or manually"""
        make_ships_automatically = \
            Player.ask_yes_no("Do you want to arrange "
                              "you ships automatically?")
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
        """Make shots near all part of ship when it sank"""
        halo = set()
        ship = last_field.ship.parts
        for field in ship:
            field_halo = battlefield.get_halo(field)
            for cell in field_halo:
                halo.add(cell)
        for field in halo:
            field.to_shoot()

    def fire(self, opponent):
        """Make a shot to the field by Player"""
        shoot = True
        while shoot:
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
        """Check if player or enemy (self) was defeated (all ships sank)"""
        still_live = {ship.is_alive for ship in self.ships}
        if True not in still_live:
            return True

    def join_maps(self, opponent_battlefield):
        """Return Player's map and Enemy's map in printable format"""
        splitted_map_self = self.battlefield.get_map.split("\n")
        splitted_map_opponent = opponent_battlefield.get_map.split("\n")

        new_map = ""
        for self_line, opponent_line in zip(splitted_map_self,
                                            splitted_map_opponent):
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
    """An Enemy"""

    def make_ships(self):
        """Automatically arrange Enemy's ships"""
        self.ships = Ship.automake_ships(self.battlefield)

    def make_battlefield(self):
        """Make Enemy's battlefield"""
        self.battlefield = EnemyBattleField()

    def fire(self, opponent):
        """Make a shot to the field by Enemy"""
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
                if field.ship.is_alive:
                    print("Got it!")
                else:
                    print("Ship is crushed!")
                    self.shoot_near_drowned_ship(opponent.battlefield, field)
                print("My move again!")
            else:
                print("Missed!")
            input("Press Enter to continue...\n")

    @staticmethod
    def choose_field_to_shoot(battlefield):
        """Get random valid field for Enemy's fire"""
        free_fields = list(filter(lambda field: not field.is_shot,
                                  battlefield.fields))
        field = choice(free_fields)
        return field

    @staticmethod
    def says_after_losing():
        """The last words of the enemy after losing to player"""
        print("\n\nCongratulations, human! You destroyed me..."
              "I thought it is impossible, but maybe I was wrong...")
        sleep(10)
        print("No! i wasn't wrong!")
        sleep(3)
        print("It is an accident!")
        sleep(3)
        print("You are lucky, human! "
              "I'm sure you will never be able to beat me again!")
        sleep(4)
        print("ha-ha-ha-ha-ha")
        sleep(3)
        print("HA-HA-HA-HA-HA-HA-HA-HA-HA-HA")
        sleep(2)

    @staticmethod
    def says_after_victory():
        """The last words of the enemy after the victory over player"""
        print("\n\nHa-ha-ha-ha-ha. "
              "You'll never be able to surpass machine intellegence!\n"
              "Victory for me!")
        sleep(2)
