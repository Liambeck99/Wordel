from curses import window
from curses.ascii import isdigit
import tkinter as tk
from tkinter.ttk import *
import random
import datetime

from numpy import append
#from Game import GameLoop

class MenuController:
    def __init__(self):
        self.initialiseWindow(600,500)

    # Create the window with size
    def initialiseWindow(self, width, height):
        self.bgcolour = '#25272a'
        # Initialize and configure windows
        self.menuWindow = tk.Tk()
        self.menuWindow.title('Wordel')
        dimensions = str(width) + 'x' + str(height)
        self.menuWindow.geometry(dimensions)
        self.menuWindow.configure(bg=self.bgcolour)

        # Initialize canvas
        self.canvas = tk.Canvas(self.menuWindow, width = width, height = height, bg=self.bgcolour, borderwidth='0', highlightthickness=0)
        self.canvas.pack()

        self.initialiseUI()

        self.menuWindow.mainloop()



    def initialiseUI(self):
        # Create style Object
        style = Style()
        
        style.configure('TButton', font = ('calibri', 20, 'bold'), borderwidth = '4')

        # Changes will be reflected
        # by the movement of mouse.
        style.map('TButton', foreground = [('active', '!disabled', 'green')],
                            background = [('active', 'black')])
        
        # button 1
        btn1 = Button(self.menuWindow, text = 'Quit !', command = self.menuWindow.destroy)
        btn1.grid(row = 0, column = 3, padx = 100)
        
        # button 2
        btn2 = Button(self.menuWindow, text = 'Click me !', command = None)
        btn2.grid(row = 1, column = 3, pady = 10, padx = 100)

