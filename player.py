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
from erlport.erlterms import Atom
from erlport.erlang import set_message_handler, call, cast, self as selfPID
# from middle_for_player import send_message



class Player:
    def __init__(self, name, PID_server_player, PID_me_player):
        self.board = Board()
        self.scores = [0,0,0,0]
        self.name  = name
        self.tiles = []
        self.erlangPID = PID_server_player
        self.erlangMe = PID_me_player
        self.gui = None
        self.lock = threading.Lock()

    def setGUI(self, GUI):
        with self.lock:
            self.gui = GUI


    def made_move(self, tile_ray, direction, start_pos_array, used_tiles):
        start_pos = (start_pos_array[0], start_pos_array[1])
        with self.lock:
            start_index = start_pos[0] # if direction = 'd'
            if direction == 'r':
                start_index = start_pos[1]

            word, start_index = self.get_word(tile_ray, start_index);
            if direction == 'r':
                start_pos = (start_pos[0], start_index)
            else:
                start_pos = (start_index, start_pos[1])

            valid, new_grid, new_score = self.board.update(start_pos, word, 
                                                           direction, False)
            if valid:
                # send to server
                self.send_to_server(word, direction, start_pos, used_tiles)
            # refresh display
            self.gui.refresh(new_grid, self.tiles[:], self.scores)

    def refresh(self, tile_board, scores):
        with self.lock:
            self.board.set_board(tile_board)
            self.scores = scores
            self.board.print_board()
            cur_tiles = self.tiles[:]
            # print tiles
            for tile_print in cur_tiles:
                print(tile_print.to_tuple())
        self.gui.refresh(tile_board, cur_tiles, scores)

    def get_new_tiles(self, old_tiles, new_tiles):
        with self.lock:
            for tile in old_tiles:
                self.tiles.remove(tile)
            self.tiles.extend(new_tiles)
            tiles_cur = self.tiles[:]
            scores_cur = self.scores
            # print tiles
            for tile_print in tiles_cur:
                print(tile_print.to_tuple())
        self.gui.refresh(self.board.get_board(), tiles_cur, scores_cur)

    def send_to_server(self, word, direction, start_pos, used_tiles):
        word_tuple = [letter.to_tuple() for letter in word]
        used_tiles_tuple = [letter.to_tuple() for letter in used_tiles]
        send_message(self.erlangPID, (self.erlangMe, "move", word_tuple,
        direction, start_pos, used_tiles_tuple))


    def get_word(self, tile_ray, start_pos):
        word = []
        front = start_pos
        # finds begining of word
        while (front >= 0 and front <= 14):
            if tile_ray[front].is_blank():
                front += 1
                break
            else:
                word.append(tile_ray[front])
            front -= 1

        word.reverse()
        back = start_pos + 1

        # finds end of word
        while (back >= 0 and back <= 14):
            if tile_ray[back].is_blank():
                back -= 1
                break
            else:
                word.append(tile_ray[back])
            back += 1
        return word, front

def send_message(dest_pid, message):
    cast(dest_pid, message)

from GUI import Gui
