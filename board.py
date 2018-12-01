# board class in Python

import threading
from tile import Tile
from tile import string_to_tiles
from tile import tiles_to_string
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
            return [row[:] for row in self.grid]

    def set_board(self, new_grid):
        with self.lock:
            self.grid = new_grid

    # takes array of tiles as word
    def update(self,starting_positon, word, direction):
        score = 0
        word_multipler = 1
        tile = Tile() # simple tile used as a base for many comparisons
        has_over_lap = False # used to make sure word is touching another
        new_tile_count = 0 # used to see if user placed 7 tiles so 50 point bonus can be added
        with self.lock:
            if (not twl.check(tiles_to_string(word))):
                # print("returning 1")
                return (False, self.grid, 0)

            # check if starting position is valid
            row = starting_positon[0]
            col = starting_positon[1]
            if not self.inbounds(row,col):
                # print("returning 2")
                return (False, self.grid, 0)

########################################################################
# gotta come up with a solution that allows a user to place a move like this: p
#                                             set being the new word          i
#                            should word if only s is played also             e
#                                                                             s e t
            # # check if letters to left or up
            # if self.inbounds(row - 1):
            #     if not self.grid[row-1][col].is_blank():
            #         # non-empty tile above
            #        print("returning 3")
            #         return (False, self.grid, 0)
            # if self.inbounds(col - 1):
            #     if not self.grid[row][col-1].is_blank():
            #         # non-empty tile left
            #        print("returning 4")
            #         return (False, self.grid, 0)
#########################################################################

            # create copy of grid so if the word turns out to not work we have the old list
            grid = [row[:] for row in self.grid]
            # used to lock cross_score and is_valid
            mutex = threading.Lock()
            threads = []
            cross_score = [0]
            is_valid = [True]
            for letter in word:
                # check to see if a tile is already there
                if grid[row][col].is_blank():
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
                        cur_thread = threading.Thread(target = self.check_and_score_row, args=(grid,row,col,temp_multi,cross_score,is_valid,mutex))
                    else:
                        # to check col
                        cur_thread = threading.Thread(target = self.check_and_score_col, args=(grid,row,col,temp_multi,cross_score,is_valid,mutex))
                    # print("starting thread")
                    cur_thread.daemon = True
                    cur_thread.start()
                    threads.append(cur_thread)

                # check to see if tile trying to insert is already there
                elif grid[row][col] != letter:
                    # this means trying to overwrite a letter
                    # print("returning 9")
                    # print("{} {} {} {}".format(grid[row][col].value,letter.value,grid[row][col].id,letter.id))

                    # TODO: add stuff for starting tile

                    return (False, self.grid, 0)
                else:
                    # this means we are inserting the same tile so we are now overlapping what is there
                    has_over_lap = True
                    score += grid[row][col].score

                # update row and col
                if direction == 'd':
                    row += 1
                else:
                    col += 1

            for thread in threads:
                thread.join()
                # print("thread joined")

            # outside looping through letters
            if (not has_over_lap) or (not is_valid[0]):
                # print("returning 10")
                # print("has_over_lap {}, is_valid[0] {}".format(has_over_lap,is_valid[0]))
                return (False, self.grid, 0)
            else:
                self.grid = grid
                score = score * word_multipler + (cross_score[0])
                return (True, self.grid, (score,score+50)[new_tile_count == 7])

    def check_and_score_col(self,grid,r,c,multiplier, xtra_score, valid, mutex):
        # print("in thread")
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
        return


    def check_and_score_row(self,grid,r,c,multiplier, xtra_score, valid, mutex):
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
        return

    # both not needed anymore
    # def check_word_col(self,row,col,grid):
    #     # assuming grid[row][col] is non empty
    #     start_row = row
    #     word = []
    #     score = 0
    #     while self.inbounds(start_row):
    #         if grid[start_row][col].is_blank():
    #             break
    #         else:
    #             word.append(grid[start_row][col])
    #             score += grid[start_row][col].score
    #             start_row -= 1
    #     start_row += 1
    #     word.reverse()
    #
    #     end_row = row + 1
    #     while self.inbounds(end_row):
    #         if grid[end_row][col].is_blank():
    #             break
    #         else:
    #             word.append(grid[end_row][col])
    #             score += grid[end_row][col].score
    #             end_row += 1
    #     end_row -= 1
    #
    #     str_word = ""
    #     for letter in word:
    #         str_word += letter.value
    #     return score, twl.check(str_word)
    # def check_word_row(self,row,col,grid):
    #     # assuming grid[row][col] is non empty
    #     start_col = col
    #     word = []
    #     score = 0
    #     while self.inbounds(start_col):
    #         if grid[row][start_col].is_blank():
    #             break
    #         else:
    #             word.append(grid[row][start_col])
    #             score += grid[row][start_col].score
    #             start_col -= 1
    #     start_col += 1
    #     word.reverse()
    #
    #     end_col = col + 1
    #     while self.inbounds(end_col):
    #         if grid[row][end_col].is_blank():
    #             break
    #         else:
    #             word.append(grid[row][end_col])
    #             score += grid[row][end_col].score
    #             end_col += 1
    #     end_col -= 1
    #
    #     str_word = ""
    #     for letter in word:
    #         str_word += letter.value
    #     return score, twl.check(str_word)

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

        grid[7][7] = Tile('',0,(1,'w'),0) # center start tile
        return grid







                    # old code to check for cross words

                    # if direction == 'd':
                    #     # have to check row
                    #     checked_row = False
                    #     if self.inbounds(col-1):
                    #         if not grid[row][col-1].is_blank():
                    #             # have to check word
                    #             checked_row = True
                    #             added_score, is_word = self.check_word_row(row,col,grid)
                    #             if not is_word:
                    #                 print("returning 5")
                    #                 return (False, self.grid, 0)
                    #             else:
                    #                 if temp_multi[1] == 'l':
                    #                     cross_score += added_score + (temp_multi[0]-1)*letter.score
                    #                 else:
                    #                     cross_score += added_score * temp_multi[0]
                    #     if (not checked_row) and self.inbounds(col+1):
                    #         if not grid[row][col+1].is_blank():
                    #             # have to check word
                    #             checked_row = True
                    #             added_score, is_word = self.check_word_row(row,col,grid)
                    #             if not is_word:
                    #                 print("returning 6")
                    #                 return (False, self.grid, 0)
                    #             else:
                    #                 if temp_multi[1] == 'l':
                    #                     cross_score += added_score + (temp_multi[0]-1)*letter.score
                    #                 else:
                    #                     cross_score += added_score * temp_multi[0]
                    #
                    # else:
                    #     # have to check col
                    #     checked_col = False
                    #     if self.inbounds(row-1):
                    #         if not grid[row-1][col].is_blank():
                    #             # have to check word
                    #             checked_col = True
                    #             added_score, is_word = self.check_word_col(row,col,grid)
                    #             if not is_word:
                    #                 print("returning 7")
                    #                 return (False, self.grid, 0)
                    #             else:
                    #                 if temp_multi[1] == 'l':
                    #                     cross_score += added_score + (temp_multi[0]-1)*letter.score
                    #                 else:
                    #                     cross_score += added_score * temp_multi[0]
                    #     if (not checked_col) and self.inbounds(col+1):
                    #         if not grid[row+1][col].is_blank():
                    #             # have to check word
                    #             added_score, is_word = self.check_word_col(row,col,grid)
                    #             if not is_word:
                    #                 print("returning 8")
                    #                 return (False, self.grid, 0)
                    #             else:
                    #                 if temp_multi[1] == 'l':
                    #                     cross_score += added_score + (temp_multi[0]-1)*letter.score
                    #                 else:
                    #                     cross_score += added_score * temp_multi[0]
