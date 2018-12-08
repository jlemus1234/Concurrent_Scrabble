# middle module for game


from erlport.erlterms import Atom
from erlport.erlang import set_message_handler, call, cast


import time
global game
global PID_my
global PID_players

# Starts the Scrabble game module and keeps track of current PID
def start(Pid):
    global game, PID_my, PID_players
    PID_my = Pid
    PID_players = []
    game = Game(PID_my=PID_my)

# This function takes in a player number and a message that you want to send
# to that player. It then looks up the proper PID and sends it via Erlport
def send_message(player_number, message):
    global PID_my, PID_players
    print("In middle of game's send message")
    dest = PID_players[player_number]
    # Erlport call function to send message because it spawns a new process
    call(Atom("scrabble"), Atom("send_to_pyclient"), [dest, message])

# Function needed for Erlport. Sets up the default handler for
# any messages python recieves
def register_handler(dest):
    set_message_handler(handler)
    return Atom("ok")

# Takes in message and calls the appropriate function. Message could either
# instruct to create a new player, make a move, or end the game
def handler(message):
    print("In python handler for middle_for_game")
    print(message)

    message_type = message[1]
    switcher = {
        "new player":add_player,
        "move":make_move
        # "game over":game_over
    }
    # Ensures every player has enough time to get ready
    time.sleep(5)
    switcher[message_type](message)

# Add Player to the game by saving its PID and calling the 'new_player' function
# from within the game module instance.
def add_player(message):
    print("Adding player")
    global PID_players
    PID_players.append(message[0])
    game.new_player(len(PID_players) - 1)

# Split the message given to vlarify the return values and check if the move is
# valid by calling "check_move" from within the game module instance.
def make_move(message):
    print("Making move")
    (player_number, word, direction, starting_positon,
                                        used_tiles) = split_message(message)
    game.check_move(player_number, word, starting_positon, direction,
                    used_tiles)

def game_over():
    game.end_game()

# Split message so as to clarify what each value is. Return each value
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
