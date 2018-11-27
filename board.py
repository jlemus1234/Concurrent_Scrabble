# board class in Python

import threading
import tile

class board:

    def __init__(self):
        self.lock = threading.Lock()
        self.grid = __starting_grid()

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
        # TODO write all code
        with self.lock:
            temp

    def print(self):
        for row in self.grid:
            for tile in row:
                to_be_printed = "__"
                if tile.multiplier[0] != 1:
                    to_be_printed = "{}{}".format(multiplier[0],multiplier[1])
                print(to_be_printed,end=" ")
            print("",end="\n")

        
    def __starting_grid():
        grid = [[tile() for i in range(0,14)] for j in range(0,14)]

        # adding double word tiles
        for col in range(0,14):
            grid[col][col]    = tile('',0,(2,'w'),0)
            grid[14-col][col] = tile('',0,(2,'w'),0)

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
            x = double_letter_places[x]
            grid[y][x]       = tile('',0,(2,'l'),0)
            grid[x][y]       = tile('',0,(2,'l'),0)
            grid[14-y][x]    = tile('',0,(2,'l'),0)
            grid[14-x][y]    = tile('',0,(2,'l'),0)
            grid[y][14-x]    = tile('',0,(2,'l'),0)
            grid[x][14-y]    = tile('',0,(2,'l'),0)
            grid[14-x][14-y] = tile('',0,(2,'l'),0)
            grid[14-y][14-x] = tile('',0,(2,'l'),0)

        # adding triple letter tiles
        triple_letter_places = {
          # y:x
            1:5,
            5,5
        }
        for y in triple_letter_places:
            x = triple_letter_places[x]
            grid[y][x]       = tile('',0,(3,'l'),0)
            grid[x][y]       = tile('',0,(3,'l'),0)
            grid[14-y][x]    = tile('',0,(3,'l'),0)
            grid[14-x][y]    = tile('',0,(3,'l'),0)
            grid[y][14-x]    = tile('',0,(3,'l'),0)
            grid[x][14-y]    = tile('',0,(3,'l'),0)
            grid[14-x][14-y] = tile('',0,(3,'l'),0)
            grid[14-y][14-x] = tile('',0,(3,'l'),0)

        # adding triple word tiles
        for row in range(0,14,7):
            for col in range(0,14,7):
                grid[row][col] = tile('',0,(3,'w'),0)

        grid[7][7] = tile('*',0,(1,'w'),0) # center start tile
        return grid
