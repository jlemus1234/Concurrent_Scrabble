# middle module for game


from erlport.erlterms import Atom
from erlport.erlang import set_message_handler, call, cast


import time
global game
global PID_my
global PID_players
#global PID_players = []

def start(Pid):
    global game, PID_my, PID_players
    PID_my = Pid
    # You can't pass around empty arrays in python so make the first entry your own PID
    PID_players = []
    # Change game so it accepts an array of players
    game = Game(PID_my=PID_my)



#def send_message(player_number, data):
#    global PID_players, PID_my
#    Pid_to_send = PID_players[player_number]
#    message = (Pid_to_send + data)
#    cast(PID_my, message)

def send_message(player_number, message):
    global PID_my, PID_players
    print("In middle for game's send message")
    dest = PID_players[player_number]
    call(Atom("scrabble"), Atom("send_to_pyclient"), [dest, message])
    #cast(PID_my, (PID_players[player_number], message))


# def send_message(pid_list, my_pid ,player_number, data):
#     Pid_to_send = pid_list[player_number]
#     message = (Pid_to_send + data)
#     print("In send_message")
#     print(message)
#     cast(my_pid, message)

def register_handler(dest):
    # no need to hold on to dest (the PID from which the message was sent)
    # because it will stay const and was set in start
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
    global PID_players
    PID_players.append(message[0])
    game.new_player(len(PID_players) - 1)

def make_move(message):
    player_number, word, direction, starting_positon, used_tiles = split_message(message)
    game.check_move(player_number, word, starting_positon, direction, used_tiles)

def game_over():
    game.end_game()

def split_message(message):
    global player_PID
    player_number       = PID_players.index(message[0])
    word                = message[2]
    direction           = message[3]
    starting_positon    = message[4]
    used_tiles          = message[5]
    return player_number, word, direction, starting_positon, used_tiles

from game import Game

# messge recieve
# player_PID, keyword, word, direction, starting_positon, used tiles

# message to send:
# keyword, board, scores, old_tiles, new_tiles

# example of how erlport message passing words
# cast(erlPID, data)


from game import Game
