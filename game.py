# game class in Python

import threading
from board import Board
from tile import Tile
from tile import string_to_tiles
from tile import tiles_to_string
from bag import Bag

GAME_END = -1

class Game:

    def __init__(self, Pid):
        self.lock = threading.RLock()
        self.board = Board()
        self.erlangPID = Pid
        self.scores = []
        self.bag = Bag()


    def end_game(self):
        max_score = max(scores)
        winning_player = GAME_END
        for i in range(0,4):
            if scores[i] == max_score
                winning_player = i
                break
        send_to_all_player(True, winning_player, GAME_END, GAME_END, GAME_END)

    def check_move(self, player_number, word, starting_positon, direction, used_tiles):
        with lock:
            valid, new_board, score = board.update(starting_positon, word, direction)
            if not valid:
                self.send_to_one_player(player_number, False, new_board, self.scores)
            else:
                # have to send to all players new state and to one player new tiles
                self.scores[player_number] += score
                new_tiles = self.bag.get_n_tiles(len(used_tiles))
                self.send_to_one_player(player_number, True, '', '', used_tiles, new_tiles)
                self.send_to_all_player(True, new_board, self.scores, '', '')

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

    # messge recieve
    # word, direction, starting_positon, used tiles

    # message to send:
    # status, board, scores, old_tiles, new_tiles
    def send_to_one_player(self, player_number, staus, board, scores, old_tiles, new_tiles):
        dd

    def send_to_all_player(self, status, board, scores, old_tiles, new_tiles):
        for player_number in range(0,4):
            send_to_one_player(player_number, status, board, scores, old_tiles, new_tiles)
