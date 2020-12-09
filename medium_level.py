###############################################################
# Medium maze level
# maze generation: Depth First Search (Recursive Backtracking)
###############################################################

import math, copy, random
from cmu_112_graphics import *
from tkinter import *

class MazeCell(object):
    def __init__(self, north, east, south, west):
        self.north = north
        self.east = east
        self.south = south
        self.west = west

def appStarted(app):
    #colors shortcut
    app.mint = '#a2d5c6'
    app.red = '#b85042'
    app.white = '#FFFFFF'
    app.gold = '#fbbc04'

    # maze
    mode.cellSize = 25
    mode.mazeRows = 20 # increase for difficulty
    mode.mazeCols = 20 # increase for difficulty
    mode.mazeCX = mode.width/2
    mode.mazeCY = mode.height/2
    mode.mazeTopLeftCornerX = mode.mazeCX - (mode.cellSize * mode.mazeCols / 2)
    mode.mazeTopLeftCornerY = mode.mazeCY - (mode.cellSize * mode.mazeRows / 2)
    mode.validDirections = [PLACEHOLDER]
    mode.buttonFont = ('Calibri', 15)
    mode.buttonH = 50 # height
    mode.buttonW = 200 # width
    
    #False = not visited yet; True = already visited
    app.grid = [[MazeCell(False, False, False, False)] * app.mazeCols for i in range(app.mazeRows)] #board = 2d list
    createMaze(app)

    #user
    userStarted(app)

    
def userStarted(app):
    app.userPosition = (0, 0) #update with row, drow, etc.
    pass

def getCellBounds(app, row, col): 
        # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
        x0 = app.mazeTopLeftCornerX +  col * app.cellSize
        x1 = app.mazeTopLeftCornerX + (col+1) * app.cellSize
        y0 = app.mazeTopLeftCornerY + row * app.cellSize
        y1 = app.mazeTopLeftCornerY + (row+1) * app.cellSize
        return (x0, y0, x1, y1)

def cellIsValid(app, row, col):
    if not (0 <= row <= app.rows-1) and (0 <= col <= app.cols-1): # within bounds
        return False
    if app.grid[row][col].visited == False: #cell not visited:
        return True
    return False

def createMaze(app):
    # choose starting cell in app.grid
    # randomly order app.validDirections
    # iterate through directions in app.validDirections
        # get (row, col) of the new cell w/ the direction
        # if cellIsValid(app, row, col) == True:
            # carve passage
            # move onto next cell (recursion)
        # elif cellIsValid(app, row, col) == False:
            # 
    # random.shuffle(app.validDirections) 
    for direction in app.validDirections:
        pass

def drawUserPath(app, canvas):
    '''
    (startCellX, startCellY) = (0, 0)
    currCell = app.grid[startCellX][startCellY] # starting cell
    randomIndex = random.randint(0, len(app.validDirections) - 1)
    direction = app.validDirections[randomIndex] # N, E, S, W
    if direction == 'north':
        cellDX, cellDY = 0, -1
    elif direction == 'east':
        cellDX, cellDY = 1, 0
    elif direction == 'south':
        cellDX, cellDY = 0, 1
    elif direction == 'west':
        cellDX, cellDY = -1, 0
    (newCellX, newCellY) = (startCellX + cellDX, startCellY + cellDY)

    if cellIsValid(app, newCellX, newCellY) == True:
        currCell
         # wall between currCell and nextCell = False
    # recursion on next cell
    '''
    return app.grid # modified list

def drawMaze(app, canvas):
    pass

def drawGameButtons(app, canvas):
    # hint button = left
    b1cx = (app.mazeCX - (app.mazeCols * app.cellSize) / 2) / 2
    b1cy = app.mazeCY
    canvas.create_rectangle(b1cx - app.buttonW/2, b1cy - app.buttonH/2, 
                            b1cx + app.buttonW/2, b1cy + app.buttonH/2, 
                            fill=app.white, width=0)
    canvas.create_text(b1cx, b1cy, text='hint', 
                        font=app.buttonFont, fill=app.red)
    # solution button = right
    b2cx = app.width - b1cx
    b2cy = app.mazeCY
    canvas.create_rectangle(b2cx - app.buttonW/2, b2cy - app.buttonH/2, 
                            b2cx + app.buttonW/2, b2cy + app.buttonH/2, 
                            fill=app.red, width=0)
    canvas.create_text(b2cx, b2cy, text='solution', 
                        font=app.buttonFont, fill=app.white)
    # return to menu button = bottom center
    b3cx = app.mazeCX
    b3cy = app.height - 50 
    canvas.create_rectangle(b3cx - app.buttonW/2, b3cy - app.buttonH/2, 
                            b3cx + app.buttonW/2, b3cy + app.buttonH/2, 
                            fill=app.red, width=0)
    canvas.create_text(b3cx, b3cy, text='<< MENU <<', 
                        font=app.buttonFont, fill=app.white)

def drawTimer(app, canvas):
    pass

def timerFired(app):
    pass

def mousePressed(app, event):
    pass

def redrawAll(app, canvas):
    #screen background
    canvas.create_rectangle(0, 0, app.width, app.height, fill=app.mint)
    drawMaze(app, canvas)
    drawGameButtons(app, canvas)

runApp(width=1200, height=800)