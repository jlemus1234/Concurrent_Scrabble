# middle module for player side


from player import Player
from GUI import Gui
from erlport.erlterms import Atom
from erlport.erlang import set_message_handler, call, cast, self as selfPID
from tile import Tile
import threading

global player
global gui
global PID_my # python instance's parent pid
global PID_server # pid of game server


def start(my_Pid, server_Pid):
    global player, gui, PID_my, PID_server
    PID_my = my_Pid
    PID_server = server_Pid

    gameThread = threading.Thread(target = start_gui)
    gameThread.start()
    # send start message
    #send_message((PID_server, "new player"))
    send_message(PID_server, (selfPID(), "new player")) # Sending the python instance's pid right now
    #cast(PID
    print("calling player start")


def start_gui():
    global player, gui
    player = Player("Player",PID_server)
    gui = Gui()
    player.setGUI(gui)
    gui.setPlayer(player)
    # something like this
    gui.start()

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
    # getting rid of PID of destination
    print("inside middle_for_player handler")
    print("This is the original message: {}".format(message))
    message = message[1:]
    message_type = message[0]
    switcher = {
        "tiles":new_tiles_func,
        "refresh":refresh_func
        # "report_winner":winner,
        # "end":end_game
    }
    new_message = message[1:]
    print("this is the new message: {}".format(new_message))
    switcher[message_type](new_message)

def send_message(dest_pid, message):
    global PID_my, PID_server
    print("Sending message from middle_for_player")
    call(Atom("scrabble"), Atom("send_messages"), [dest_pid, message])
    print("Sent message from m_f_p")
    #cast(PID_server, message) # does send to the game server, but not through gen server (unhandled)
    #cast(PID_my, (PID_server, PID_my, message)) #original


def split_message_player_side(message):
    board       = message[0]
    scores      = message[1]
    old_tiles   = message[2]
    new_tiles   = message[3]
    return status, board, scores, old_tiles
#new_tiles

def refresh_func(message):
    board, scores, old_tiles_tup, new_tiles_tup = split_message_player_side(message)

    global player
    tile_board = [[Tile("","","","",tile_tup) for tile_tup in row] for row in board]

    player.refresh(tile_board, score)

def new_tiles_func(message):
    board, scores, old_tiles_tup, new_tiles_tup = split_message_player_side(message)

    global player

    new_tiles = []
    for tile_tup in new_tiles_tup:
         new_tiles.append(Tile("","","","",tile_tup))

    old_tiles = []
    for tile_tup_old in old_tiles_tup:
        old_tiles.append(Tile("","","","",tile_tup_old))

    #tile_board = [[Tile("","","","",tile_tup) for tile_tup in row] for row in board]

    player.get_new_tiles(old_tiles, new_tiles)
