from curses import window
from curses.ascii import isdigit
from tarfile import LENGTH_NAME
import tkinter as tk
from tkinter.ttk import *
import random
import datetime
import time

from numpy import append

# Class to control the Game Logic
class GameLoop:

    def __init__(self, targetLength, filename):
        self.targetLength = targetLength
        self.goalWord, self.words = self.getWord(filename, targetLength)
        self.currentGuess = ""
        self.previousGuesses = []

        ## PROTOTYPE PURPOSES ONLY ##
        print(self.goalWord)

        # initialise variables for boxes for letters
        self.box_width = 50
        self.box_height = 50
        self.margin = 4

        self.popupFlag = False  # needed to stop redraw over top of popup messages

        # initialise window
        self.bgcolour = '#25272a'
        self.lightcolour = '#404245'
        self.darkcolour = '#18191A'
        self.greencolour = '#6e9960'
        self.yellowcolour = '#d5b081'
        self.redcolour = '#cf6a4f'
        self.font = "Helvetica"
        self.initialiseWindow(600,500)
        self.gameWindow.mainloop()

    # Create the window with size
    def initialiseWindow(self, width, height):
        # Initialize and configure windows
        self.gameWindow = tk.Tk()
        self.gameWindow.title('Wordel')
        dimensions = str(width) + 'x' + str(height)
        self.gameWindow.geometry(dimensions)
        self.gameWindow.minsize(width,height)
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

            # start of row dependent on word length
            self.x_start = (canvas_width/2) - self.targetLength/2*self.box_width - (self.targetLength/2 -1)*self.margin 
            x = self.x_start + self.box_width*i + self.margin*i
            self.y_start = self.box_height*row_id + self.margin*row_id
            y = self.y_start + self.box_height + self.margin

            coordinates = ( x, y,x+self.box_width,y+self.box_height)

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
                self.gameCanvas.create_text(x+self.box_width/2, y+self.box_height/2, text=guess[i], fill="white", tags=tags, font=(self.font,25))
                self.gameCanvas.lower(id)

    # Update the current row with the caracter
    def update_row(self, character):        
        # add new character, clear row and redraw
        self.currentGuess += character.upper()
        self.clearRow(1)
        self.create_row(600, 500, 0, self.currentGuess, "row1", False)

    # Deletes the row at index i
    def clearRow(self, i):
        if ( isinstance(i,int)):
            string = 'current&&row' + str(i)
            self.gameCanvas.delete(string)
        else:
            self.gameCanvas.delete(i)
    
    # Returns true if current guess exists in word list
    def currentGuessExists(self):
        if self.currentGuess in self.words:
            return True
        return False

    # Function call when backspace is pressed
    def onBackspacePress(self, event):
        if(self.popupFlag): return

        # slice off last element, clear row & redraw
        self.currentGuess = self.currentGuess[:-1]
        self.clearRow(1)
        self.create_row(600, 500, 0, self.currentGuess.upper(), "row0", False)

    # Handle key press
    def onKeyPress(self, event):
        if(self.popupFlag): return

        if( len(self.currentGuess) == self.targetLength):
            return

        character = event.char

        if( character.isalpha() ):
            self.update_row(character)

    # Handle on return/enter pressed
    def onReturnPress(self,event):
        if(self.popupFlag): return

        # If word not correct length return
        if ( len(self.currentGuess) != self.targetLength ):
            self.popUp("Incorrect Length", "length")
            return
        
        # If current guess not a word
        if ( not self.currentGuessExists() ):
            self.popUp("Doesnt Exist", "exists")
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

    # Create a pop up message over first row
    def popUp(self, message, tag):
        # initialise variables
        tags = (tag,)
        length = len(self.goalWord)

        # caluclate where to draw popup
        x_end = self.x_start + length*self.box_width + (length-1)*self.margin
        y = self.y_start + self.box_height
        coordinates = ( self.x_start, y, x_end, y + self.box_height + self.margin)

        # draw popup and set flag so remains on front
        self.popupFlag = True
        self.gameCanvas.create_rectangle(coordinates, fill=self.redcolour, outline=self.redcolour, tags=tags)
        self.gameCanvas.create_text(self.gameCanvas.winfo_width()/2, y+self.box_height/2, text=message, fill="white", tags=tags, font=(self.font,5*len(self.goalWord) if len(self.goalWord) < 5 else 25))


        # wait before deleting
        self.gameWindow.after(1000, self.deletePopup, tags)

    def deletePopup(self, tags):

        self.clearRow(tags)
        self.popupFlag = False

            
