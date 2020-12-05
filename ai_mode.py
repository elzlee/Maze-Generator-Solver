import math, copy, random
from cmu_112_graphics import *
from tkinter import *

####################### mazeCell #######################
class MazeCell(object):
    def __init__(self, north, east, south, west):
        self.north = north
        self.east = east
        self.south = south
        self.west = west

####################### some global bois #######################       
NORTH = (-1,0)
EAST = (0,1)
SOUTH = (1,0)
WEST = (0,-1)

class AIMode(Mode):
    def appStarted(mode):
        # colors shortcut
        mode.mint = '#a2d5c6'
        mode.red = '#b85042'
        mode.white = '#FFFFFF'
        mode.gold = '#fbbc04'

        # button/label
        mode.buttonFont = ('Calibri', 15)
        mode.buttonH = 50 # height
        mode.buttonW = 200 # width
        mode.playerLabelFont = ('Calibri', 40)

        # general
        mode.cellSize = 25
        mode.mazeRows = 20
        mode.mazeCols = 20
        mode.mazeCellColor = mode.white
        mode.mazeWallColor = mode.red
        mode.winner = None
        mode.loser = None
        
        # binary tree maze gen
        mode.validDirectionsBT = ['south', 'east']

        # user maze
        mode.userMazeCX = mode.width * (1/4)
        mode.userMazeCY = mode.height/2
        mode.userGrid = [[MazeCell(False, False, False, False)] * mode.mazeCols for i in range(mode.mazeRows)] #board = 2d list
        mode.userLabelCX = mode.userMazeCX
        mode.userLabelCY = mode.userMazeCY + (mode.cellSize * mode.mazeRows /2) + 50

        # user, path
        mode.userPosition = (mode.mazeRows-1, mode.mazeCols-1) #update with row, drow, etc.
        mode.userPath = set() # to be filled...
        mode.userPath.add((mode.mazeRows-1, mode.mazeCols-1)) # add first position

        # ai maze
        mode.aiMazeCX = mode.width * (3/4)
        mode.aiMazeCY = mode.height/2
        mode.aiGrid = [[MazeCell(False, False, False, False)] * mode.mazeCols for i in range(mode.mazeRows)] #board = 2d list
        mode.createBothMazes()
        mode.aiLabelCX = mode.aiMazeCX
        mode.aiLabelCY = mode.aiMazeCY + (mode.cellSize * mode.mazeRows /2) + 50

        # pathfinding
        # mode.currNode = (mode.mazeRows-1, mode.mazeCols-1) # init
        # mode.visited = [[False] * mode.mazeCols for i in range(mode.mazeRows)] # 2d list of maze cells, True=visited

        # flags
        mode.aiSolvedMaze = False
        mode.userSolvedMaze = False
        mode.userStartedMaze = False
        mode.gameOver = False #true if there's a winner

    def getCellBounds(mode, row, col, mazeType): 
        # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
        if mazeType == 'userMaze':
            (mazeCX, mazeCY) = (mode.userMazeCX, mode.userMazeCY)
        elif mazeType == 'aiMaze':
            (mazeCX, mazeCY) = (mode.aiMazeCX, mode.aiMazeCY)
        mazeTopLeftCornerX = mazeCX - (mode.cellSize * mode.mazeCols / 2)
        mazeTopLeftCornerY = mazeCY - (mode.cellSize * mode.mazeRows / 2)
        x0 = mazeTopLeftCornerX +  col * mode.cellSize
        x1 = mazeTopLeftCornerX + (col+1) * mode.cellSize
        y0 = mazeTopLeftCornerY + row * mode.cellSize
        y1 = mazeTopLeftCornerY + (row+1) * mode.cellSize
        return (x0, y0, x1, y1)
   
   ####################### (both) maze generation #######################
    # binary tree for now, change to RANDOM later #

    def createBothMazes(mode): #DONE
    # same algorithm (switch it up after MVP), but add to both
    # mode.userGrid & mode.aiGrid
        # bias: SOUTH/EAST 
        for row in range(mode.mazeRows):
            for col in range(mode.mazeCols):
                randomIndex = random.randint(0, len(mode.validDirectionsBT) - 1) # 0 or 1
                direction = mode.validDirectionsBT[randomIndex] #south or east
                if direction == 'south':
                    mode.userGrid[row][col] = MazeCell(True, True, False, True)
                    mode.aiGrid[row][col] = MazeCell(True, True, False, True)
                elif direction == 'east':
                    mode.userGrid[row][col] = MazeCell(True, False, True, True)
                    mode.aiGrid[row][col] = MazeCell(True, False, True, True)
                mode.undoOverDrawnWall(row, col, 'userMaze')
                mode.undoOverDrawnWall(row, col, 'aiMaze')
                
        ### override for exception cases 

        # bottom row
        for col in range(mode.mazeCols):
            row = mode.mazeRows - 1
            mode.userGrid[row][col] = MazeCell(True, False, True, True)
            mode.aiGrid[row][col] = MazeCell(True, False, True, True)
            mode.undoOverDrawnWall(row, col, 'userMaze')
            mode.undoOverDrawnWall(row, col, 'aiMaze')
        # rightmost column
        for row in range(mode.mazeRows):
            col = mode.mazeCols - 1
            mode.userGrid[row][col] = MazeCell(True, True, False, True)
            mode.aiGrid[row][col] = MazeCell(True, False, True, True)
            mode.undoOverDrawnWall(row, col, 'userMaze')
            mode.undoOverDrawnWall(row, col, 'aiMaze')
        # last cell: direction info not needed for last cell
        mode.userGrid[mode.mazeRows - 1][mode.mazeCols - 1] = MazeCell(False, True, True, False)
        mode.aiGrid[mode.mazeRows - 1][mode.mazeCols - 1] = MazeCell(False, True, True, False)
        return mode.userGrid, mode.aiGrid # modified list

    def undoOverDrawnWall(mode, row, col, mazeType): #DONE
    # helper function, no data saved --> if statements!
    # Undo drawing over open walls 

        # for mazeType
        if mazeType == 'userMaze':
            gridPlaceholder = mode.userGrid
            currCell = mode.userGrid[row][col]
        elif mazeType == 'aiMaze':
            gridPlaceholder = mode.aiGrid
            currCell = mode.aiGrid[row][col]

        # meat of the function
        if col > 0:
            leftCell = gridPlaceholder[row][col-1] # col > 0 for leftCell to exist
            if leftCell.east == False: # east wall = open
                currCell.west = False      
        if row > 0:
            aboveCell = gridPlaceholder[row-1][col] # row > 0 for aboveCell to exist
            if aboveCell.south == False:
                currCell.north = False

    def drawUserMaze(mode, canvas): #DONE
        for row in range(mode.mazeRows):
            for col in range(mode.mazeCols):
                (x0, y0, x1, y1) = mode.getCellBounds(row, col, 'userMaze') 
                currCell = mode.userGrid[row][col]
                mode.drawGeneralMaze(canvas, row, col, currCell, x0, y0, x1, y1)  
                # gold End square turns mint when user solves maze
                if (row, col) == (0, 0):
                    if mode.userPosition == (0,0): 
                        color = mode.mint
                        canvas.create_rectangle(x0, y0, x1, y1, fill=color, width=0)

    def drawAIMaze(mode, canvas): #DONE
        for row in range(mode.mazeRows):
            for col in range(mode.mazeCols):
                (x0, y0, x1, y1) = mode.getCellBounds(row, col, 'aiMaze') 
                currCell = mode.aiGrid[row][col]
                mode.drawGeneralMaze(canvas, row, col, currCell, x0, y0, x1, y1) 

    def drawGeneralMaze(mode, canvas, row, col, currCell, x0, y0, x1, y1): #DONE        
        # maze cell color
        canvas.create_rectangle(x0, y0, x1, y1, fill=mode.mazeCellColor, width=0)
        # gold End square
        if (row, col) == (0, 0):
            color = mode.gold
            canvas.create_rectangle(x0, y0, x1, y1, fill=color, width=0)
        # mint Start square
        if (row, col) == (mode.mazeRows-1, mode.mazeCols-1):
            canvas.create_rectangle(x0, y0, x1, y1, fill=mode.mint, width=0)

        # draw red maze lines
        if currCell.north == True:
            canvas.create_line(x0, y0, x1, y0, fill=mode.mazeWallColor, width=1)
        if currCell.east == True:
            canvas.create_line(x1, y0, x1, y1, fill=mode.mazeWallColor, width=1)
        if currCell.south == True:
            canvas.create_line(x0, y1, x1, y1, fill=mode.mazeWallColor, width=1)
        if currCell.west == True:
            canvas.create_line(x0, y0, x0, y1, fill=mode.mazeWallColor, width=1)

        # mint walls for start & end
        if (row, col) == (0, 0):
            canvas.create_line(x0, y0, x1, y0, fill=mode.mint, width=3)
        if (row, col) == (mode.mazeRows-1, mode.mazeCols-1):
            canvas.create_line(x0, y1, x1, y1, fill=mode.mint, width=3)
                      
    ####################### (user) interaction #######################

    def mousePressed(mode, event): #DONE
        # BUTTON: 'menu'
        b3cx = mode.width/2
        b3cy = mode.height - 50 
        if (((b3cx - mode.buttonW/2) <= event.x <= (b3cx + mode.buttonW/2)) and 
            ((b3cy - mode.buttonH/2) <= event.y <= (b3cy + mode.buttonH/2))):
            mode.app.setActiveMode(mode.app.splashScreenMode)

    def keyPressed(mode, event): #DONE
    # only for userGrid
        (row, col) = mode.userPosition
        if mode.userStartedMaze == False: 
            mode.userStartedMaze = True
        if event.key == 'Up' and mode.validMove(row, col, NORTH, 'userMaze') == True:
            mode.doUserMove(row, col, NORTH)
        elif event.key == 'Right' and mode.validMove(row, col, EAST, 'userMaze') == True:
            mode.doUserMove(row, col, EAST)
        elif event.key == 'Down' and mode.validMove(row, col, SOUTH, 'userMaze') == True:
            mode.doUserMove(row, col,  SOUTH)
        elif event.key == 'Left' and mode.validMove(row, col, WEST, 'userMaze') == True:
            mode.doUserMove(row, col, WEST) 

    def validMove(mode, row, col, direction, mazeType): #DONE
    # given current position (row,col), is moving in 'direction' Valid?
    # 1. within bounds of grid
    # 2. there is no wall between currCell and newCell
        if mazeType == 'userMaze':
            gridPlaceholder = mode.userGrid
        elif mazeType == 'aiMaze':
            gridPlaceholder = mode.aiGrid

        (drow, dcol) = direction
        (newrow, newcol) = (row+drow, col+dcol)
        if (not 0 <= newrow < mode.mazeRows) or (not 0 <= newcol < mode.mazeCols):
            return False
        if direction == NORTH:
            if gridPlaceholder[row][col].north == False: return True
        elif direction == EAST:
            if gridPlaceholder[row][col].east == False: return True
        elif direction == SOUTH:
            if gridPlaceholder[row][col].south == False: return True
        elif direction == WEST:
            if gridPlaceholder[row][col].west == False: return True
        return False        

    def doUserMove(mode, row, col, direction): #DONE
        # 1. update mode.userPosition
        # 2. add or subtract new position from the mode.userPath set
        (drow, dcol) = direction
        (newRow, newCol) = (row + drow, col + dcol)
        mode.userPosition = (newRow, newCol)
        if mode.userPosition not in mode.userPath:
            mode.userPath.add(mode.userPosition)
        else:
            mode.userPath.remove((row,col))
        if mode.userPosition == (0,0): 
            mode.userSolvedMaze = True

    def drawUserPath(mode, canvas): #DONE
        for (row, col) in mode.userPath:
            (x0, y0, x1, y1) = mode.getCellBounds(row, col, 'userMaze')
            canvas.create_rectangle(x0, y0, x1, y1, fill=mode.mint, width = 0)
 
    ####################### (ai) maze solving #######################
    def drawSolution(mode, canvas): 
        #should be similar, change variables
        pass
    def createSolution(mode): #dijkstra --> update to visualization after MVP
        pass
    def doStep(mode):
        # 
        pass
    def timerFired(mode):
        #mode.doStep()
        pass

    def gameOver(mode):
        #if (mode.userPosition == (0,0)) or aiSolvedMaze :
            # mode.gameOver = True
        pass
    ####################### extra features #######################
    def drawGameButtons(mode, canvas):
        # return to menu button = bottom center
        b3cx = mode.width/2
        b3cy = mode.height - 50 
        canvas.create_rectangle(b3cx - mode.buttonW/2, b3cy - mode.buttonH/2, 
                                b3cx + mode.buttonW/2, b3cy + mode.buttonH/2, 
                                fill=mode.red, width=0)
        canvas.create_text(b3cx, b3cy, text='MENU', 
                            font=mode.buttonFont, fill=mode.white)

    def drawPlayerLabels(mode, canvas):
        canvas.create_text(mode.userLabelCX, mode.userLabelCY, text='YOU', 
                            font=mode.playerLabelFont, fill=mode.white)
        canvas.create_text(mode.aiLabelCX, mode.aiLabelCY, text='AI', 
                            font=mode.playerLabelFont, fill=mode.white)
                   
    def drawWinnerLoserLabels(mode, canvas):
        if mode.winner == 'user':
            canvas.create_text(mode.userLabelCX, mode.userLabelCY, text='YOU win :)', 
                            font=mode.playerLabelFont, fill=mode.white)
            canvas.create_text(mode.aiLabelCX, mode.aiLabelCY, text='AI', 
                            font=mode.playerLabelFont, fill=mode.white)
        elif mode.winner == 'ai':
            canvas.create_text(mode.userLabelCX, mode.userLabelCY, text='YOU lose :(', 
                            font=mode.playerLabelFont, fill=mode.white)
            canvas.create_text(mode.aiLabelCX, mode.aiLabelCY, text='AI', 
                            font=mode.playerLabelFont, fill=mode.white)

    def drawTimer(mode, canvas): #important for game ai mode!
        pass

    #####################################################################

    def redrawAll(mode, canvas):
        #screen background
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill=mode.mint)
        mode.drawUserMaze(canvas)
        mode.drawAIMaze(canvas)
        mode.drawGameButtons(canvas)
        mode.drawUserPath(canvas)
        if mode.gameOver == False:
            mode.drawPlayerLabels(canvas)
        else: # mode.gameOver = True
            mode.drawWinnerLoserLabels(canvas)
        # ai win
        if (mode.aiSolvedMaze == True) and (mode.userSolvedMaze == False):
            # color in the winner maze
            # draw text 'ai win'
            pass
        # user win
        elif (mode.userSolvedMaze == True) and (mode.aiSolvedMaze == False):
            # color in the winner maze
            # draw text 'user win'
            pass
