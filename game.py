# game class in Python

import threading
from board import Board
from tile import Tile
from tile import string_to_tiles
from tile import tiles_to_string
from bag import Bag
from middle_for_game import send_message

#global GAME_END = -1
global GAME_END


class Game:

#    def __init__(self):

    def __init__(self, PID_players, PID_my):
	GAME_END = -1
        self.lock = threading.RLock()
        self.board = Board()
        # self.erlangPID = Pid
        self.scores = []
        self.bag = Bag()
        self.first_move = True
    	# adding so board can use imported send_message
    	self.PID_players = PID_players
    	self.PID_my = PID_my



    # should review exactly what critical section is so can make it run faster
    def check_move(self, player_number, word, starting_positon, direction, used_tiles):
        # not converting used_tiles to Tiles
        # switches tuple form of tiles back to Tile form
        word = [Tile("","","","",letter) for letter in word]

        # check if first move is in center
        if self.first_move:
            if not over_lap_center(word, starting_positon, direction):
                self.send_to_one_player(player_number, False, self.board.get_board(), self.scores, [], [])
                return

        with lock:
            valid, new_board, score = board.update(starting_positon, word, direction)
            if not valid:
                self.send_to_one_player("refresh", player_number, False, new_board, self.scores, [], [])
            else:
                # have to send to all players new state and to one player new tiles
                self.first_move = False
                self.scores[player_number] += score
                new_tiles = self.bag.take_n_from_bag(len(used_tiles))
                self.send_to_one_player(player_number, True, [[]], [], used_tiles, new_tiles)
                self.send_to_all_player(True, new_board, self.scores, [], [])

    def over_lap_center(word, positon, direction):
        length = len(word)
        for i in range(length):
            if positon == (7,7):
                return True
            if direction == 'd':
                positon = (positon[0] + 1, positon[1])
            else:
                postion = (positon[0] , positon[1] + 1)
        return False


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

    #
    # def send_message(pid_list, my_pid ,player_number, data):
    # 	Pid_to_send = pid_list[player_number]
    # 	message = (Pid_to_send + data)
    # 	cast(my_pid, message)




    # messge recieve
    # word, direction, starting_positon, used tiles

    # message to send:
    # status, board, scores, old_tiles, new_tiles

    def send_to_one_player(self, keyword, player_number, staus, board, scores, old_tiles, new_tiles):
        # everything sent should be in a sendable way
        tuple_board     = [[tile.to_tuple() for tile in row] for row in board]
        # not converting used_tiles to Tiles so no need to switch back
        #tuple_old_tiles =  [tile.to_tuple() for tile in old_tiles]
        tuple_new_tiles =  [tile.to_tuple() for tile in new_tiles]
        # funciton name needs to be changed when we finish middle module
        #send_message(player_number, (status, tuple_board, scores, tuple_old_tiles, tuple_new_tiles))
        send_message(self.PID_players, self.PID_my, player_number, (status, tuple_board, scores, old_tiles, tuple_new_tiles))



    def send_to_all_player(self, status, board, scores, old_tiles, new_tiles):
        for player_number in range(4):
            send_to_one_player(player_number, status, board, scores, old_tiles, new_tiles)

    # not worring about ending game right now
    def end_game(self):
        global GAME_END
        max_score = max(scores)
        winning_player = GAME_END
        for i in range(0,4):
            if (scores[i] == max_score):
                winning_player = i
                break
        send_back = [GAME_END for i in range(4)]
        send_back[winning_player] = max_score
        send_to_all_player(True, [[]], send_back, [], [])
