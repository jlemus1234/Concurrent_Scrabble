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

def create_word(word):
    tile_word = []
    for letter in word:
        tile_word.append(Tile(letter))
    return tile_word


class Tile:

    def __init__(self, start_value='', start_score=0, start_multiplier=(1,'w'), start_id=0, tuple_form=''):
        if tuple_form == '':
            self.value      = start_value
            self.score      = self.scores[start_value]
            self.multiplier = start_multiplier
            self.id         = start_id
        else:
            self.value      = tuple_form[0]
            self.score      = tuple_form[1]
            self.multiplier = tuple_form[2]
            self.id         = tuple_form[3]

    def to_tuple(self):
        return (self.value, self.score, self.multiplier, self.id)

    def is_blank(self):
        return self.value == ''


    # equal overloader
    # everything is equal to blank or multiplier
    def __eq__(self, other):
        if self.value == '' or other.value == '':
            return True
        return self.id == other.id

    # not equal overloader
    def __ne__(self, other):
        return not self == other

    scores = {
        # empty string can be used for multiplier spaces
        '' :0,
        # star used for center tile
        '*':0,

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
