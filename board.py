# board class in Python

import threading
from tile import Tile
from tile import string_to_tiles
from tile import tiles_to_string
import twl


class Board:

    def __init__(self, grid=''):
        self.lock = threading.RLock()
        # If no grid given, initiate grid with multipliers
        if grid == '':
            self.grid = self.starting_grid()
        # If grid given, copy grid row by row
        else:
            self.grid = [row[:] for row in grid]

    # returns deep copy of grid
    def get_board(self):
        with self.lock:
            return [row[:] for row in self.grid]

    def set_board(self, new_grid):
        with self.lock:
            self.grid = new_grid

    # takes array of tiles as word
    def update(self,starting_positon, word, direction, is_first):
        print("in board update")
        score = 0
        word_multipler = 1
        is_touching = False
        # simple tile used as a base for many comparisons
        tile = Tile()
        # used to see if user placed 7 tiles so 50 point bonus can be added
        new_tile_count = 0
        print("about to get lock")
        with self.lock:
            print("got lock checking against dict")
            print("word in dict")
            print(tiles_to_string(word))
            if (not twl.check(tiles_to_string(word))):
                # print("returning 1")
                return (False, self.grid, 0)
            print("checked dict")
            # check if starting position is valid
            row = starting_positon[0]
            col = starting_positon[1]
            print("row before inbonds: {}".format(row))
            print("col before inbounds: {}".format(row))
            if not self.inbounds(row,col):
                # print("returning 2")
                return (False, self.grid, 0)

            # create copy of grid so if the word turns out to not work we have the old list
            grid = [row_make_temp[:] for row_make_temp in self.grid]
            print("grid: {}".format(grid))
            # used to lock cross_score and is_valid
            mutex = threading.Lock()
            threads = []
            cross_score = [0]
            is_valid = [True]
            for letter in word:
                # check to see if a tile is already there
                print("row before is_blank: {}".format(row))
                print("col before is_blank: {}".format(row))

                if grid[row][col].is_blank():
                    print("in is_blank section")
                    # can be inserted
                    new_tile_count += 1
                    temp_multi = grid[row][col].multiplier
                    if temp_multi[1] == 'l':
                        score += letter.score * temp_multi[0]
                    else:
                        score += letter.score
                        word_multipler *= temp_multi[0]

                    grid[row][col] = letter
                    # check to see if a tile is touching thats not in the direction, and if there is make sure thats a word
                    if direction == 'd':
                        # to check row
                        cur_thread = threading.Thread(target = self.check_and_score_row, args=(grid,row,col,temp_multi,cross_score,is_valid,is_touching,mutex))
                    else:
                        # to check col
                        cur_thread = threading.Thread(target = self.check_and_score_col, args=(grid,row,col,temp_multi,cross_score,is_valid,is_touching,mutex))
                    # print("starting thread")
                    cur_thread.daemon = True
                    cur_thread.start()
                    threads.append(cur_thread)

                # check to see if tile trying to insert is already there
                elif grid[row][col] != letter:
                    print("letter already there")
                    return (False, self.grid, 0)
                else:
                    # this means we are inserting the same tile so we are now overlapping what is there
                    print("tile already there, so has overlap")
                    is_touching = True
                    score += grid[row][col].score

                print("about to increase row/col")
                # update row and col
                if direction == 'd':
                    row += 1
                else:
                    col += 1

            for thread in threads:
                thread.join()
                # print("thread joined")

            # outside looping through letters
            if not is_valid[0] or (not is_touching):
                return (False, self.grid, 0)

            self.grid = grid
            score = score * word_multipler + (cross_score[0])
            print("returing from update in board")
            return (True, self.grid, (score,score+50)[new_tile_count == 7])

    def check_and_score_col(self,grid,r,c,multiplier, xtra_score, valid, is_touching, mutex):
        print("in thread check_and_score_col")
        # checking row so col is changing
        word = [grid[r][c]]
        temp_score = grid[r][c].score
        front_r = r - 1
        # finds begining of word
        while self.inbounds(front_r):
            if grid[front_r][c].is_blank():
                break
            else:
                word.append(grid[front_r][c])
                temp_score += grid[front_r][c].score
            front_r -= 1

        word.reverse()
        back_r = r + 1

        # finds end of word
        while self.inbounds(back_r):
            if grid[back_r][c].is_blank():
                break
            else:
                word.append(grid[back_r][c])
                temp_score += grid[back_r][c].score
            back_r += 1

        if len(word) == 1:
            # is valid but not a new word
            # print("size is 1 starting letter = {}".format(grid[r][c].value))
            return

        if multiplier[1] == 'l':
            temp_score += grid[r][c] * (multiplier[0]-1)
        else:
            temp_score *= multiplier[0]

        str_word = tiles_to_string(word)
        word_valid = twl.check(str_word)
        # print("score from a thread = {}".format(temp_score))
        with mutex:
            valid[0] = valid[0] and word_valid
            xtra_score[0] += temp_score
            is_touching = True
        print("end thread check_and_score_col")
        return


    def check_and_score_row(self,grid,r,c,multiplier, xtra_score, valid, mutex):
        print("in thread check_and_score_row")
        # print("in thread")
        # checking row so col is changing
        word = [grid[r][c]]
        temp_score = grid[r][c].score
        front_c = c - 1
        # finds begining of word
        while self.inbounds(front_c):
            if grid[r][front_c].is_blank():
                break
            else:
                word.append(grid[r][front_c])
                temp_score += grid[r][front_c].score
            front_c -= 1

        word.reverse()
        back_c = c + 1

        # finds end of word
        while self.inbounds(back_c):
            if grid[r][back_c].is_blank():
                break
            else:
                word.append(grid[r][back_c])
                temp_score += grid[r][back_c].score
            back_c += 1

        if len(word) == 1:
            # is valid but not a new word
            return

        if multiplier[1] == 'l':
            temp_score += grid[r][c] * (multiplier[0]-1)
        else:
            temp_score *= multiplier[0]

        str_word = tiles_to_string(word)
        word_valid = twl.check(str_word)
        # print("score from a thread = {}".format(temp_score))
        with mutex:
            valid[0] = valid[0] and word_valid
            xtra_score[0] += temp_score
            is_touching = True
        print("end thread check_and_score_row")
        return


    # untested function
    def to_tuple(self):
        with self.lock:
            tuple_board = [[tile.to_tuple() for tile in row] for row in self.board]
            return tuple_board


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
                buffer = ""
                for tile in row:
                    to_be_printed = "__"
                    if tile.value != '':
                        to_be_printed = "{} ".format(tile.value)
                    elif tile.multiplier[0] != 1:
                        to_be_printed = "{}{}".format(tile.multiplier[0],tile.multiplier[1])
                    buffer = buffer + to_be_printed + " "
                print(buffer)

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

        grid[7][7] = Tile('',0,(1,'w'),0) # center start tile
        return grid
