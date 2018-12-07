#!/usr/bin/python -tt
#   player.py
#
#   COMP 50CP Fall 2018
#   Group Project: Distributed Scrabble
#
#   Modified On: November 30, 2018

""" Purpose: This module holds the implementation of the class Player"""

from board import Board
from tile import Tile
import threading

from middle_for_game import send_message



class Player:
    def __init__(self, name, PID):
	self.board = Board()
        self.score = 0
        self.name  = name
        self.tiles = []
        self.erlangPID = PID
        self.gui = None
        self.lock = threading.RLock()

    def setGUI(self, GUI):
        with self.lock:
            self.gui = GUI


    def made_move(self, tile_ray, direction, start_pos, used_tiles):
        with self.lock:
            start_index = start_pos[0] # if direction = 'd'
            if direction == 'r':
                start_index = start_pos[1]

            word = self.get_word(tile_ray, start_index);

            valid, new_grid, new_score = self.board.update(start_pos, word, direction)

            if valid:
                # send to server
                self.send_to_server(word, direction, start_pos, used_tiles)

                # dont want to remove tiles anymore
                # # remove tiles from rack
                # for tile in used_tiles:
                #     self.tiles.remove(tile)

            # refresh display
            self.gui.refresh(new_grid, self.tiles, self.scores)

    def refresh(self, tile_board, scores):
        with self.lock:
            self.board.set_board(tile_board)
            self.scores = scores
            self.board.print_board()
            # self.gui.refresh(tile_board, self.tiles, scores)

    def get_new_tiles(self, old_tiles, new_tiles):
        with self.lock:
            for tile in old_tiles:
                self.tiles.remove(tile)
            self.tiles.extend(new_tiles)
            for tile in self.tiles:
                print(tile.to_tuple())

            #self.gui.refresh(self.board.get_board(), self.tiles, self.scores)

    def send_to_server(self, word, direction, start_pos, used_tiles):
        word_tuple = [letter.to_tuple() for letter in word]
        used_tiles_tuple = [letter.to_tuple() for letter in used_tiles]
	## What is this send function?
        send_message(("move", word_tuple, direction, start_pos, used_tiles))


    def get_word(self, tile_ray, start_pos):
        word = []
        front = start_pos
        # finds begining of word
        while (front >= 0 and front <= 14):
            if grid[front].is_blank():
                break
            else:
                word.append(tile_ray[front])
            front -= 1

        word.reverse()
        back = start_pos + 1

        # finds end of word
        while (back >= 0 and back <= 14):
            if grid[back].is_blank():
                break
            else:
                word.append(tile_ray[back])
            back += 1
        return word



from GUI import Gui
    # def sendMessageToErlang(self, tile_ray, direction, start_pos, used_tiles):
    # def receiveMessageFromErlang(self):
    # def moveSuccessful()
















    # Validate to get start_pos of word, not first tile put down, and the
    # array of tiles to represent word

    # import middle module and send stuff to it via function call. Convert
    # everything to tuples

    # Have a function to get new board and new score, then call GUI update

    # Have function to call GUI fucntion to report winner

    # For each class written, convert to Tuuple (to_tuple)
