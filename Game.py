from curses import window
from curses.ascii import isdigit
import tkinter as tk
import random
import datetime

from numpy import append

# Class to control the Game Logic
class GameLoop:

    def __init__(self, targetLength, filename):
        self.targetLength = targetLength
        self.goalWord, self.words = self.getWord(filename, targetLength)

        ## PROTOTYPE PURPOSES ONLY ##
        print(self.goalWord)

        self.currentGuess = ""
        self.previousGuesses = []
        self.bgcolour = '#25272a'
        self.lightcolour = '#404245'
        self.darkcolour = '#18191A'
        self.greencolour = '#6e9960'
        self.yellowcolour = '#d5b081'
        self.initialiseWindow(600,500)
        self.gameWindow.mainloop()

    # Create the window with size
    def initialiseWindow(self, width, height):
        # Initialize and configure windows
        self.gameWindow = tk.Tk()
        self.gameWindow.title('Wordel')
        dimensions = str(width) + 'x' + str(height)
        self.gameWindow.geometry(dimensions)
        self.gameWindow.configure(bg=self.bgcolour)
        self.gameWindow.bind('<BackSpace>', self.onBackspacePress)
        self.gameWindow.bind('<Key>', self.onKeyPress)
        self.gameWindow.bind('<Return>', self.onReturnPress)

        # Initialize canvas
        self.gameCanvas = tk.Canvas(self.gameWindow, width = width, height = height, bg=self.bgcolour, borderwidth='0', highlightthickness=0)
        self.gameCanvas.pack()

        # create blank instance of first row
        self.create_row(600, 500, 0, "", "row0", False)

    # Returns goal word and list of all words in file of length X
    def getWord(self, filename, length):
        # Read file
        fileObj = open(filename, "r")   # open file in read mode
        allWords = fileObj.read().splitlines()  # put all files into array
        fileObj.close()

        words = []
        # get all words of length x
        for i in range(len(allWords)):
            if (len(allWords[i]) == length):
                words.append(allWords[i].upper())

        # set seed and pick random word from list
        current_date = datetime.datetime.now()
        random.seed(current_date.hour * current_date.minute * current_date.second)
        goalWord = words[random.randint(0,len(words))].upper()

        # return goal word and full list
        return(goalWord, words)

    # Display row
    def create_row(self, canvas_width, canvas_height, row_id,  guess, tag, checkcolour):
        for i in range(self.targetLength):

            # initialise tags
            tags = (tag,)

            # Calculate location to draw onscreen
            box_width = 50
            box_height = 50
            margin = 4

            # start of row dependent on word length
            x_start = (canvas_width/2) - self.targetLength/2*box_width - (self.targetLength/2 -1)*margin 
            x = x_start + box_width*i + margin*i
            y_start = box_height*row_id + margin*row_id
            y = y_start + box_height + margin

            coordinates = ( x, y,x+box_width,y+box_height)

            # draw rectange
            # if checking previous guess
            colour = self.lightcolour
            if (checkcolour):
                if (guess[i] == self.goalWord[i]):
                    colour = self.greencolour # green
                elif guess[i] in self.goalWord:
                    colour = self.yellowcolour # yellow
                else:
                    colour = self.darkcolour # dark
            self.gameCanvas.create_rectangle(coordinates, fill=colour, outline=colour )

            # if no letter exists dont create a text
            if ( i > len(guess)-1 ):
                continue
            else:
                self.gameCanvas.create_text(x+box_width/2, y+box_height/2, text=guess[i], fill="white", tags=tags, font=("Arial",25))
                self.gameCanvas.lower(id)

    # Update the current row with the caracter
    def update_row(self, character):        
        # add new character, clear row and redraw
        self.currentGuess += character.upper()
        self.clearRow(1)
        self.create_row(600, 500, 0, self.currentGuess, "row1", False)

    # Deletes the row at index i
    def clearRow(self, i):
        string = 'current&&row' + str(i)
        self.gameCanvas.delete(string)
    
    # Returns true if current guess exists in word list
    def currentGuessExists(self):
        if self.currentGuess in self.words:
            return True
        return False

    # Function call when backspace is pressed
    def onBackspacePress(self, event):
        # slice off last element, clear row & redraw
        self.currentGuess = self.currentGuess[:-1]
        self.clearRow(1)
        self.create_row(600, 500, 0, self.currentGuess.upper(), "row0", False)

    # Handle key press
    def onKeyPress(self, event):
        global targetLength

        if( len(self.currentGuess) == self.targetLength):
            return

        character = event.char

        if( character.isalpha() ):
            self.update_row(character)

    # Handle on return/enter pressed
    def onReturnPress(self,event):

        # If word not correct length return
        if ( len(self.currentGuess) != self.targetLength ):
            return
        
        # If current guess not a word
        if ( not self.currentGuessExists() ):
            return

        # add current guess to start of guess list
        self.previousGuesses.insert(0,self.currentGuess)
        self.currentGuess = '' # clear for new guess

        # redraw empty first row
        self.clearRow(0)
        self.create_row(600, 500, 0, self.currentGuess, "row0", False)

        # draw row for all previous guesses
        for i in range( len(self.previousGuesses)):
            row = 'row' + str(i+1)
            self.create_row(600, 500, i+1, self.previousGuesses[i], row, True)
