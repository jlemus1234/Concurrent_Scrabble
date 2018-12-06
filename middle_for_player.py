# middle module for player side


from player import Player
from GUI import Gui
from erlport.erlterms import Atom
from erlport.erlang import set_message_handler, call, cast
from tile import Tile
import threading

global player
global gui
global PID_my # python instance's pid
global PID_server # pid of erlport instance that launched this


def start(my_Pid, server_Pid):
    global player, gui, Pid_my, PID_server
    PID_my = my_Pid
    PID_server = server_Pid

    gameThread = threading.Thread(target = start_gui)
    gameThread.start()

    print("calling player start")


def start_gui():
    global player, gui
    player = Player("Player1",PID_server)
    gui = Gui()
    player.setGUI(gui)
    gui.setPlayer(player)
    # something like this
    gui.doItAll()

    ## This creates the game loop that the game doesn't return from. 
    ## must launch this from a different thread.


    #send_message(("new player", PID_my))
    print("player start finished")
    # need to now send message to server registering me



def register_handler(dest):
    # no need to hold on to dest (the PID from which the message was sent)
    # because it will stay const and was set in start
    print("setting client handler")
    set_message_handler(handler)
    return Atom("ok")

# need to add more funcitons
def handler(message):
    message_type = message[0]
    switcher = {
        "success":success_func,
        "refresh":refresh_func
        # "report_winner":winner,
        # "end":end_game
    }
    switcher[message_type](message[1:])

def send_message(data):
    global PID_players, PID_my
    message = (Pid_to_send + data)
    cast(PID_server, message)




def split_message_player_side(message):
    board       = message[0]
    scores      = message[1]
    old_tiles   = message[2]
    new_tiles   = message[3]
    return status, board, scores, old_tiles,
#new_tiles

def refresh_func(message):
    board, scores, old_tiles_tup, new_tiles_tup = split_message_player_side(message)

    global player
    tile_board = [[Tile("","","","",tile_tup) for tile_tup in row] for row in board]

    player.refresh_failure(tile_board, score)

def success_func(message):
    board, scores, old_tiles_tup, new_tiles_tup = split_message_player_side(message)

    global player

    tiles = []
    for tile_tup in new_tiles_tup:
         tiles.append(Tile("","","","",tile_tup))
    tile_board = [[Tile("","","","",tile_tup) for tile_tup in row] for row in board]

    player.refresh(tile_board, score, tiles)
