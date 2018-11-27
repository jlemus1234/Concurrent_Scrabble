# board class in Python

import threading
from tile import Tile
import twl

class Board:

    def __init__(self, grid=''):
        self.lock = threading.RLock()
        if grid == '':
            self.grid = self.starting_grid()
        else:
            self.grid = [row[:] for row in grid]

    # returns deep copy of grid
    def get_board(self):
        with self.lock:
            return self.grid

    def set_board(self, new_grid):
        with self.lock:
            self.grid = new_grid

    def is_valid(self,starting_positon, word, direction):
        # TODO write all code
        with self.lock:
            temp

    def update(self,starting_positon, word, direction):
        score = 0
        word_multipler = 1
        tile = Tile() # simple tile used as a base for many comparisons
        has_over_lap = False # used to make sure word is touching another
        with self.lock:
            if (not twl.check(word)):
                return (False, self.grid, 0)

            # check if starting position is valid
            row = starting_positon[0]
            col = starting_positon[1]
            if not self.inbounds(row,col):
                return (False, self.grid, 0)

            # check if letters to left or up
            if self.inbounds(row - 1):
                if not self.grid[row-1][col].is_blank():
                    # non-empty tile above
                    return (False, self.grid, 0)
            if self.inbounds(col - 1):
                if not self.grid[row][col-1].is_blank():
                    # non-empty tile left
                    return (False, self.grid, 0)


            # create copy of grid so if the word turns out to not work we have the old list
            grid = [row[:] for row in self.grid]
            for letter in word:
                # check to see if a tile is already there
                if grid[row][col].is_blank():
                    # can be inserted
                    temp_multi = grid[row][col].multiplier
                    if temp_multi[1] == 'l':
                        score += letter.score * temp_multi[1]
                    else:
                        score += letter.score
                        word_multipler *= temp_multi[1]

                    grid[row][col] = letter
                    # check to see if a tile is touching thats not in the direction, and if there is make sure thats a word
                    if direction == 'd':
                        # have to check row
                        checked_row = False
                        if self.inbounds(col-1):
                            if not grid[row][col-1].is_blank():
                                # have to check word
                                checked_row = True
                                if not self.check_word_row(row,col,grid):
                                    return (False, self.grid, 0)
                        if (not checked_row) and self.inbounds(col+1):
                            if not grid[row][col+1].is_blank():
                                # have to check word
                                if not self.check_word_row(row,col,grid):
                                    return (False, self.grid, 0)
                    else:
                        # have to check col
                        checked_col = False
                        if self.inbounds(row-1):
                            if not grid[row-1][col].is_blank():
                                # have to check word
                                checked_col = True
                                if not self.check_word_col(row,col,grid):
                                    return (False, self.grid, 0)
                        if (not checked_col) and self.inbounds(col+1):
                            if not grid[row+1][col].is_blank():
                                # have to check word
                                if not self.check_word_row(row,col,grid):
                                    return (False, self.grid, 0)


                # check to see if tile trying to insert is already there
                elif grid[row][col] != letter:
                    # this means trying to overwrite a letter
                    return (False, self.grid, 0)
                else:
                    # this means we are inserting the same tile so we are now overlapping what is there
                    has_over_lap = True

                if not has_over_lap:
                    return (False, self.grid, 0)


    def check_word_col(self,row,col,grid):
        # assuming grid[row][col] is non empty
        start_row = row
        word = []
        while self.inbounds(start_row):
            if grid[start_row][col].is_blank():
                break
            else:
                word.append(grid[start_row][col])
                start_row -= 1
        start_row += 1
        word.reverse()

        end_row = row + 1
        while self.inbounds(end_row):
            if grid[end_row][col].is_blank():
                break
            else:
                word.append(grid[end_row][col])
                end_row += 1
        end_row -= 1

        str_word = ""
        for letter in word:
            str_word += letter.value
        return twl.check(str_word)

    def check_word_row(self,row,col,grid):
        # assuming grid[row][col] is non empty
        start_col = col
        word = []
        while self.inbounds(start_col):
            if grid[row][start_col].is_blank():
                break
            else:
                word.append(grid[row][start_col])
                start_col -= 1
        start_col += 1
        word.reverse()

        end_col = col + 1
        while self.inbounds(end_col):
            if grid[row][end_col].is_blank():
                break
            else:
                word.append(grid[row][end_col])
                end_col += 1
        end_col -= 1

        str_word = ""
        for letter in word:
            str_word += letter.value
        return twl.check(str_word)

    def inbounds(self, i, j=1):
        return not (i < 0 or i > 14 or j < 0 or j > 14)


    def no_check_insert(self, starting_positon, word, direction):
        with self.lock:
            # create copy of grid so if the word turns out to not work we have the old list
            grid = [row[:] for row in self.grid]
            row = starting_positon[0]
            col = starting_positon[1]
            for letter in word:
                if col < 0 or col > 14 or row < 0 or col > 14:
                    return False
                grid[row][col] = letter
                if direction == 'd':
                    row += 1
                else:
                    col += 1
            self.grid = grid


    def print_board(self):
        with self.lock:
            for row in self.grid:
                for tile in row:
                    to_be_printed = "__"
                    if tile.value != '':
                        to_be_printed = "{} ".format(tile.value)
                    elif tile.multiplier[0] != 1:
                        to_be_printed = "{}{}".format(tile.multiplier[0],tile.multiplier[1])
                    print(to_be_printed,end=" ")
                print("",end="\n")


    def starting_grid(self):
        grid = [[Tile() for i in range(0,15)] for j in range(0,15)]

        # adding double word tiles
        for col in range(0,15):
            grid[col][col]    = Tile('',0,(2,'w'),0)
            grid[14-col][col] = Tile('',0,(2,'w'),0)

        # adding double letter tiles
        # using fact that it is symetrical split into eigths
        double_letter_places = {
          # y:x
            0:3,
            2:6,
            3:7, # will create dublicates
            6:6  # will create dublicates
        }
        for y in double_letter_places:
            x = double_letter_places[y]
            grid[y][x]       = Tile('',0,(2,'l'),0)
            grid[x][y]       = Tile('',0,(2,'l'),0)
            grid[14-y][x]    = Tile('',0,(2,'l'),0)
            grid[14-x][y]    = Tile('',0,(2,'l'),0)
            grid[y][14-x]    = Tile('',0,(2,'l'),0)
            grid[x][14-y]    = Tile('',0,(2,'l'),0)
            grid[14-x][14-y] = Tile('',0,(2,'l'),0)
            grid[14-y][14-x] = Tile('',0,(2,'l'),0)

        # adding triple letter tiles
        triple_letter_places = {
          # y:x
            1:5,
            5:5
        }
        for y in triple_letter_places:
            x = triple_letter_places[y]
            grid[y][x]       = Tile('',0,(3,'l'),0)
            grid[x][y]       = Tile('',0,(3,'l'),0)
            grid[14-y][x]    = Tile('',0,(3,'l'),0)
            grid[14-x][y]    = Tile('',0,(3,'l'),0)
            grid[y][14-x]    = Tile('',0,(3,'l'),0)
            grid[x][14-y]    = Tile('',0,(3,'l'),0)
            grid[14-x][14-y] = Tile('',0,(3,'l'),0)
            grid[14-y][14-x] = Tile('',0,(3,'l'),0)

        # adding triple word tiles
        for row in range(0,15,7):
            for col in range(0,15,7):
                grid[row][col] = Tile('',0,(3,'w'),0)

        grid[7][7] = Tile('*',0,(1,'w'),0) # center start tile
        return grid
