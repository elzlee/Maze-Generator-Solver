##########################################
# Easy maze level
# Perfect maze generation: binary tree
# Maze Searching: Breadth First Search 
# Pathfinding: made it up? not sure if it's a thing
##########################################
# Citations referenced in this file #
    # hackerearth: 'Pseudocode' section, 'Visualizer' section
    # https://www.hackerearth.com/practice/algorithms/graphs/breadth-first-search/tutorial/

    # geeksforgeeks: 
    # https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/?ref=leftbar-rightbar
'''
QUESTION: popping things for set
BUG: going back to menu saves progress

- create maze without canvas, stored as list/tuple
- choose start, end points
- check with backtracking if soln exists
- collision detection = if wall exists
'''

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

class EasyMode(Mode):
    ####################### init #######################
    def appStarted(mode):
        #colors shortcut
        mode.mint = '#a2d5c6'
        mode.red = '#b85042'
        mode.white = '#FFFFFF'
        mode.gold = '#fbbc04'

        # maze
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
        mode.mazeCellColor = mode.white
        mode.mazeWallColor = mode.red

        # user, path
        mode.userPosition = (mode.mazeRows-1, mode.mazeCols-1) #update with row, drow, etc.
        mode.userPath = set() # to be filled...
        mode.userPath.add((mode.mazeRows-1, mode.mazeCols-1)) # add first position
        mode.userStartedMaze = False
        mode.userSolvedMaze = False
        mode.startingCell = (mode.mazeRows-1, mode.mazeCols-1) # mint) change for diff maze gen algos

        # pathfinding: solution, hint
        mode.showSolution = False
        mode.showHint = False
        mode.currNode = (mode.mazeRows-1, mode.mazeCols-1) # init
        mode.visited = [[False] * mode.mazeCols for i in range(mode.mazeRows)] # 2d list of maze cells, True=visited

        # mode.solution = [[False] * mode.mazeCols for i in range(mode.mazeRows)] # 2d list of maze cells
        mode.nodeSearchDirections = [NORTH, EAST, SOUTH, WEST] 
        mode.solution  = []
        mode.createSolution()
        

    def getCellBounds(mode, row, col): 
            # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
            x0 = mode.mazeTopLeftCornerX +  col * mode.cellSize
            x1 = mode.mazeTopLeftCornerX + (col+1) * mode.cellSize
            y0 = mode.mazeTopLeftCornerY + row * mode.cellSize
            y1 = mode.mazeTopLeftCornerY + (row+1) * mode.cellSize
            return (x0, y0, x1, y1)

    ####################### user interaction #######################
    def mousePressed(mode, event):
        # click on cell
        
        # BUTTON: 'hint'
        b1cx = (mode.mazeCX - (mode.mazeCols * mode.cellSize) / 2) / 2
        b1cy = mode.mazeCY
        if (((b1cx - mode.buttonW/2) <= event.x <= (b1cx + mode.buttonW/2)) and
            ((b1cy - mode.buttonH/2) <= event.y <= (b1cy + mode.buttonH/2))):
            mode.showHint = True

        # BUTTON: 'solution'
        b2cx = mode.width - b1cx
        b2cy = mode.mazeCY
        if (((b2cx - mode.buttonW/2) <= event.x <= (b2cx + mode.buttonW/2)) and
            ((b2cy - mode.buttonH/2) <= event.y <= (b2cy + mode.buttonH/2))):
            mode.showSolution = True

        # BUTTON: 'menu'
        b3cx = mode.width/2
        b3cy = mode.height - 50 
        if (((b3cx - mode.buttonW/2) <= event.x <= (b3cx + mode.buttonW/2)) and 
            ((b3cy - mode.buttonH/2) <= event.y <= (b3cy + mode.buttonH/2))):
            mode.app.setActiveMode(mode.app.splashScreenMode)

    def keyPressed(mode, event):
        (row, col) = mode.userPosition
        if mode.userStartedMaze == False: 
            mode.userStartedMaze = True
        if event.key == 'Up' and mode.validMove(row, col, NORTH) == True:
            mode.doMove(row, col, NORTH)
        elif event.key == 'Right' and mode.validMove(row, col, EAST) == True:
            mode.doMove(row, col, EAST)
        elif event.key == 'Down' and mode.validMove(row, col, SOUTH) == True:
            mode.doMove(row, col,  SOUTH)
        elif event.key == 'Left' and mode.validMove(row, col, WEST) == True:
            mode.doMove(row, col, WEST)       
        #elif event.key == 'BackSpace':
            #mode.undoMove(row, col) --> doesn't exist bc it's a set
        
    def validMove(mode, row, col, direction):
    # given current position (row,col), is moving in 'direction' Valid?
    # 1. within bounds of grid
    # 2. there is no wall between currCell and newCell
        (drow, dcol) = direction
        (newrow, newcol) = (row+drow, col+dcol)
        if (not 0 <= newrow < mode.mazeRows) or (not 0 <= newcol < mode.mazeCols):
            return False

        if direction == NORTH:
            if mode.grid[row][col].north == False: return True
        elif direction == EAST:
            if mode.grid[row][col].east == False: return True
        elif direction == SOUTH:
            if mode.grid[row][col].south == False: return True
        elif direction == WEST:
            if mode.grid[row][col].west == False: return True
        return False

    def doMove(mode, row, col, direction):
    # 1. update mode.userPosition
    # 2. add or subtract new position from the mode.userPath set
        # (row, col) = mode.userPosition  --> already stated in keyPressed
        (drow, dcol) = direction
        (newRow, newCol) = (row + drow, col + dcol)
        mode.userPosition = (newRow, newCol)
        if mode.userPosition not in mode.userPath:
            mode.userPath.add(mode.userPosition)
        else:
            mode.userPath.remove((row,col))
        if mode.userPosition == (0,0): 
            mode.userSolvedMaze = True
        #print('userPosition=',mode.userPosition)
        #print('userpath=', mode.userPath)

    #def undoMove(mode, row, col):

    def drawUserPath(mode, canvas):
        for (row, col) in mode.userPath:
            (x0, y0, x1, y1) = mode.getCellBounds(row, col)
            canvas.create_rectangle(x0, y0, x1, y1, fill=mode.mint, width = 0)

    ####################### maze generation #######################
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
        for row in range(mode.mazeRows):
            for col in range(mode.mazeCols):
                (x0, y0, x1, y1) = mode.getCellBounds(row, col) 
                currCell = mode.grid[row][col]
                
                # maze cell color
                canvas.create_rectangle(x0, y0, x1, y1, fill=mode.mazeCellColor, width=0)
                # gold End square
                if (row, col) == (0, 0):
                    color = mode.gold
                    if mode.userPosition == (0,0): color = mode.mint
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
              
    ####################### maze solving #######################
    def drawSolution(mode, canvas):
        
        for (row, col) in mode.solution:
                (x0, y0, x1, y1) = mode.getCellBounds(row, col) 
                if mode.solution[row][col] == True:
                    canvas.create_rectangle(x0, y0, x1, y1, fill=mode.mint, width = 0)

    def createSolution(mode):
    # Citation: hackerearth, geeksforgeeks (see Citations section at top for more details)
        nodesList = [] # init
        (targetRow, targetCol) = (0, 0)
        childToParentDict = dict() # child: parent (no multiples)

        def BFSearch(mode, row, col):  #row, col = starting node
            # base cases
            '''
            if (row,col) in mode.visited: 
                print('did base case1')
                return False
            '''
            mode.visited.append((row,col))
            if (row,col)==(targetRow,targetCol): 
                print('did base case2')
                return True

            # recursive case
            mode.visited[mode.mazeRows-1][mode.mazeCols-1] = True # source node
            print('##############################')
            print(f'Current cell = ({row},{col})')
            for direction in mode.nodeSearchDirections:
                (drow, dcol) = direction # N, E, S, W
                (neighborRow, neighborCol) = (row+drow, col+dcol) #the neighbor node
                
                print('---direction=', direction, '=', (mode.validMove(row, col, direction) and not mode.visited[neighborRow][neighborCol]))
                
                if (mode.validMove(row, col, direction) == True and 
                    mode.visited[neighborRow][neighborCol] == False):
                    print('--------got to if statement!')
                    childToParentDict[(neighborRow, neighborCol)] = (row, col) # child: parent
                    mode.visited[neighborRow][neighborCol] = True # marked as visited, this is now (currRow, currCol)
                    nodesList.insert(0,(neighborRow, neighborCol)) # FI of FIFO
                    print('--------nodesList=', nodesList)
                else:
                    print('--------do nothing')
            nodesList.pop(0) # FO of FIFO
            for (nodeRow, nodeRow) in nodesList:
                print('gonna do recursion...')
                BFSearch(mode, nodeRow, nodeRow)
                print('just did recursion!')
        
        # walking back from target (gold) --> start (mint)
        def getSolution(mode, row, col): # (row, col) = starting cell of path
            # base case
            if (row, col) == (mode.mazeRows-1, mode.mazeCols-1):
                return [(mode.mazeRows-1, mode.mazeCols-1)]
            # recursion
            (parentRow, parentCol) = childToParentDict[(row, col)]
            mode.solution = [(row,col)] +  getSolution(parentRow, parentCol)
                 
        if BFSearch(mode, mode.mazeRows-1, mode.mazeCols-1) == True: #solution can be found from given source node
            print('SOLUTION=', mode.solution)
            return getSolution(mode, targetRow, targetCol)  # return (row, col) tuples of solution path
        else: 
            return False

    ####################### extra features #######################           
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

    def drawMintToGoldInstructions(mode, canvas):
        canvas.create_text(mode.width/2, 687.5, text='Start at the mint, and finish at the gold...', 
                            font=mode.buttonFont, fill=mode.white)
    def drawSolvedText(mode, canvas):
        canvas.create_text(mode.width/2, 687.5, text='Solved!', 
                            font=mode.buttonFont, fill=mode.white)
    def drawTimer(mode, canvas):
        pass
    
    def timerFired(mode):
        pass

    #######################
    def redrawAll(mode, canvas):
        #screen background
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill=mode.mint)
        mode.drawMaze(canvas)
        mode.drawGameButtons(canvas)
        mode.drawUserPath(canvas)
        if mode.userStartedMaze == False:
            mode.drawMintToGoldInstructions(canvas)
        if mode.userSolvedMaze == True:
            mode.drawSolvedText(canvas)
        if mode.showSolution == True:
            mode.drawSolution(canvas)


