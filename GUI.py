import sys
if sys.version_info[0] == 2:
    from Tkinter import *
else:
    from tkinter import *
from mttkinter import mtTkinter


import threading
import tkFont
from PIL import ImageTk, Image

from tile import Tile
from tile import string_to_tiles
from board import Board
#python 2.712

class Gui:
    
    initGrid = [
            ['3w','x','x','2l','x','x','x','3w','x','x','x','2l','x','x','3w'],
            ['x','2w','x','x','x','3l','x','x','x','3l','x','x','x','2w','x'],
            ['x','x','2w','x','x','x','2l','x','2l','x','x','x','2w','x','x'],
            ['2l','x','x','2w','x','x','x','2l','x','x','x','2w','x','x','2l'],
            ['x','x','x','x','2w','x','x','x','x','x','2w','x','x','x','x'],
            ['x','3l','x','x','x','3l','x','x','x','3l','x','x','x','3l','x'],
            ['x','x','2l','x','x','x','2l','x','2l','x','x','x','2l','x','x'],
            ['3w','x','x','2l','x','x','x','c','x','x','x','2l','x','x','3w'],
            ['x','x','2l','x','x','x','2l','x','2l','x','x','x','2l','x','x'],
            ['x','3l','x','x','x','3l','x','x','x','3l','x','x','x','3l','x'],
            ['x','x','x','x','2w','x','x','x','x','x','2w','x','x','x','x'],
            ['2l','x','x','2w','x','x','x','2l','x','x','x','2w','x','x','2l'],
            ['x','x','2w','x','x','x','2l','x','2l','x','x','x','2w','x','x'],
            ['x','2w','x','x','x','3l','x','x','x','3l','x','x','x','2w','x'],
            ['3w','x','x','2l','x','x','x','3w','x','x','x','2l','x','x','3w']
        ]

    def __init__(self, grid = '', hand = '', scores = ''):

        # Labels of the board for GUI
        self.grid = [
            ['','','','','','','','','','','','','','',''],
            ['','','','','','','','','','','','','','',''],
            ['','','','','','','','','','','','','','',''],
            ['','','','','','','','','','','','','','',''],
            ['','','','','','','','','','','','','','',''],
            ['','','','','','','','','','','','','','',''],
            ['','','','','','','','','','','','','','',''],
            ['','','','','','','','','','','','','','',''],
            ['','','','','','','','','','','','','','',''],
            ['','','','','','','','','','','','','','',''],
            ['','','','','','','','','','','','','','',''],
            ['','','','','','','','','','','','','','',''],
            ['','','','','','','','','','','','','','',''],
            ['','','','','','','','','','','','','','',''],
            ['','','','','','','','','','','','','','','']
        ]

        # Tile representation of various GUI elements
        self.tileGrid = []
        self.tileHand = []
        self.currLetterTile = Tile()
        self.currPlacedTiles = []      
        
        self.hand = []
        self.scores = [0, 0, 0, 0]
        self.scoreLabels = []
        self.currLetterChar = ''
        self.currPlacedXYs = []
        self.direction = ''

        # The main GUI elements
        self.window = Tk()
        self.handFrame = LabelFrame(self.window, padx = 5)
        
        # Fonts for tiles
        self.helv16 = tkFont.Font(self.window, family='Helvetica', size=15,
            weight=tkFont.BOLD)
        self.helv8 = tkFont.Font(self.window, family='Helvetica', size=8)

        # Images for boards
        self.tileImg           = ImageTk.PhotoImage(
            Image.open("./assets/tile.png"))
        self.tripWordTileImg   = ImageTk.PhotoImage(
            Image.open("./assets/3ws.png"))
        self.dubWordTileImg    = ImageTk.PhotoImage(
            Image.open("./assets/2ws.png"))
        self.tripLetterTileImg = ImageTk.PhotoImage(
            Image.open("./assets/3ls.png"))
        self.dubLetterTileImg  = ImageTk.PhotoImage(
            Image.open("./assets/2ls.png"))
        self.centerTileImg     = ImageTk.PhotoImage(
            Image.open("./assets/center.png"))
        self.legendImg         = ImageTk.PhotoImage(
            Image.open("./assets/legend.png"))
        
    def setPlayer(self, cur_Player):
        self.my_player = cur_Player

    # returns a tile array that corresponds to all the tiles in a single column
    #   of tileGrid where column = colNum
    def colToArray(self, colNum):
        arrayToReturn = []
        for i in range(15):
            arrayToReturn.append(self.tileGrid[i][colNum])
        return arrayToReturn

    # calls Player().made_move() with information about the current game state.
    def clickSubmit(self):
        if len(self.currPlacedTiles) > 1:
            rowOrCol = self.tileGrid[self.currPlacedXYs[0][0]]
            if self.direction == 'd':
                rowOrCol = self.colToArray(self.currPlacedXYs[0][1])

            direction_curr = self.direction
            currplacedXYs_curr = self.currPlacedXYs[0]
            currplacedTiles_curr = self.currPlacedTiles

            self.my_player.made_move(rowOrCol, direction_curr, currplacedXYs_curr, currplacedTiles_curr)

    # Code to be executed when Exchange button is clicked
    def clickExchange(self):
        None

    # Code to be executed when Pass button is clicked
    def clickPass(self):
        None
        
    # Clicking on the board
    def boardClicked(self, event):
        validMove = True
        row = 0
        col = 0
        
        # nested loops to find row and column of clicked tile
        for row in range(15):
            for col in range(15):
                if self.grid[row][col] == event.widget:
                    break;
            if self.grid[row][col] == event.widget:
                break;
        
        if len(self.currPlacedXYs) == 1:
        # figures out if player is making a word along the x or y axis and
        #    sets self.direction to r or d respectively.
            if self.currPlacedXYs[0][0] == row:
                self.direction = 'r'
            elif self.currPlacedXYs[0][1] == col:
                self.direction = 'd'
            else:
                validMove = False
        # makes sure player is placing the current tile in the same row or column
        #    as previously placed tiles
        elif len(self.currPlacedXYs) > 1:
            if self.currPlacedXYs[0][0] != row and self.direction == 'r':
                validMove = False
            elif self.currPlacedXYs[0][1] != col and self.direction == 'd':
                validMove = False

        #below only executed when placing in valid spot
        if validMove == True:
            if event.widget.config()['text'][4] == '':
                event.widget.config(text = self.currLetterTile.value, image = self.tileImg)

            # records information about correctly placed tile:
            #    appends row, col coordinates of placed tile to self.currPlacedXYs
            #    appends the placed tile to self.currPlacedTiles
            # updates label on window to diplay newly placed tile
            # resets self.currLetterTile to hold an empty tile
            for row in range(15):
                for col in range(15):
                    if self.grid[row][col] == event.widget:
                        self.currPlacedTiles.append(self.currLetterTile)
                        self.currPlacedXYs.append([row ,col])
                        self.tileGrid[row][col] = self.currLetterTile
                        self.currLetterTile = Tile('')


    # Debug function that makes a favorable game state
    def boardRightClicked(self, event):
        testHand  = string_to_tiles('turtles')
        dummyScores = [2, 3, 4, 5]
        self.refresh(self.tileGrid, testHand, dummyScores)
            

    # Clicking on a tile in hand
    def handClicked(self, event):
        for i in range(len(self.hand)):
            if self.tileHand[i].value == event.widget.config()['text'][4]:
                self.currLetterTile = self.tileHand[i]
                event.widget.config(text = '')
                self.tileHand.pop(i)
                break

    # Helper func for making tile labels
    def makeTile(self, letter):
        return Label(self.handFrame, image = self.tileImg, text = letter,
            font = self.helv16, compound = CENTER, relief = FLAT)

    # helper function used to make 15x15 grid of Labels
    # displayed on window
    def makeBoardGrid(self):
        tileDict = {
            '3l': self.tripLetterTileImg,
            '2l': self.dubLetterTileImg,
            '3w': self.tripWordTileImg,
            '2w': self.dubWordTileImg,
            'c' : self.centerTileImg,
            'x' : self.tileImg
        }

        for x in range(15):
            for y in range(15):
                currTile = Label(self.window, image = tileDict[self.initGrid[x][y]],
                    text = '', font = self.helv16, compound = CENTER)
                currTile.bind("<Button-1>", self.boardClicked)
                currTile.bind("<Button-3>", self.boardRightClicked)
                currTile.grid(row = x, column = y)
                self.grid[x][y] = currTile

    # call after initializing an instance of GUI.
    # sets the widgets to display a blank game state
    def start(self):
            #Main self.window of an application
            self.window.title("Scrabble")
            self.window.geometry("1100x650")
            self.window.configure(background='SteelBlue1')

            #Score Labels
            scoreFrame = LabelFrame(self.window, text="Scores")
            for score in self.scores:
                scoreLabel = Label(scoreFrame, text = '')
                scoreLabel.pack()
                self.scoreLabels.append(scoreLabel)

                #Submit Buttons - Submit, Exchange, Pass
                buttonFrame = Frame(self.window)
                submitBtn = Button(buttonFrame, text = "Submit", command = self.clickSubmit)
                exchangeBtn = Button(buttonFrame, text = "Exhange", command = self.clickExchange)
                passBtn = Button(buttonFrame, text = "Pass", command = self.clickPass)
                submitBtn.pack(side = LEFT)
                exchangeBtn.pack(side = LEFT)
                passBtn.pack(side = LEFT)

                #Tiles in hand
                if self.hand == []:
                    for i in range(7):
                        singleTile = self.makeTile('')
                        singleTile.bind("<Button-1>", self.handClicked)
                        singleTile.pack(side = LEFT)
                        self.hand.append(singleTile)

                #Make legend
                legendLabel = Label(self.window, image = self.legendImg,
                    text = '', font = self.helv16, compound = CENTER)
                legendLabel.place(relx = .90, rely = .4,)
                
                
                self.makeBoardGrid()
                buttonFrame.place(relx = .55, rely = 1, anchor = SW)
                self.handFrame.place(relx = .60, rely = .5,)
                scoreFrame.place(relx = 1, rely = 0, anchor = NE)

            #Start the GUI
            self.window.mainloop()
            
            from player import Player

    # updates screen to display the board held in self.tileGrid
    def drawTileGrid(self):
        tileDict = {
            '3l': self.tripLetterTileImg,
            '2l': self.dubLetterTileImg,
            '3w': self.tripWordTileImg,
            '2w': self.dubWordTileImg,
            'c' : self.centerTileImg,
            'x' : self.tileImg
        }

        for row in range(15):
            for col in range(15):
                if self.tileGrid[row][col].value == '':
                    tileBack = tileDict[self.initGrid[row][col]]
                else:
                    tileBack = self.tileImg
                self.grid[row][col].config(text = self.tileGrid[row][col].value, image = tileBack)

    # updates the hand tiles displayed on screen
    def drawHandTiles(self):
        i = 0
        for tile in self.tileHand:
            self.hand[i].config(text = tile.value)
            i = i + 1

    # updates the scores displayed on screen
    def drawScores(self):
        player = 1
        i = 0
        for score in self.scores:
            textString = 'Player ' + str(player) + ': ' + str(score)
            self.scoreLabels[i].config(text = textString)
            player = player + 1
            i = i + 1


    # refreshes the screen to display the information passed
    # in. board is a 2d array of Tiles. Hand is an array of Tiles.
    # scores is an int array with four elements
    def refresh(self, board, hand, scores):
            self.tileGrid = board
            self.drawTileGrid()

            self.tileHand = hand
            self.drawHandTiles()
            self.handFrame.update()

            self.scores   = scores
            self.drawScores()

            #reset everything for next turn
            self.currPlacedTiles = []
            self.direction = ''
            self.currPlacedXYs = []
            self.currPlacedTiles = []
            self.currLetterTile = Tile()
            
            #update the screen
            self.window.update()
            
            

#main for testing
def main():
    player1Screen = Gui()
    player1Screen.start()
    testBoard = Board()
    testHand  = string_to_tiles('rabbitr')
    dummyScores = [100, 12, 34, 56]

    print 'calling player1Screen'
    player1Screen.refresh(testBoard.get_board(), testHand, dummyScores)

    testHand  = string_to_tiles('turtler')
    dummyScores = [2, 3, 4, 5]
    player1Screen.refresh(testBoard.get_board(), testHand, dummyScores)


if __name__ == '__main__':
    main()
