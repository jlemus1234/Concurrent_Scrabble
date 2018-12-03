# middle module for game

from game import Game
from erlport.erlterms import Atom
from erlport.erlang import set_message_handler, call, cast
 
global game
global PID_my
global PID_players = []


def start(Pid):
    global game, PID_my
    game = Game()
    PID_my = Pid

def send_message(player_number, data):
    global PID_players, PID_my
    Pid_to_send = PID_players[player_number]
    message = (Pid_to_send + data)
    cast(PID_my, message)

def add_player(new_player_Pid):
    global PID_players
    game.new_player(len(PID_players))
    PID_players.append(new_player_Pid)

def resigster_handler():

    return Atom("ok")

cast(erlPID, data)
