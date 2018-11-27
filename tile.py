# Tile Class in Python

# This class contains 3 different constructors
# 1. a default constructor that takes nothing
# 2. one that takes all elements
# 3. one that takes everything but the corresponding score which the class will
#   calculate itself

# The class will have 4 varialbes
# value -> the charater representing the letter (capital letter)
# score -> how many points it is worth
# multiplier -> a tuple, (multiplier_amount, type of multiplier)
#               type of multiplier is a char, 'w' for word, 'l' for letter
# id -> a unique identifier given to each tile (must be set by client)

class tile:

    scores = {
        # empty string can be used for multiplier spaces
        '' :0,

        'E':1,
        'A':1,
        'I':1,
        'O':1,
        'N':1,
        'R':1,
        'T':1,
        'L':1,
        'S':1,
        'U':1,

        'D':2,
        'G':2,

        'B':3,
        'C':3,
        'M':3,
        'P':3,

        'F':4,
        'H':4,
        'V':4,
        'W':4,
        'Y':4,

        'K':5,

        'J':8,
        'X':8,

        'Q':10,
        'Z':10
    }

    def __init__(self):
        self.value =  ''
        self.score = 0
        self.multiplier = (1,'w')
        self.id = 0

    def __init__(self, start_value, start_score, start_multiplier, start_id):
        self.value = start_value
        self.score = new_score
        self.multiplier = start_multiplier
        self.id = start_id

    def __init__(self,start_value, start_multiplier,start_id):
        self.value = start_value
        self.score = scores[value]
        self.multiplier = start_multiplier
        self.id = start_id
