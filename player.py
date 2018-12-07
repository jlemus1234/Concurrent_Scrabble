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
from GUI import Gui


class Player:
    def __init__(self, name, PID):
        self.board = board.Board()
        self.score = 0
#        self.name = "Jane Doe"
	    self.name = name
        self.tiles = []
        self.erlangPID = PID
        self.gui = None
        self.lock = threading.RLock()

    def setGUI(self, GUI):
        self.gui = GUI


    def made_move(self, tile_ray, direction, start_pos, used_tiles):
        #valid = True

        # # Determine if space found in word. If found, boolean set to False
        # for tile in tile_ray:
        #     if tile.value == '':
        #         valid = False

        start_index = start_pos[0] # if direction = 'd'
        if direction == 'r':
            start_index = start_pos[1]

        word = self.get_word(tile_ray, start_pos);

        valid, new_grid, new_score = self.board.update(start_pos, word, direction)

        if valid:
            # send to server
            self.send_to_server(word, direction, new_grid, used_tiles)
            # remove tiles from rack
            for tile in used_tiles:
                self.tiles.remove(tile)

        # refresh display
        self.gui.refresh(new_grid, self.tiles, self.scores)








        # If tiles places are all sequential ...
        if valid:
            # Board class takes in different values for direction. "d" for row
            direction = "d" if direction == "r" else "nd"
            # Update board with tiles and
            status, new_grid, new_score = self.board.update(start_pos, tile_ray, direction)
            if status == True:
                # Send message to Erlport
                status = True
                # After message received form Erlport ...
                # Remove tiles used and update to new if successful. Update grid

                # self.board.grid = new_grid
                # self.score = new_score


    # def sendMessageToErlang(self, tile_ray, direction, start_pos, used_tiles):
    # def receiveMessageFromErlang(self):
    # def moveSuccessful()



    def get_word(tile_ray, start_pos):
        word = []
        front = start_pos
        # finds begining of word
        while front >= 0 and front =< 14:
            if grid[front].is_blank():
                break
            else:
                word.append(tile_ray[front])
            front -= 1

        word.reverse()
        back = start_pos + 1

        # finds end of word
        while back >= 0 and back =< 14:
            if grid[back].is_blank():
                break
            else:
                word.append(tile_ray[back])
            back += 1
        return word














    # Validate to get start_pos of word, not first tile put down, and the
    # array of tiles to represent word

    # import middle module and send stuff to it via function call. Convert
    # everything to tuples

    # Have a function to get new board and new score, then call GUI update

    # Have function to call GUI fucntion to report winner

    # For each class written, convert to Tuuple (to_tuple)
