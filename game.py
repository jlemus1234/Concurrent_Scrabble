# game class in Python

import threading
from board import Board
from tile import Tile
from tile import string_to_tiles
from tile import tiles_to_string
from bag import Bag

class Game:

    def __init__(self, Pid):
        self.lock = threading.RLock()
        self.board = Board()
        self.erlangPID = Pid
        self.scores = []
        self.bag = Bag()


    def end_game():
        dd

    
    def check_move(self, player_number, tile_tuples, starting_positon, direction):
        with lock:
            valid, new_board, score = board.update(starting_positon, word, direction)
            if not valid:
                self.send_to_one_player(player_number, )


    def new_player(self, player_number):
        scores.append(0)
        if player_number == 3:
            self.start_game()

    # to be called after the 4th player has entered
    def start_game(self):
        for i in range(0,4):
            tiles = self.bag.get_seven_tiles()
            tile_tuples = []
            for tile in tiles:
                tile_tuples.append(tile.to_tuple())
            self.send_to_one_player(i,tile_tuples)


    # message to send:
    # status, board, scores, old_tiles, new_tiles
    def send_to_one_player(self, player_number, staus=True, board, scores):
        dd

    def send_to_all_player(self, data):
        for player_number in range(0,4):
            send_to_one_player(player_number)
