# game class in Python

import threading
from board import Board
from tile import Tile
from tile import string_to_tiles
from tile import tiles_to_string
from bag import Bag

global GAME_END


class Game:

    def __init__(self, PID_players=[], PID_my=[]):

        GAME_END = -1
        self.lock = threading.RLock()
        self.board = Board()    # Master Board
        self.scores = []        # List of all players' scores
        self.bag = Bag()        # Bag of remaining tiles
        # Used to check if first move overlaps with center tile
        self.first_move = True  
        # List of PID of players so board can use imported send_message
        self.PID_players = PID_players 
        self.PID_my = PID_my    # Current PID
        print("Finished creating a new Game instance")

    # Given a player number, a word, the starting position of the word on the
    # master board, the direction (right or down), and an array of the tiles
    # used, validate move with master board. If valid, refresh all players' 
    # boards with new board and score. If not, put old tiles back in player hand
    def check_move(self, player_number, word_tuple, starting_positon, 
                   direction, used_tiles):
        print("Inside Check_move game module")
        # Switches tuple form of tiles back to Tile object form
        word = [Tile("","","","",letter) for letter in word_tuple]

        # check if first move is in center
        if self.first_move:
            if not self.over_lap_center(word, starting_positon, direction):
                # If first move doesn't overlap center, place old tiles back
                self.send_to_one_player("refresh", player_number, False, 
                                    self.board.get_board(), self.scores, [], [])
                return
        print("Before lock acquired in check move")
        with self.lock:
            print("After lock acquired inside check move")

            # Validate word. If valid, the new board with the word inserted as 
            # well as the new score is returned
            valid, new_board, score = self.board.update(starting_positon, word,
                                                    direction, self.first_move)
            print("valid: {}".format(valid))

            # If word not valid, add used tiles back to player's hand and 
            # refresh board to old board
            if not valid:
                self.send_to_one_player("refresh", player_number, False, 
                                        new_board, self.scores, [], [])
            # Else if word is valid, update score, return new tiles, and return
            else:
                # Have to send to all players new board and new scores, whereas
                # only one player receives new tiles
                self.first_move = False
                self.scores[player_number] += score
                new_tiles = self.bag.take_n_from_bag(len(used_tiles))
                self.send_to_one_player("tiles", player_number, True, [[]], 
                                        [], used_tiles, new_tiles)
                self.send_to_all_player(True, new_board, self.scores, [], [])

    # Given a word, its position (row, col), and the direction (right or down),
    # return True if it overlaps with middle tile (index [7][7])
    def over_lap_center(self, word, positon, direction):
        print("over_lap_center called")
        length = len(word)
        for i in range(length):
            if positon == (7,7):
                return True
            # If word is in a column, update row to get to next letter in word
            if direction == 'd':
                positon = (positon[0] + 1, positon[1])
            # If word is in a row, update column to get to next letter in word
            else:
                postion = (positon[0] , positon[1] + 1)
        return False

    # Every time a new player connects, append their initial score (0) to the 
    # score array. once four players connect, call start_game()
    def new_player(self, player_number):
        print("In new_player game.py")
        with self.lock:
            self.scores.append(0)
            print("This is the player number:{}".format(player_number))
            if player_number == 3:
                self.start_game()

    # After four players enter game, send the empty board as well as 7 random 
    # tiles to each player, as well as the initial scores (0).
    def start_game(self):
        print("In start_game of game.py")
        for i in range(4):
            tiles = self.bag.take_n_from_bag(7)
            tile_tuples = [tile.to_tuple() for tile in tiles]
            self.send_to_one_player("tiles", i, True, [[]], [], [], tiles)
            self.send_to_one_player("refresh", i, True, self.board.get_board(),
                                    [0,0,0,0],[],[])


    # Sends information about the board, score, old tiles, and new tiles to 
    # one player via send_messsage, which encorporates Erlport, hence why
    # everything is being converted to a tuple
    def send_to_one_player(self, keyword, player_number, staus, board, scores, 
                           old_tiles, new_tiles):
        print("in send_to_one_player of game.py")
        # Convert all tiles in board into a tuple passed in 2D array
        tuple_board     = [[tile.to_tuple() for tile in row] for row in board]
        tuple_new_tiles =  [tile.to_tuple() for tile in new_tiles]
        # Send the board, scores, old tiles, and new tiles converted as tuples
        # to the player number via Erlport using send_message().
        send_message(player_number, (keyword, tuple_board, scores, old_tiles, 
                                     tuple_new_tiles))


    # Sends information about the board, score, old tiles, and new tiles to 
    # every player via calling send-to_one_player four times. 
    def send_to_all_player(self, status, board, scores, old_tiles, new_tiles):
        print("In send to all players of game.py")
        for player_number in range(4):
            self.send_to_one_player("refresh", player_number, status, board, 
                                    scores, old_tiles, new_tiles)

    # not worring about ending game right now
    # def end_game(self):
    #    global GAME_END
    #    max_score = max(scores)
    #    winning_player = GAME_END
    #    for i in range(0,4):
    #        if (scores[i] == max_score):
    #            winning_player = i
    #            break
    #    send_back = [GAME_END for i in range(4)]
    #    send_back[winning_player] = max_score
    #    send_to_all_player(True, [[]], send_back, [], [])


from middle_for_game import send_message
