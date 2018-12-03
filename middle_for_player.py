# middle module for player side


from player import Player
from gui import Gui

global player
global gui
global PID_my
global PID_server


def start(my_Pid, server_Pid):
    global player, gui, Pid_my, PID_server
    player = Player(Pid)
    gui = Gui()
    player.getGUI(gui)
    gui.getPlayer(player)
    # something like this
    gui.start()
    PID_my = my_Pid
    PID_server = server_Pid
    # need to now send message to server registering me


def recieve_message():
    dd

def send_message():
    dd
