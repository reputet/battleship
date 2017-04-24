class Field(object):
    """A playing field."""
    LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    NUMBERS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    
    def __init__(self, letter, number):
        self.letter = letter
        self.number = number
        self.name = letter+number
        self.shot = False
        self.free = True

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def to_shoot(self, battlefield):
        """Make a shot to this field"""
        self.shot = True
        battlefield.shot.append(self)

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
        

class BattleField(object):
    """A battlefield with ships"""

    def __init__(self):
        self.fields = []
        self.matrix = []
        self.mapping = {}
        self.shot = []
                
        for count, number in enumerate(Field.NUMBERS):
            self.matrix.append(list())
            for letter in Field.LETTERS:
                new_field = Field(letter, number)
                self.matrix[count].append(new_field)
                new_field.y = len(self.matrix) - 1
                new_field.x = len(self.matrix[count]) - 1
                self.mapping.update({new_field.name:new_field})

    def get_halo(self, field):
        range_y = (field.y - 1, field.y, field.y + 1)
        range_x = (field.x - 1, field.x, field.x + 1)
        self.halo = [self.matrix[y][x] for y in range_y for x in range_x\
                     if x in range(10) and y in range(10)]
        return self.halo

    def get_random_fields(self, ship_size):
        from random import choice

        ROW_LENGTH = 10
        COLUMN_LENGTH = 10
        ship_fields = []
        while len(ship_fields) < ship_size:
            horizontal_ship = choice((True, False))
            if horizontal_ship:
                row_number = choice(range(COLUMN_LENGTH))
                row = self.matrix[row_number]
                ship_head = choice(row[:-ship_size]).x
                ship_tail = ship_head + ship_size
                ship = row[ship_head:ship_tail]
                ship_fields = [ship_field for ship_field in ship if ship_field.is_free]
            else:
                column_number = choice(range(ROW_LENGTH))
                column = [row[column_number] for row in self.matrix]
                ship_head = choice(column[:-ship_size]).y
                ship_tail = ship_head + ship_size
                ship = column[ship_head:ship_tail]
                ship_fields = [ship_field for ship_field in ship if ship_field.is_free]
                
        return ship_fields

            

    #def make_ship(self, ship_fields):
        

class Ship(object):
    def __init__(self, ship_fields, battlefield):
        self.fields = fields
        self.size = len(fields)

    @classmethod
    def make_ships(cls):
        ship_length = (4, 3, 3, 2, 2, 2, 1, 1, 1, 1)
        















        







