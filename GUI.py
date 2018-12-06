import tkinter as tk
import tkFont
from PIL import ImageTk, Image



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
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']
        ]        

        self.hand = [' ', ' ', ' ', ' ', ' ', ' ', ' ']
        self.scores = [0, 0, 0, 0]
        self.currLetter = ' '

        self.playedTiles = []
        self.lastPlacedTile = '0'

        self.window = tk.Tk()
        self.handFrame = tk.LabelFrame(self.window, padx = 5)
        # Fonts for tiles
        self.helv16 = tkFont.Font(self.window, family='Helvetica', size=15, 
            weight=tkFont.BOLD)
        self.helv8 = tkFont.Font(self.window, family='Helvetica', size=8)

        # Images for boards
        self.tileImg           = ImageTk.PhotoImage(
            Image.open("assets/tile.png"))
        self.tripWordTileImg   = ImageTk.PhotoImage(
            Image.open("assets/3ws.png"))
        self.dubWordTileImg    = ImageTk.PhotoImage(
            Image.open("assets/2ws.png"))
        self.tripLetterTileImg = ImageTk.PhotoImage(
            Image.open("assets/3ls.png"))
        self.dubLetterTileImg  = ImageTk.PhotoImage(
            Image.open("assets/2ls.png"))
        self.centerTileImg     = ImageTk.PhotoImage(
            Image.open("assets/center.png"))

    #Button Pressed Funcs
    def clickSubmit(self):
        print 'You clicked Submit'

    def clickExchange(self):
        print 'You clicked Exchange'

    def clickPass(self):
        print 'You clicked Pass'

    def addToHand(self, letter):
        print 'added ', letter, 'to hand'

    # Clicking on the board
    def boardClicked(self, event):
        if event.widget.config()['text'][4] == ' ':
            event.widget.config(text = self.currLetter, image = self.tileImg)
            currLetter = ' '
        
        #code to extract mouse click x,y. Unneeded
        print 'mouse click  on board x, y = ', event.x, event.y
        #code to extract x,y
        for x in range(15):
            for y in range(15):
                if self.grid[x][y] == event.widget:
                    print '(x, y) = (', x, ',', y, ')'

    def boardRightClicked(self, event):
        print 'we in boardRightClicked'
        clickedLetter = event.widget.config()['text'][4]
        if clickedLetter != ' ':
            self.addToHand(clickedLetter)
            event.widget.config(text = ' ', image = self.tileImg)
            self.currLetter = ' '

    # Clicking on a tile in hand
    def handClicked(self, event):
        print 'mouse click  on handTile x, y = ', event.x, event.y
        self.currLetter = event.widget.config()['text'][4]
        print 'letter was: ', self.currLetter
        event.widget.config(text = ' ')

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
                    text = ' ', font = self.helv16, compound = tk.CENTER)
                currTile.bind("<Button-1>", self.boardClicked)
                currTile.bind("<Button-3>", self.boardRightClicked)
                #currTile.bind("<Button-1>", lambda event: lamClick(event, currLetter))
                currTile.grid(row = x, column = y)
                self.grid[x][y] = currTile


        for x in range(15):
            for y in range(15):
                print self.grid[x][y]
                
                #currTile.bind("<Button-1>", boardClicked)
    def doItAll(self):
        #Main self.window of an application
        self.window.title("Scrabble")
        self.window.geometry("1100x650")
        self.window.configure(background='grey')




        
        # Old single board code
        #boardPath         = "assets/board.png"
        #boardImg = ImageTk.PhotoImage(Image.open(boardPath))
        #board = tk.Label(self.window, image = boardImg)
        #board.bind("<Button-1>", boardClicked)

        #Score Labels
        scoreFrame = tk.LabelFrame(self.window, text="Scores")
        myScore = tk.Label(scoreFrame, text = "Score: 0")
        myScore.pack()
        enemyScore = tk.Label(scoreFrame, text = "Score: 0")
        enemyScore.pack()

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
        for i in range(5):
            singleTile = self.makeTile('o')
            singleTile.bind("<Button-1>", self.handClicked)    
            singleTile.pack(side = tk.LEFT)

        singleTile = self.makeTile('d')
        singleTile.pack(side = tk.LEFT)
        singleTile.bind("<Button-1>", self.handClicked)
        singleTile = self.makeTile('g')
        singleTile.pack(side = tk.LEFT)
        singleTile.bind("<Button-1>", self.handClicked)

        self.makeBoardGrid()
        buttonFrame.place(relx = .55, rely = 1, anchor = tk.SW)
        self.handFrame.place(relx = .60, rely = .5,)
        scoreFrame.place(relx = 1, rely = 0, anchor = tk.NE)


        #Start the GUI
        self.window.mainloop()
        print 'doItAll'
            
            



#tileFrame = tk.LabelFrame(window, height = 38, width = 38, bg = "brown")
#letterLbl = tk.Label(tileFrame, text = "  A  ", font = helv16, bg = "brown")
#pointsLbl = tk.Label(tileFrame, text = "        10", font = helv4, bg = "brown")
#letterLbl.grid(row = 0, column = 0)
#pointsLbl.grid(row = 1, column = 1)
#letterLbl.pack()
#pointsLbl.pack()


#Placing widgets on the window.
# panel.pack(side = "left", fill = "none", expand = "no")
# board.grid(row = 0, column = 0)
# handFrame.grid(row = 0, column = 2)

#main for testing
def main():
    player1Screen = Gui()
    player1Screen.doItAll()


if __name__ == '__main__':
    main()
