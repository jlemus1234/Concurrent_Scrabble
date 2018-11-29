import tkinter as tk
import tkFont
from PIL import ImageTk, Image



#This creates the main window of an application
window = tk.Tk()
window.title("Scrabble")
window.geometry("1100x600")
window.configure(background='grey')

helv16 = tkFont.Font(window, family='Helvetica', size=15, weight=tkFont.BOLD)
helv4 = tkFont.Font(window, family='Helvetica', size=8)

boardPath = "board.png"

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

#Submit Buttons - Submit, Exchange, Pass
buttonFrame = tk.Frame(window)
submitBtn = tk.Button(buttonFrame, text = "Submit", command = clickSubmit)
exchangeBtn = tk.Button(buttonFrame, text = "Exhange", command = clickExchange)
passBtn = tk.Button(buttonFrame, text = "Pass", command = clickPass)
submitBtn.pack(side = tk.LEFT)
exchangeBtn.pack(side = tk.LEFT)
passBtn.pack(side = tk.LEFT)


#Tiles
tileFrame = 

#tileFrame = tk.LabelFrame(window, height = 38, width = 38, bg = "brown")
#letterLbl = tk.Label(tileFrame, text = "  A  ", font = helv16, bg = "brown")
#pointsLbl = tk.Label(tileFrame, text = "        10", font = helv4, bg = "brown")
#letterLbl.grid(row = 0, column = 0)
#pointsLbl.grid(row = 1, column = 1)
#letterLbl.pack()
#pointsLbl.pack()


#Placing widgets on the window.
# panel.pack(side = "left", fill = "none", expand = "no")
board.grid(row = 0, column = 0)
buttonFrame.place(relx = .55, rely = 1, anchor = tk.SW)
tileFrame.grid(row = 0, column = 1)
scoreFrame.place(relx = 1, rely = 0, anchor = tk.NE)


#Start the GUI
window.mainloop()

