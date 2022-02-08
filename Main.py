from curses import window
from curses.ascii import isdigit
import tkinter as tk
import random
import datetime

from numpy import append

goalWord = ""
currentGuess = ''
previousGuesses = []

# sets goal word to random word from file of length x
def getWord(filename, length):
    # Read file
    fileObj = open(filename, "r")   # open file in read mode
    allWords = fileObj.read().splitlines()  # put all files into array
    fileObj.close()

    # get all words of length x
    words = [""]
    for i in range(len(allWords)):
        if (len(allWords[i]) == length):
            words.append(allWords[i])

    # set seed and pick random word
    current_date = datetime.datetime.now()
    random.seed(current_date.hour * current_date.minute * current_date.second)
    
    global goalWord
    goalWord = words[random.randint(0,len(words))].upper()

    print(goalWord)
    


def clearRow(i):

    string = 'current&&row' + str(i)
    canvas.delete('current&&row')

# Function call when backspace is pressed
def onBackspacePress(event):
    global currentGuess
    # slice off last element, clear row & redraw
    currentGuess = currentGuess[:-1]
    clearRow(1)
    create_row(canvas, 600, 500, 0, currentGuess.upper(), "row0", False)

# Handle key press
def onKeyPress(event):

    if( len(currentGuess) == 6):
        return

    character = event.char

    if( character.isalpha() ):
        update_row(character)

def onReturnPress(event):
    global currentGuess

    if ( len(currentGuess) != 6 ):
        return

    # add current guess to start of guess list
    previousGuesses.insert(0,currentGuess)
    # clear current guess
    currentGuess = ''

    # redraw empty first row
    clearRow(0)
    create_row(canvas, 600, 500, 0, currentGuess.upper(), "row0", False)

    # draw row for all previous guesses
    for i in range( len(previousGuesses)):
        row = 'row' + str(i+1)
        create_row(canvas, 600, 500, i+1, previousGuesses[i].upper(), row, True)
    

def update_row(character):
    global currentGuess
    
    # add new character, clear row and redraw
    currentGuess += character
    clearRow(1)
    create_row(canvas, 600, 500, 0, currentGuess.upper(), "row1", False)

# Display row
def create_row(canvas, canvas_width, canvas_height, row_id, guess, tag, checkcolour):
    global goalWord

    for i in range(6):

        # initialise tags
        tags = (tag,)

        # Calculate location to draw onscreen
        box_width = 50
        box_height = 50
        margin = 4
        x_start = (canvas_width/2) - 3*box_width - 2*margin
        x = x_start + box_width*i + margin*i
        y_start = box_height*row_id + margin*row_id
        y = y_start + box_height + margin

        coordinates = ( x, y,x+box_width,y+box_height)

        # draw rectange
        # if checking previous guess
        colour = '#404245'
        if (checkcolour):
            if (guess[i] == goalWord[i]):
                colour = '#6e9960' # green
            elif guess[i] in goalWord:
                colour = '#d5b081' # yellow
            else:
                colour = '#18191A' # dark
        canvas.create_rectangle(coordinates, fill=colour, outline=colour )

        # if no letter exists dont create a text
        if ( i > len(guess)-1 ):
            continue
        else:
            canvas.create_text(x+box_width/2, y+box_height/2, text=guess[i], fill="white", tags=tags, font=("Arial",25))
            canvas.lower(id)

# Initialize and configure windows
window = tk.Tk()
window.title('Wordel')
window.geometry('600x500')
window.configure(bg='#25272a')
window.bind('<BackSpace>', onBackspacePress)
window.bind('<Key>', onKeyPress)
window.bind('<Return>', onReturnPress)

canvas = tk.Canvas(window, width = 600, height = 500, bg='#25272a', borderwidth='0', highlightthickness=0)
canvas.pack()

# create blank instance of first row
create_row(canvas, 600, 500, 0, "", "row0", False)
getWord("words.txt", 6)


window.mainloop()