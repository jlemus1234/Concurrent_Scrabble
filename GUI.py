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

    #grid shared by all instances of GUI, do not modify!
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

        # self.lock = threading.Lock()

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

        # Tile representation of the GUI board
        self.tileGrid = []

        #self.hand = ['' for i in range(7)]
        self.hand = []
        self.tileHand = []
        self.scores = [0, 0, 0, 0]
        self.scoreLabels = []
        self.currLetterChar = ''
        self.currLetterTile = Tile()
        self.currPlacedTiles = []
        self.currPlacedXYs = []

        self.lastPlacedTile = ''
        self.direction = ''
        self.firstTilePlaced = ''

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

    def setPlayer(self, cur_Player):
        print("setting player")
        self.my_player = cur_Player

    def colToArray(self, colNum):
        arrayToReturn = []
        for i in range(15):
            arrayToReturn.append(self.tileGrid[i][colNum])
        return arrayToReturn

    #Button Pressed Funcs ===========-=-=-======================================-=-=-=-=-=-=-=-=-=-
    #Needs to send:
    #     tile_ray  = entire row or column being played TILES
    #     direction = 'd' or 'r'
    #     start     = (x, y) of first tile placed
    #     usedTiles = Array of used TILES
    def clickSubmit(self):
      # with self.lock:
        print 'You clicked Submit'
        rowOrCol = self.tileGrid[self.currPlacedXYs[0][0]]
        if self.direction == 'd':
            rowOrCol = colToArray(self.currPlacedXYs[0][1])
        print("about to call made_move")

        direction_curr = self.direction
        # print("direction: {}".format(direction_curr))
        currplacedXYs_curr = self.currPlacedXYs[0]
        # print("currPlacedXYs: {}".format(currplacedXYs_curr))
        currplacedTiles_curr = self.currPlacedTiles
        # print("currLetterTiles: {}".format(currplacedTiles_curr))

        print("about to make thread")
        self.my_player.made_move(rowOrCol, direction_curr, currplacedXYs_curr, currplacedTiles_curr)
        # self.my_player.made_move(rowOrCol, direction_curr,    currplacedXYs_cur, currPlacedTiles_curr)
        print 'You clicked Submit end, thread started'


    def clickExchange(self):
        print 'You clicked Exchange'

    def clickPass(self):
        print 'You clicked Pass'

    def addToHand(self, letter):
        print 'added ', letter, 'to hand'

    # Clicking on the board
    def boardClicked(self, event):
        print 'before boardClicked lock'
        # with self.lock:
        print 'got board lock'
        validMove = True
        #find current x,y
        row = 0
        col = 0

        for row in range(15):
            for col in range(15):
                if self.grid[row][col] == event.widget:
                    break;
            if self.grid[row][col] == event.widget:
                break;

        print 'after break: row, col = ', str(row), ', ', str(col)
        if len(self.currPlacedXYs) == 1:
            print self.currPlacedXYs[0]
            if self.currPlacedXYs[0][0] == row:
                self.direction = 'r'
            elif self.currPlacedXYs[0][1] == col:
                self.direction = 'd'
            else:
                validMove = False
        elif len(self.currPlacedXYs) > 1:
            print 'self.currPlacedXYs[0][0] = ', self.currPlacedXYs[0][0]
            print 'row, col = ', str(row), ', ', str(col)
            print 'self.direction = ', self.direction
            print str(self.currPlacedXYs[0][0] == row and self.direction == 'r')
            if self.currPlacedXYs[0][0] != row and self.direction == 'r':
                validMove = False
            elif self.currPlacedXYs[0][1] != col and self.direction == 'd':
                validMove = False

        #below only executed when placing in proper spotupdate
        if validMove == True:
            print 'validMove = True'
            if event.widget.config()['text'][4] == '':
                event.widget.config(text = self.currLetterTile.value, image = self.tileImg)
                #self.currLetterChar = ''

            #code to extract mouse click x,y. Unneeded
            #print 'mouse click  on board x, y = ', event.x, event.y

            #code to extract row, col
            for row in range(15):
                for col in range(15):
                    if self.grid[row][col] == event.widget:
                        print '(row, col) = (', row, ',', col, ')'
                        self.currPlacedTiles.append(self.currLetterTile)
                        self.currPlacedXYs.append([row ,col])
                        self.tileGrid[row][col] = self.currLetterTile
                        self.currLetterTile = Tile('')
            # print 'release board lock'

    def boardRightClicked(self, event):
        print 'we in boardRightClicked'
        testHand  = string_to_tiles('turtler')
        dummyScores = [2, 3, 4, 5]
        self.refresh(self.tileGrid, testHand, dummyScores)

        #clickedLetter = event.widget.config()['text'][4]
        #if clickedLetter != '':
            #self.addToHand(clickedLetter)
            #event.widget.config(text = '', image = self.tileImg)
            #self.currLetterChar = ''

    # Clicking on a tile in hand
    def handClicked(self, event):
        for i in range(len(self.hand)):
            if self.tileHand[i].value == event.widget.config()['text'][4]:
                self.currLetterTile = self.tileHand[i]
                print 'letter was: ', self.currLetterTile.value
                event.widget.config(text = '')
                self.tileHand.pop(i)
                break

    # Helper func for making tile labels
    def makeTile(self, letter):
        return Label(self.handFrame, image = self.tileImg, text = letter,
            font = self.helv16, compound = CENTER, relief = FLAT)

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
                #currTile.bind("<Button-1>", lambda event: lamClick(event, currLetter))
                currTile.grid(row = x, column = y)
                self.grid[x][y] = currTile



                #currTile.bind("<Button-1>", boardClicked)
    def start(self):
        # with self.lock:
            #Main self.window of an application
            self.window.title("Scrabble")
            self.window.geometry("1100x650")
            self.window.configure(background='grey')

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
                        singleTile = self.makeTile(str(i))
                        singleTile.bind("<Button-1>", self.handClicked)
                        singleTile.pack(side = LEFT)
                        self.hand.append(singleTile)

                self.makeBoardGrid()
                buttonFrame.place(relx = .55, rely = 1, anchor = SW)
                self.handFrame.place(relx = .60, rely = .5,)
                scoreFrame.place(relx = 1, rely = 0, anchor = NE)

            #Start the GUI
            print 'before mainloop'
            # move loop start to main, in final version the caller will need
            # to start loop after calling .start()
            self.window.mainloop()
            print 'after mainloop'

            from player import Player


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

    def drawHandTiles(self):
        i = 0
        for tile in self.tileHand:
            self.hand[i].config(text = tile.value)
            i = i + 1

    def drawScores(self):
        player = 1
        i = 0
        for score in self.scores:
            textString = 'Player ' + str(player) + ': ' + str(score)
            self.scoreLabels[i].config(text = textString)
            player = player + 1
            i = i + 1


    def refresh(self, board, hand, scores):
            print("in refresh pre lock")
            # with self.lock:
            print("in refresh post lock")
            self.tileGrid = board
            self.drawTileGrid()#done

            self.tileHand = hand
            self.drawHandTiles()#done
            self.handFrame.update()

            self.scores   = scores
            self.drawScores()#done

            #reset everything for this turn
            self.currPlacedTiles = []
            self.lastPlacedTile = ''
            self.direction = ''
            self.firstTilePlaced = []
            self.currPlacedXYs = []
            self.currPlacedTiles = []
            self.currLetterTile = Tile()
            #self.window.mainloop()
            print("gave back lock in refresh")
            self.window.update()
            print("done with update")


#main for testing
def main():
    player1Screen = Gui()
    player1Screen.start()
    testBoard = Board()
    testHand  = string_to_tiles('rabbitr')
    dummyScores = [100, 12, 34, 56]

    #player1Screen.drawScores(dummyScores)
    print 'calling player1Screen'
    player1Screen.refresh(testBoard.get_board(), testHand, dummyScores)
    #player1Screen.window.mainloop()

    testHand  = string_to_tiles('turtler')
    dummyScores = [2, 3, 4, 5]
    player1Screen.refresh(testBoard.get_board(), testHand, dummyScores)


if __name__ == '__main__':
    main()
