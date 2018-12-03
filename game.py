# game class in Python

import threading
from board import Board
from tile import Tile
from tile import string_to_tiles
from tile import tiles_to_string
from bag import Bag
from middle_for_game import send_message

global GAME_END = -1

class Game:

    def __init__(self):
        self.lock = threading.RLock()
        self.board = Board()
        # self.erlangPID = Pid
        self.scores = []
        self.bag = Bag()


    def end_game(self):
        global GAME_END
        max_score = max(scores)
        winning_player = GAME_END
        for i in range(0,4):
            if scores[i] == max_score
                winning_player = i
                break
        send_back = [GAME_END for i in range(4)]
        send_back[winning_player] = max_score
        send_to_all_player(True, [[]], send_back, [], [])


    # should review exactly what critical section is so can make it run faster
    def check_move(self, player_number, word, starting_positon, direction, used_tiles):
        # not converting used_tiles to Tiles
        # switches tuple form of tiles back to Tile form
        word = [Tile("","","","",letter) for letter in word]
        with lock:
            valid, new_board, score = board.update(starting_positon, word, direction)
            if not valid:
                self.send_to_one_player(player_number, False, new_board, self.scores, [], [])
            else:
                # have to send to all players new state and to one player new tiles
                self.scores[player_number] += score
                new_tiles = self.bag.take_n_from_bag(len(used_tiles))
                self.send_to_one_player(player_number, True, [[]], [], used_tiles, new_tiles)
                self.send_to_all_player(True, new_board, self.scores, [], [])

    def new_player(self, player_number):
        with lock:
            scores.append(0)
            if player_number == 3:
                self.start_game()

    # to be called after the 4th player has entered
    def start_game(self):
        for i in range(4):
            tiles = self.bag.take_n_from_bag(7)
            self.send_to_one_player(i, False, self.board.get_board(), [0,0,0,0], tiles,[])

    # messge recieve
    # word, direction, starting_positon, used tiles

    # message to send:
    # status, board, scores, old_tiles, new_tiles
    def send_to_one_player(self, player_number, staus, board, scores, old_tiles, new_tiles):
        # everything sent should be in a sendable way
        tuple_board     = [[tile.to_tuple() for tile in row] for row in board]
        # not converting used_tiles to Tiles so no need to switch back
        #tuple_old_tiles =  [tile.to_tuple() for tile in old_tiles]
        tuple_new_tiles =  [tile.to_tuple() for tile in new_tiles]
        # funciton name needs to be changed when we finish middle module
        send_message(player_number, (status, tuple_board, scores, tuple_old_tiles, tuple_new_tiles))

    def send_to_all_player(self, status, board, scores, old_tiles, new_tiles):
        for player_number in range(4):
            send_to_one_player(player_number, status, board, scores, old_tiles, new_tiles)
