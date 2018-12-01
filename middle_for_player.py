# middle module for player side


from player import Player
from gui import Gui

player
gui

def start(Pid):
    player = Player(Pid)
    gui = Gui()
    player.getGUI(gui)
    gui.getPlayer(player)
    # something like this
    gui.start()


def recieve_message():
    dd

def send_message():
    dd
