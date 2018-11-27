# board class in Python

import threading
import tile

class board:

    def __init__(self):
        self.lock = threading.Lock()
        self.grid = starting_grid()

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

    def starting_grid():
        grid = [[tile() for i in range(0,14)] for j in range(0,14)]
        # TODO: add specail tiles

        # adding double word tiles
        for col in range(0,14):
            grid[col][col]    = tile('',0,(2,'w'),0)
            grid[14-col][col] = tile('',0,(2,'w'),0)



        # adding triple word tiles
        for row in range(0,14,7):
            for col in range(0,14,7):
                grid[row][col] = tile('',0,(3,'w'),0)

        grid[7][7] = tile('*',0,(1,'w'),0) # center start tile
