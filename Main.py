from curses import window
from curses.ascii import isdigit
import tkinter as tk

goalWord = "ENGINE"
currentGuess = ""


def clearRow(i):

    string = 'current&&row' + str(i)
    canvas.delete('current&&row')

# Function call when backspace is pressed
def onBackspace(event):
    global currentGuess
    # slice off last element, clear row & redraw
    currentGuess = currentGuess[:-1]
    clearRow(1)
    create_row(canvas, 600, 500, 1, currentGuess.upper(), "row1")

def onKeyPress(event):
    character = event.char
    if( character.isalpha() ):
        update_row(character)

def onReturnPress(event):
    a = 1


def update_row(character):
    global currentGuess
    
    # add new character, clear row and redraw
    currentGuess += character
    clearRow(1)
    create_row(canvas, 600, 500, 1, currentGuess.upper(), "row1")

# Display row
def create_row(canvas, canvas_width, canvas_height, row_id, guess, tag):

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
        canvas.create_rectangle(coordinates, fill='#404245', outline='#404245' )

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
window.bind('<BackSpace>', onBackspace)
window.bind('<Key>', onKeyPress)

canvas = tk.Canvas(window, width = 600, height = 500, bg='#25272a', borderwidth='0', highlightthickness=0)
canvas.pack()

# create blank instance of first row
create_row(canvas, 600, 500, 1, "", "row1")



window.mainloop()