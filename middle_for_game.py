# middle module for game


from erlport.erlterms import Atom
from erlport.erlang import set_message_handler, call, cast


import time
global game
global PID_my
global PID_players

def start(Pid):
    global game, PID_my, PID_players
    PID_my = Pid
    PID_players = []
    game = Game(PID_my=PID_my)

# This function takes in a player numberr and a message that you want to send
# to that player. It then looks up the proper PID and sends it via Erlport
def send_message(player_number, message):
    global PID_my, PID_players
    print("In middle of game's send message")
    dest = PID_players[player_number]
    call(Atom("scrabble"), Atom("send_to_pyclient"), [dest, message])

# function needed for Erlport
# sets up the default handler for any messages python recieves
def register_handler(dest):
    set_message_handler(handler)
    return Atom("ok")

# need to add more funcitons
def handler(message):
    print("In python handler for middle_for_game")
    print(message)
    # getting rid of PID of destination
    #message = message[1:]
    #message_type = message[1]

    message_type = message[1]
    switcher = {
        "new player":add_player,
        "move":make_move
        # "game over":game_over
    }
    time.sleep(5)
    switcher[message_type](message)

# INCOMPLETE need to know what the message looks like
def add_player(message):
    print("Adding player")
    global PID_players
    PID_players.append(message[0])
    game.new_player(len(PID_players) - 1)

def make_move(message):
    print("Making move")
    player_number, word, direction, starting_positon, used_tiles = split_message(message)
    game.check_move(player_number, word, starting_positon, direction, used_tiles)

def game_over():
    game.end_game()

def split_message(message):
    print("Splitting message")
    global player_PID
    player_number       = PID_players.index(message[0])
    word                = message[2]
    direction           = message[3]
    starting_positon    = message[4]
    used_tiles          = message[5]
    print("Finished splitting message")
    return player_number, word, direction, starting_positon, used_tiles

from game import Game

# messge recieve
# player_PID, keyword, word, direction, starting_positon, used tiles

# message to send:
# keyword, board, scores, old_tiles, new_tiles

# example of how erlport message passing words
# cast(erlPID, data)


from game import Game
