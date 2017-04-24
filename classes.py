class Field(object):
    """A playing field."""
    LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    NUMBERS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    
##    for x, letter in enumerate(Field.LETTERS, 1):
##            for y, number in enumerate(Field.NUMBERS, 1):
##                if 

    
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

    def shoot(self):
        """Make a shot to this field"""
        self.shot = True

    def involve(self):
        """Make this field involve that means that it is not possible
           to stand there ships"""
        self.free = False

    def give_halo(self):
        pass        

    @property
    def is_free(self):
        return self.free
        
    @property
    def is_shot(self):
        return self.shot
        

class BattleField(object):
    """A battlefield with ships"""
    # HORIZONTAL = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    # VERTICAL = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    
##    ANGULAR_FIELDS = ("A1", "A10", "J1", "J10")
##    SIDE_FIELDS = ("A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9",
##                   "J2", "J3", "J4", "J5", "J6", "J7", "J8", "J9",
##                   "B1", "C1", "D1", "E1", "F1", "G1", "H1", "I1",
##                   "B10", "C10", "D10", "E10", "F10", "G10", "H10", "I10")
                
##    def get_angular_fields(self, matrix):
##        angular_fields = self.matrix[0][0] + self.matrix[0][9] + self.matrix[9][0] + self.martix[9][9]

    def __init__(self):
        self.fields = []
        self.matrix = []
##        self.angular_fields = []
##        self.side_fields = []
        self.mapping = {}

##        for letter in Field.LETTERS:
##            for number in Field.NUMBERS:
##                self.fields.append(Field(letter, number))
                
        for count, number in enumerate(Field.NUMBERS):
            self.matrix.append(list())
            for letter in Field.LETTERS:
                new_field = Field(letter, number)
                self.matrix[count].append(new_field)
                new_field.y = len(self.matrix) - 1
                new_field.x = len(self.matrix[count]) - 1
                self.mapping.update({new_field.name:new_field})

##                if new_field.name in BattleField.ANGULAR_FIELDS:
##                    self.angular_fields.append(new_field)
##                elif new_field.name in BattleField.SIDE_FIELDS:
##                    self.side_fields.append(new_field)
    
    def get_halo(self, field):
        range_y = (field.y - 1, field.y, field.y + 1)
        range_x = (field.x - 1, field.x, field.x + 1)
        
        self.halo = [self.matrix[y][x] for y in range_y for x in range_x\
                     if x in range(10) and y in range(10)]

        
##        for index_y in (field.y - 1, field.y, field.y + 1):
##            for index_x in (field.x - 1, field.x, field.x + 1):
##                if index_y not in range(10) or index_x not in range(10):
##                    pass
##                else:
##                    self.halo.append(self.matrix[index_y][index_x])
        return self.halo
        
    

class Ship(object):
    def __init__(self, ship_fields, battlefield):
        self.fields = fields
        self.size = len(fields)







