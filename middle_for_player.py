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

    # sends message back to server saying we want to play
    send_message(PID_server, (PID_my, "new player"))

# Think we can delete this later
# def send_message_helper(message):
#     send_message(PID_server, message)

# This is used to start up the player and gui
def start_gui():
    global player, gui, PID_server, PID_my
    player = Player("Player", PID_server, PID_my)
    gui = Gui()
    player.setGUI(gui)
    gui.setPlayer(player)
    gui.start()

# function needed for Erlport
# sets up the default handler for any messages python recieves
def register_handler(dest):
    set_message_handler(handler)
    return Atom("ok")

# our handler that all messages pass through
def handler(message):
    print("inside middle_for_player handler")
    print(message)
    thread = threading.Thread(target=handler_helper, args=(message))
    thread.daemon = True
    thread.start()

# this is our helper function for the handler
# It is used as targets of threads so we can handle multiple requests
# that may eventually call gui.refresh which starts an infinite loop
def handler_helper(message_type, board, scores, old_tiles, new_tiles):
    print("in other thread")
    switcher = {
        "tiles":new_tiles_func,
        "refresh":refresh_func
    }
    switcher[message_type](board, scores, old_tiles, new_tiles)

# sends message from the player to the given PID, in this case, the server
def send_message(dest_pid, message):
    print("Sending message from middle_for_player")
    retvalue = call(Atom("scrabble"), Atom("send_messages"), [dest_pid, message])
    print(retvalue)
    print("Sent message from m_f_p")


# function that takes in a message that a player may recieve, and breaks it
# splits it up into its compounents
def split_message_player_side(message):
    board       = message[0]
    scores      = message[1]
    old_tiles   = message[2]
    new_tiles   = message[3]
    return board, scores, old_tiles, new_tiles

# function used when the message recieved has the keyword "refresh"
# this means the message contains information about a new board and new scores
def refresh_func(board, scores, old_tiles_tup, new_tiles_tup):
    print("in refresh_func middle_for_player")
    global player
    tile_board = [[Tile("","","","",tile_tup) for tile_tup in row]
                                                for row in board]
    player.refresh(tile_board, scores)

# function used when the message recieved has the keyword "tiles"
# this means the message contains information about a new tiles and old tiles
def new_tiles_func(board, scores, old_tiles_tup, new_tiles_tup):
    print("in new_tiles_func middle_for_player")
    global player
    new_tiles = []
    for tile_tup in new_tiles_tup:
         new_tiles.append(Tile("","","","",tile_tup))

    old_tiles = []
    for tile_tup_old in old_tiles_tup:
        old_tiles.append(Tile("","","","",tile_tup_old))

    player.get_new_tiles(old_tiles, new_tiles)
