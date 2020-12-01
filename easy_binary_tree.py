##########################################
# Easy maze level
# maze generation: binary tree 
##########################################
'''
- create maze without canvas, stored as list/tuple
- choose start, end points
- check with backtracking if soln exists
- collision detection = if wall exists
'''

import math, copy, random
from cmu_112_graphics import *
from tkinter import *

class MazeCell(object):
    def __init__(self, north, east, south, west):
        self.north = north
        self.east = east
        self.south = south
        self.west = west
        
class EasyMode(Mode):
    def appStarted(mode):
        mode.cellSize = 25
        mode.mazeRows = 20 # increase for difficulty
        mode.mazeCols = 20 # increase for difficulty
        mode.mazeCX = mode.width/2
        mode.mazeCY = mode.height/2
        mode.mazeTopLeftCornerX = mode.mazeCX - (mode.cellSize * mode.mazeCols / 2)
        mode.mazeTopLeftCornerY = mode.mazeCY - (mode.cellSize * mode.mazeRows / 2)
        mode.validDirections = ['south', 'east']
        mode.buttonFont = ('Calibri', 15)
        mode.buttonH = 50 # height
        mode.buttonW = 200 # width
        
        #False = open wall; True = closed wall
        mode.grid = [[MazeCell(False, False, False, False)] * mode.mazeCols for i in range(mode.mazeRows)] #board = 2d list
        mode.createMaze()

        #colors shortcut
        mode.mint = '#a2d5c6'
        mode.red = '#b85042'
        mode.white = '#FFFFFF'
        mode.gold = '#fbbc04'

    def getCellBounds(mode, row, col): 
            # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
            x0 = mode.mazeTopLeftCornerX +  col * mode.cellSize
            x1 = mode.mazeTopLeftCornerX + (col+1) * mode.cellSize
            y0 = mode.mazeTopLeftCornerY + row * mode.cellSize
            y1 = mode.mazeTopLeftCornerY + (row+1) * mode.cellSize
            return (x0, y0, x1, y1)

    def createMaze(mode):
        # bias: SOUTH/EAST 
        for row in range(mode.mazeRows):
            for col in range(mode.mazeCols):
                randomIndex = random.randint(0, len(mode.validDirections) - 1) # 0 or 1
                direction = mode.validDirections[randomIndex] #south or east
                if direction == 'south':
                    mode.grid[row][col] = MazeCell(True, True, False, True)
                elif direction == 'east':
                    mode.grid[row][col] = MazeCell(True, False, True, True)
                mode.undoOverDrawnWall(row, col)
                
        ### override for exception cases 

        # bottom row
        for col in range(mode.mazeCols):
            row = mode.mazeRows - 1
            mode.grid[row][col] = MazeCell(True, False, True, True)
            mode.undoOverDrawnWall(row, col)
        # rightmost column
        for row in range(mode.mazeRows):
            col = mode.mazeCols - 1
            mode.grid[row][col] = MazeCell(True, True, False, True)
            mode.undoOverDrawnWall(row, col)
        # last cell: direction info not needed for last cell
        mode.grid[mode.mazeRows - 1][mode.mazeCols - 1] = MazeCell(False, True, True, False) 
        return mode.grid # modified list

    def undoOverDrawnWall(mode, row, col):
    # Undo drawing over open walls 
        currCell = mode.grid[row][col]
        if col > 0:
            leftCell = mode.grid[row][col-1] # col > 0 for leftCell to exist
            if leftCell.east == False: # east wall = open
                currCell.west = False      
        if row > 0:
            aboveCell = mode.grid[row-1][col] # row > 0 for aboveCell to exist
            if aboveCell.south == False:
                currCell.north = False

    def drawMaze(mode, canvas):
        # bulk of maze
        for row in range(mode.mazeRows):
            for col in range(mode.mazeCols):
                (x0, y0, x1, y1) = mode.getCellBounds(row, col) 
                currCell = mode.grid[row][col]
                if currCell.north == True:
                    canvas.create_line(x0, y0, x1, y0, fill=mode.red, width=3)
                if currCell.east == True:
                    canvas.create_line(x1, y0, x1, y1, fill=mode.red, width=3)
                if currCell.south == True:
                    canvas.create_line(x0, y1, x1, y1, fill=mode.red, width=3)
                if currCell.west == True:
                    canvas.create_line(x0, y0, x0, y1, fill=mode.red, width=3)
            

    def drawGameButtons(mode, canvas):
        # hint button = left
        b1cx = (mode.mazeCX - (mode.mazeCols * mode.cellSize) / 2) / 2
        b1cy = mode.mazeCY
        canvas.create_rectangle(b1cx - mode.buttonW/2, b1cy - mode.buttonH/2, 
                                b1cx + mode.buttonW/2, b1cy + mode.buttonH/2, 
                                fill=mode.white, width=0)
        canvas.create_text(b1cx, b1cy, text='hint', 
                            font=mode.buttonFont, fill=mode.red)
        # solution button = right
        b2cx = mode.width - b1cx
        b2cy = mode.mazeCY
        canvas.create_rectangle(b2cx - mode.buttonW/2, b2cy - mode.buttonH/2, 
                                b2cx + mode.buttonW/2, b2cy + mode.buttonH/2, 
                                fill=mode.red, width=0)
        canvas.create_text(b2cx, b2cy, text='solution', 
                            font=mode.buttonFont, fill=mode.white)
        # return to menu button = bottom center
        b3cx = mode.width/2
        b3cy = mode.height - 50 
        canvas.create_rectangle(b3cx - mode.buttonW/2, b3cy - mode.buttonH/2, 
                                b3cx + mode.buttonW/2, b3cy + mode.buttonH/2, 
                                fill=mode.red, width=0)
        canvas.create_text(b3cx, b3cy, text='MENU', 
                            font=mode.buttonFont, fill=mode.white)

    def drawTimer(mode, canvas):
        pass

    def timerFired(mode):
        pass

    def mousePressed(mode, event):
        # BUTTON: 'menu'
        b3cx = mode.width/2
        b3cy = mode.height - 50 
        if (((b3cx - mode.buttonW/2) <= event.x <= (b3cx + mode.buttonW/2)) and 
            ((b3cy - mode.buttonH/2) <= event.y <= (b3cy + mode.buttonH/2))):
            mode.app.setActiveMode(mode.app.splashScreenMode)

    def redrawAll(mode, canvas):
        #screen background
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill=mode.mint)
        mode.drawMaze(canvas)
        mode.drawGameButtons(canvas)


