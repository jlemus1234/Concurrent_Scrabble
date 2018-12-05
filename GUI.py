import tkinter as tk
import tkFont
from PIL import ImageTk, Image

currLetter = 'f'


grid = [
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

class Gui:

    def __init__(self, grid, hand, scores):
        self.grid = [
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                 '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                 '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                 '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                 '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                 '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                 '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                 '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                 '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                 '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                 '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                 '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                 '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                 '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                 '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                 '.', '.']
           ]
        self.hand = ['.', '.', '.', '.', '.', '.', '.']
        self.scores = [0, 0, 0, 0]


#This creates the main window of an application
window = tk.Tk()
window.title("Scrabble")
window.geometry("1100x600")
window.configure(background='grey')

helv16 = tkFont.Font(window, family='Helvetica', size=15, weight=tkFont.BOLD)
helv4 = tkFont.Font(window, family='Helvetica', size=8)

boardPath         = "assets/board.png"
tileImg           = ImageTk.PhotoImage(Image.open("assets/tile.png"))
tripWordTileImg   = ImageTk.PhotoImage(Image.open("assets/3ws.png"))
dubWordTileImg    = ImageTk.PhotoImage(Image.open("assets/2ws.png"))
tripLetterTileImg = ImageTk.PhotoImage(Image.open("assets/3ls.png"))
dubLetterTileImg  = ImageTk.PhotoImage(Image.open("assets/2ls.png"))
centerTileImg     = ImageTk.PhotoImage(Image.open("assets/center.png"))

#Creates a Tkinter-compatible photo image, which can be
# used everywhere Tkinter expects an image object.
boardImg = ImageTk.PhotoImage(Image.open(boardPath))
board = tk.Label(window, image = boardImg)

#Score Labels
scoreFrame = tk.LabelFrame(window, text="Scores")
myScore = tk.Label(scoreFrame, text = "Score: 0")
myScore.pack()
enemyScore = tk.Label(scoreFrame, text = "Score: 0")
enemyScore.pack()


#Button Pressed Funcs
def clickSubmit():
    print 'You clicked Submit'

def clickExchange():
    print 'You clicked Exchange'

def clickPass():
    print 'You clicked Pass'

def boardClicked(event):
    print 'mouse click  on board x, y = ', event.x, event.y
    event.widget.bind("<Button-1>")
    event.widget.config(text = currLetter, image = tileImg)

def handClicked(event):
    print 'mouse click  on handTile x, y = ', event.x, event.y
    currLetter = event.widget.config()['text'][4]
    print 'letter was: ', currLetter
    event.widget.config(text = 'w')

#board.bind("<Button-1>", boardClicked)

#Submit Buttons - Submit, Exchange, Pass
buttonFrame = tk.Frame(window)
submitBtn = tk.Button(buttonFrame, text = "Submit", command = clickSubmit)
exchangeBtn = tk.Button(buttonFrame, text = "Exhange", 
    command = clickExchange)
passBtn = tk.Button(buttonFrame, text = "Pass", command = clickPass)
submitBtn.pack(side = tk.LEFT)
exchangeBtn.pack(side = tk.LEFT)
passBtn.pack(side = tk.LEFT)

def makeTile(letter):
    return tk.Label(handFrame, image = tileImg, text = letter, font = helv16, 
                        compound = tk.CENTER, relief = tk.FLAT)


#Tiles in hand
handFrame = tk.LabelFrame(window, padx = 5)
for i in range(5):
    singleTile = makeTile('o')
    singleTile.bind("<Button-1>", handClicked)    
    singleTile.pack(side = tk.LEFT)

singleTile = makeTile('d')
singleTile.pack(side = tk.LEFT)
singleTile.bind("<Button-1>", handClicked)
singleTile = makeTile('g')
singleTile.pack(side = tk.LEFT)
singleTile.bind("<Button-1>", handClicked)

def lamClick(event = None, letter = 's'):
    print 'mouse click  on board x, y = ', event.x, event.y
    #event.widget.config(text = currLetter, image = tileImg)

def makeBoardGrid():
    tileDict = {
        '3l': tripLetterTileImg,
        '2l': dubLetterTileImg,
        '3w': tripWordTileImg,
        '2w': dubWordTileImg,
        'c': centerTileImg,
        'x': tileImg
    }
    for x in range(15):
        for y in range(15):
            currTile = tk.Label(window, image = tileDict[grid[x][y]], 
                text = ' ', font = helv16, compound = tk.CENTER)
            currTile.bind("<Button-1>", boardClicked)
            #currTile.bind("<Button-1>", lambda event: lamClick(event, currLetter))
            currTile.grid(row = x, column = y)
            grid[x][y] = currTile
            
            #currTile.bind("<Button-1>", boardClicked)
            
            



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
makeBoardGrid()
buttonFrame.place(relx = .55, rely = 1, anchor = tk.SW)
handFrame.place(relx = .60, rely = .5,)
#handFrame.grid(row = 0, column = 2)
scoreFrame.place(relx = 1, rely = 0, anchor = tk.NE)


#Start the GUI
window.mainloop()



                



