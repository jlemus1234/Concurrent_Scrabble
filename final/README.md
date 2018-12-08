# Quadruple Score
##### A game based on scrabble in which players race to put down tiles rather than take turns

### Made by:
    * Billy Witrock
    * Saad Mazhar
    * Irving Pena
    * Jose Ortiz

## Guide to Files and folder

#### assets
    * The assets folder contains images needed to run the GUI

#### erlport
    * The erlport folder contains our version of erlport that we are using.
    Some of the files have been modified from the original files on the
    Github repository

#### mttkinter
    * This folder contains all files needed to run mttkinter, which is the
    package we chose to use for our GUI

* bag.py
    * bag.py contains the Bag class which holds on to all the tiles in the
    game that are not in players hands or on the board
* board.py
    * board.py contains the Board class which keeps an instance of the board.
    The board, when given a move, checks its spelling before scoring, and adding
    it to the board
* game.py
    * game.py contains the Game class. The game class keeps track of the game
    state on the server side. It holds the bag of tiles and the master board.
* GUI.py
    * GUI.py contains the GUI class. The GUI class interacts directly with
    mttkinter to make the GUI appear. It also preforms basic game logic such as
    not letting users place tiles that are not in the same row or column
* middle_for_game.py
    * middle_for_game.py is a module that acts as the bridge between Erlport
    and the Game class.
* middle_for_player.py
    * middle_for_player.py is a module that acts as the  bridge between Erlport
    and the Player class. It also creates the instance of the GUI on each
    user's computer
* player.py
    * player.py contains the Player class. The Player class interacts with its
    own board, and the GUI. The Player class also gets called when another
    player makes a move and the game state needs to be updated
* scrabble.erl
    * scrabble.erl our only erlang module. It handles all aspects that makes
    the game distributed. It has functions to start the game, send messages,
    and receive messages
* tile.py
    * tile.py contains the Tile class. The Tile class is used to represent a
    single scrabble Tile. It is used by every python class and
    middle_for_player.
* twl.py
    * twl.py is the scrabble dictionary that we are using to validate words. We
    found this module on Github
