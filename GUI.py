import tkinter as tk
import tkFont
from PIL import ImageTk, Image
from player import Player
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

        self.tileGrid = []

        self.hand = []
        self.tileHand = []
        self.scores = [0, 0, 0, 0]
        self.scoreLabels = []
        self.currLetter = ''
        self.currPlacedTiles = []

        self.lastPlacedTile = ''
        self.direction = ''
        self.firstTilePlaced = ''

        self.window = tk.Tk()
        self.handFrame = tk.LabelFrame(self.window, padx = 5)
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

    def setPlayer(self, Player):
        self.player = Player

    #Button Pressed Funcs ===========-=-=-======================================-=-=-=-=-=-=-=-=-=-
    #Needs to send:
    #     tile_ray  = entire row or column being played TILES
    #     direction = 'd' or 'r'
    #     start     = (x, y) of first tile placed
    #     usedTiles = Array of used TILES
    def clickSubmit(self):
        player.make_move(tile_ray = self.tileGrid[7], direction = 'r', 
                         start = (0,0), usedTiles = string_to_tiles('rabb'))
        print 'You clicked Submit'
        self.window.quit()

    def clickExchange(self):
        print 'You clicked Exchange'

    def clickPass(self):
        print 'You clicked Pass'

    def addToHand(self, letter):
        print 'added ', letter, 'to hand'

    # Clicking on the board
    def boardClicked(self, event):
        if event.widget.config()['text'][4] == '':
            event.widget.config(text = self.currLetter, image = self.tileImg)
            currLetter = ''

        #code to extract mouse click x,y. Unneeded
        #print 'mouse click  on board x, y = ', event.x, event.y

        #code to extract x,y
        for x in range(15):
            for y in range(15):
                if self.grid[x][y] == event.widget:
                    print '(x, y) = (', x, ',', y, ')'

    def boardRightClicked(self, event):
        print 'we in boardRightClicked'
        clickedLetter = event.widget.config()['text'][4]
        if clickedLetter != '':
            self.addToHand(clickedLetter)
            event.widget.config(text = '', image = self.tileImg)
            self.currLetter = ''

    # Clicking on a tile in hand
    def handClicked(self, event):
        print 'mouse click  on handTile x, y = ', event.x, event.y
        for tile in self.hand:
            if tile.value == event.widget.config()['text'][4]:
                self.hand.remove(tile)
                self.currLetter = tile
                print 'letter was: ', self.currLetter.value
                event.widget.config(text = '')
                break

    # Helper func for making tile labels
    def makeTile(self, letter):
        return tk.Label(self.handFrame, image = self.tileImg, text = letter,
            font = self.helv16, compound = tk.CENTER, relief = tk.FLAT)

    def lamClick(self, event = None, letter = 's'):
        print 'mouse click  on board x, y = ', event.x, event.y
        #event.widget.config(text = currLetter, image = tileImg)

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
                currTile = tk.Label(self.window, image = tileDict[self.initGrid[x][y]],
                    text = '', font = self.helv16, compound = tk.CENTER)
                currTile.bind("<Button-1>", self.boardClicked)
                currTile.bind("<Button-3>", self.boardRightClicked)
                #currTile.bind("<Button-1>", lambda event: lamClick(event, currLetter))
                currTile.grid(row = x, column = y)
                self.grid[x][y] = currTile


        for x in range(15):
            for y in range(15):
                print self.grid[x][y]

                #currTile.bind("<Button-1>", boardClicked)
    def start(self):
        #Main self.window of an application
        self.window.title("Scrabble")
        self.window.geometry("1100x650")
        self.window.configure(background='grey')

        #Score Labels
        scoreFrame = tk.LabelFrame(self.window, text="Scores")
        for score in self.scores:
            scoreLabel = tk.Label(scoreFrame, text = '')
            scoreLabel.pack()
            self.scoreLabels.append(scoreLabel)

        #Submit Buttons - Submit, Exchange, Pass
        buttonFrame = tk.Frame(self.window)
        submitBtn = tk.Button(buttonFrame, text = "Submit",
            command = self.clickSubmit)
        exchangeBtn = tk.Button(buttonFrame, text = "Exhange",
            command = self.clickExchange)
        passBtn = tk.Button(buttonFrame, text = "Pass",
            command = self.clickPass)
        submitBtn.pack(side = tk.LEFT)
        exchangeBtn.pack(side = tk.LEFT)
        passBtn.pack(side = tk.LEFT)

        #Tiles in hand
        for i in range(7):
            singleTile = self.makeTile('')
            singleTile.bind("<Button-1>", self.handClicked)
            singleTile.pack(side = tk.LEFT)
            self.hand.append(singleTile)

        self.makeBoardGrid()
        buttonFrame.place(relx = .55, rely = 1, anchor = tk.SW)
        self.handFrame.place(relx = .60, rely = .5,)
        scoreFrame.place(relx = 1, rely = 0, anchor = tk.NE)


        #Start the GUI
        print 'before mainloop'
        #self.window.mainloop()
        print 'after mainloop'


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
        self.tileGrid = board
        self.drawTileGrid()#done

        self.tileHand = hand
        self.drawHandTiles()#done

        self.scores   = scores
        self.drawScores()#done

        #reset everything for this turn
        self.currPlacedTiles = []
        self.lastPlacedTile = ''
        self.direction = ''
        self.firstTilePlaced = []

#main for testing
def main():
    player1Screen = Gui()
    player1Screen.start()
    testBoard = Board()
    testHand  = string_to_tiles('rabbitr')
    dummyScores = [100, 12, 34, 56]
    while True:
        #player1Screen.drawScores(dummyScores)
        print 'calling player1Screen'
        player1Screen.refresh(testBoard.get_board(), testHand, dummyScores)
        player1Screen.window.mainloop()
        testHand  = string_to_tiles('turtler')
        dummyScores = [2, 3, 4, 5]
        player1Screen.refresh(testBoard.get_board(), testHand, dummyScores)


if __name__ == '__main__':
    main()
