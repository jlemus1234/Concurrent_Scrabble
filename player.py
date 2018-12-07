#!/usr/bin/python -tt
#   player.py
#
#   COMP 50CP Fall 2018
#   Group Project: Distributed Scrabble
#
#   Modified On: November 30, 2018

""" Purpose: This module holds the implementation of the class Player"""

import board
import tile
import threading
from middle_for_player import send_message

NUM_PLAYER = 4


class Player:
    def __init__(self, name=""):
        self.board = board.Board()
        self.score = [0 for i in range(NUM_PLAYER)]
        self.name = name
        self.tiles = [tile.Tile() for _ in range(7)]
        self.gui = None
        self.lock = threading.RLock()

    def setGUI(self, GUI):
        with self.lock:
            self.gui = GUI

    def refresh_failure(self, board_array, score_ray):
        with self.lock:
            self.board.set_board(board_array)
            self.score = score_ray

        # Convert board to 2d Array of tiles, hand (array of tiles), and score
        self.gui.refresh(self.board.get_board(), self.tiles, self.score)

    def refresh_success(self, board_array, score_ray, tile_ray):
        with self.lock:
            self.board.set_board(board_array)
            self.score = score_ray
            for tile in tile_ray:
                self.tiles.append(tile)

        # Convert board to 2d Array of tiles, hand (array of tiles), and score
        self.gui.refresh(self.board.get_board(), self.tiles, self.score)

    def get_word_from_line(self, start_pos, direction):
        with self.lock:
            row = orig_row = start_pos[0]
            col = orig_col = start_pos[1]
            # Add first letter of word to string
            word = self.board.grid[row][col]

            start_row = -1
            start_col = -1

            # If word is in row, we will be sliding the col index
            if direction == "r":
                start_row = row
                # Finds begining of word in the current row
                while self.board.inbounds(col - 1):
                    if self.board.grid[row][col - 1].is_blank():
                        start_col = col
                        break
                    else:
                        word.append(self.board.grid[row][col - 1])
                        

                word.reverse()
                col = orig_col

                # finds end of word in the current row
                while self.inbounds(col + 1):
                    if self.board.grid[row][col + 1].is_blank():
                        break
                    else:
                        word.append(self.board.grid[row][col + 1])

            # If word is in column, we will be sliding the row index
            else:
                start_col = col
                # Finds begining of word in the current col
                while self.board.inbounds(row - 1):
                    if self.board.grid[row - 1][col].is_blank():
                        start_row = row
                        break
                    else:
                        word.append(self.board.grid[row - 1][col])
                        

                word.reverse()
                row = orig_row

                # finds end of word in the current col
                while self.inbounds(row + 1):
                    if self.board.grid[row + 1][col].is_blank():
                        break
                    else:
                        word.append(self.board.grid[row + 1][col])

            return (word, start_row, start_col)


    def made_move(self, tile_ray, direction, start_pos, used_tiles):
        with self.lock:
            valid = True

            # Determine if space found in word. If found, boolean set to False
            for tile in tile_ray:
                if tile.value == '':
                    valid = False

            # If tiles places are all sequential ...
            if valid:
                # Get word from entire row or col depending on direction
                word, new_pos = get_word_from_line(start_pos, direction)
                # Parse for word and add to board for verification
                status, new_grid, new_score = self.board.update(new_pos, word
                                                                direction)
                if status == True:
                    # Send message to Erlport
                    send_message(("move", word, direction, start_pos, used_tiles))



    # Have function to call GUI fucntion to report winner

