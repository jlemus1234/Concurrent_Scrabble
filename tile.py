# Tile Class in Python

# The class will have 4 variables
# value -> the charater representing the letter (capital letter)
# score -> how many points it is worth
# multiplier -> a tuple, (multiplier_amount, type of multiplier)
#               type of multiplier is a char, 'w' for word, 'l' for letter
# id -> a unique identifier given to each tile (must be set by client)

# Convert string word to an array of Tiles
def string_to_tiles(word):
    tile_word = []
    for letter in word:
        tile_word.append(Tile(letter))
    return tile_word

# Convert an array of Tiles to a string
def tiles_to_string(tile_word):
    word = ""
    for letter in tile_word:
        word += letter.value
    return word


class Tile:
    def __init__(self, start_value='', start_score=0, start_multiplier=(1,'w'),
                 start_id=0, tuple_form=''):
        if tuple_form == '':
            self.value      = start_value
            self.score      = self.scores[start_value]
            # Multiplier is a tuple where position 0 holds the multiplier value
            # and position 1 holds whether to multiply by word score (w) or 
            # letter score (l)
            self.multiplier = start_multiplier
            self.id         = start_id
        else:
            self.value      = tuple_form[0]
            self.score      = tuple_form[1]
            self.multiplier = tuple_form[2]
            self.id         = tuple_form[3]

    # Convert Tile object to tuple so that it can be passed in Erport
    def to_tuple(self):
        return (self.value, self.score, self.multiplier, self.id)

    # Checks if tile value is blank 
    def is_blank(self):
        return self.value == ''


    # equal overloader. Equal if everything blank or if ID and value match
    def __eq__(self, other):
        if self.value == '' or other.value == '':
            return True
        return self.id == other.id and self.value == other.value

    # not equal overloader
    def __ne__(self, other):
        return not self == other

    scores = {
        # empty string can be used for multiplier spaces
        '' :0,
        # star used for center tile
        '*':0,

        'e':1,
        'a':1,
        'i':1,
        'o':1,
        'n':1,
        'r':1,
        't':1,
        'l':1,
        's':1,
        'u':1,

        'd':2,
        'g':2,

        'b':3,
        'c':3,
        'm':3,
        'p':3,

        'f':4,
        'h':4,
        'v':4,
        'w':4,
        'y':4,

        'k':5,

        'j':8,
        'x':8,

        'q':10,
        'z':10
    }
