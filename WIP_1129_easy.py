##########################################
# WORKING VERSION: 2 lines per cell #
##########################################
'''
PROBLEM : MVC violation happens AFTER successfully drawing the maze. Why? 
it's the "createMaze(app)" in "drawMaze(app, canvas)". 
How to avoid problem?
- create maze without canvas, stored as list/tuple
- choose start, end points
- check with backtracking if soln exists
- collision detection = if wall exists
'''

import math, copy, random
from cmu_112_graphics import *
from tkinter import *

def appStarted(app):
    app.cellSize = 25
    app.mazeRows = 20 # increase for difficulty
    app.mazeCols = 20 # increase for difficulty
    app.mazeCX = app.width/2
    app.mazeCY = app.height/2
    app.mazeTopLeftCornerX = app.mazeCX - (app.cellSize * app.mazeCols / 2)
    app.mazeTopLeftCornerY = app.mazeCY - (app.cellSize * app.mazeRows / 2)
    app.validDirections = ['south', 'east']
    app.buttonFont = ('Calibri', 15)
    app.buttonH = 50 # height
    app.buttonW = 200 # width

    #False = not visited yet; True = already visited
    app.grid = [[None] * app.mazeCols for i in range(app.mazeRows)] #board = 2d list
    createMaze(app)
    
    #colors shortcut
    app.mint = '#a2d5c6'
    app.red = '#b85042'
    app.white = '#FFFFFF'
    app.gold = '#fbbc04'
    
def getCellBounds(app, row, col): 
        # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
        x0 = app.mazeTopLeftCornerX +  col * app.cellSize
        x1 = app.mazeTopLeftCornerX + (col+1) * app.cellSize
        y0 = app.mazeTopLeftCornerY + row * app.cellSize
        y1 = app.mazeTopLeftCornerY + (row+1) * app.cellSize
        return (x0, y0, x1, y1)

def createMaze(app):
    # this maze has SOUTH/EAST bias
    for row in range(app.mazeRows):
       for col in range(app.mazeCols):
            randomIndex = random.randint(0, len(app.validDirections) - 1)
            direction = app.validDirections[randomIndex] #south or east
            if direction == 'south':
                app.grid[row][col] = 'southOpen'
            elif direction == 'east':
                app.grid[row][col]= 'eastOpen'

    ### override for exception cases
    
    # last cell
    app.grid[app.mazeRows - 1][app.mazeCols - 1] = 'both'
    # bottom row
    for col in range(app.mazeCols):
        app.grid[app.mazeRows - 1][col] = 'eastOpen'
    # rightmost column
    for row in range(app.mazeRows):
        app.grid[row][app.mazeCols - 1] = 'southOpen'
    
    return app.grid # modified list

def drawMaze(app, canvas):
    # top horizontal maze boundary
    canvas.create_line(app.mazeTopLeftCornerX, app.mazeTopLeftCornerY,
                        app.mazeTopLeftCornerX + app.mazeCols * app.cellSize,
                        app.mazeTopLeftCornerY, fill=app.red, width=3)
    # far left vertical maze boundary                   
    canvas.create_line(app.mazeTopLeftCornerX, app.mazeTopLeftCornerY,
                        app.mazeTopLeftCornerX,
                        app.mazeTopLeftCornerY + app.mazeRows * app.cellSize,
                        fill=app.red, width=3)
    # bulk of maze
    for row in range(app.mazeRows):
        for col in range(app.mazeCols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col) 
            if app.grid[row][col] == 'southOpen': # draw only East wall
                canvas.create_line(x1, y0, x1, y1, fill=app.red, width=3)
            elif app.grid[row][col] == 'eastOpen': # draw only South wall
                canvas.create_line(x0, y1, x1, y1, fill=app.red, width=3)
            elif app.grid[row][col] == 'both': # draw both walls (1 case)
                canvas.create_line(x1, y0, x1, y1, fill=app.red, width=3)
                canvas.create_line(x0, y1, x1, y1, fill=app.red, width=3)

def determineCellColor(app):
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

def keyPressed(app, event):
    pass

def redrawAll(app, canvas):
    #screen background
    canvas.create_rectangle(0, 0, app.width, app.height, fill=app.mint)
    drawMaze(app, canvas)
    drawGameButtons(app, canvas)

runApp(width=1200, height=800)

