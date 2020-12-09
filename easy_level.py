##########################################
# Easy maze level
# Perfect maze generation: Binary Tree
# Maze Searching: Breadth First Search 
# Pathfinding: parent/child connection
##########################################
# Citations referenced in this file #
    # Jamis Buck (binary tree): 'An Example' section only
    # http://weblog.jamisbuck.org/2011/2/1/maze-generation-binary-tree-algorithm#
    
    # hackerearth: 'Pseudocode' section, 'Visualizer' section
    # https://www.hackerearth.com/practice/algorithms/graphs/breadth-first-search/tutorial/

    # geeksforgeeks: 
    # https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/?ref=leftbar-rightbar

    # CMU 15112 course notes (getCellBounds)
    # https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
##########################################


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
    def modeActivated(mode):
        #colors shortcut
        mode.mint = '#a2d5c6'
        mode.red = '#b85042'
        mode.white = '#FFFFFF'
        mode.gold = '#fbbc04'

        # maze
        mode.cellSize = 25
        mode.mazeRows = 10 # increase for difficulty
        mode.mazeCols = 10 # increase for difficulty
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

        # pathfinding: solution, hint
        mode.showSolution = False
        mode.showHint = False
        mode.currNode = (mode.mazeRows-1, mode.mazeCols-1) # init
        mode.visited = [[False] * mode.mazeCols for i in range(mode.mazeRows)] # 2d list of maze cells, True=visited

        mode.nodeSearchDirections = [NORTH, EAST, SOUTH, WEST] 
        mode.solution  = [] # list of tuples
        mode.createSolution()
        
        # timer
        mode.elapsedTime = 0
        mode.elapsedSeconds = 0
        mode.seconds = 0
        mode.minutes = 0
        mode.timerFont = ('Calibri', 80)
        mode.timerDelay = 82.5
        
    def getCellBounds(mode, row, col): 
    # Citation: CMU 15112 course notes
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
        x0 = mode.mazeTopLeftCornerX +  col * mode.cellSize
        x1 = mode.mazeTopLeftCornerX + (col+1) * mode.cellSize
        y0 = mode.mazeTopLeftCornerY + row * mode.cellSize
        y1 = mode.mazeTopLeftCornerY + (row+1) * mode.cellSize
        return (x0, y0, x1, y1)

    ####################### maze generation #######################
    def createMaze(mode):
    # Citation: Jamis Buck (binary tree) (see Citations section at top for more details)
    # No copied code!
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
        # thicker border
        halfwidth = mode.mazeCols * mode.cellSize / 2
        halfheight = mode.mazeRows * mode.cellSize / 2
        canvas.create_rectangle(mode.mazeCX-halfwidth, mode.mazeCY-halfheight,
                                mode.mazeCX+halfwidth, mode.mazeCY+halfheight, 
                                outline=mode.red, width=6)
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
                    canvas.create_line(x0, y0, x1, y0, fill=mode.mint, width=6)
                if (row, col) == (mode.mazeRows-1, mode.mazeCols-1):
                    canvas.create_line(x0, y1, x1, y1, fill=mode.mint, width=6)
    
    ####################### user interaction #######################
    def mousePressed(mode, event):
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
            mode.doUserMove(row, col, NORTH)
        elif event.key == 'Right' and mode.validMove(row, col, EAST) == True:
            mode.doUserMove(row, col, EAST)
        elif event.key == 'Down' and mode.validMove(row, col, SOUTH) == True:
            mode.doUserMove(row, col,  SOUTH)
        elif event.key == 'Left' and mode.validMove(row, col, WEST) == True:
            mode.doUserMove(row, col, WEST)       
        #elif event.key == 'BackSpace':
            #mode.undoUserMove(row, col) --> doesn't exist bc it's a set
        
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

    def doUserMove(mode, row, col, direction):
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

    def drawUserPath(mode, canvas):
        for (row, col) in mode.userPath:
            (x0, y0, x1, y1) = mode.getCellBounds(row, col)
            canvas.create_rectangle(x0, y0, x1, y1, fill=mode.mint, width = 0)

    ####################### maze solving #######################
    def drawSolution(mode, canvas): 
        for row in range(mode.mazeRows):
            for col in range(mode.mazeCols):
                (x0, y0, x1, y1) = mode.getCellBounds(row, col) 
                if (row, col) in mode.solution:
                    canvas.create_rectangle(x0, y0, x1, y1, fill=mode.mint, width = 0)
                else:
                    canvas.create_rectangle(x0, y0, x1, y1, fill=mode.red, width = 0)

    def createSolution(mode):
    # Citation: hackerearth, geeksforgeeks (see Citations section at top for more details)
    # No copied code!
        nodesQueue = [] # init
        (targetRow, targetCol) = (0, 0)
        childToParentDict = dict() # child: parent (no multiples)

        def BFSearch(mode, row, col):  #row, col = starting node
            mode.visited[row][col] = True # visit given source node
            nodesQueue.append((row, col)) # enqueue given source node

            while len(nodesQueue) != 0:
                (curRow, curCol) = nodesQueue.pop(0) # FO of FIFO
                if (curRow, curCol) == (targetRow, targetCol):
                    return True # exit loop

                #loop over neighbors
                for direction in mode.nodeSearchDirections:
                    (drow, dcol) = direction # N, E, S, W
                    if mode.validMove(curRow, curCol, direction) == True: 
                        (neighborRow, neighborCol) = (curRow+drow, curCol+dcol) #the neighbor node
                        if mode.visited[neighborRow][neighborCol] == False:
                            childToParentDict[(neighborRow, neighborCol)] = (curRow, curCol) # {child: parent}
                            mode.visited[neighborRow][neighborCol] = True # marked as visited, this is now (currRow, currCol)
                            nodesQueue.append((neighborRow, neighborCol)) # FI of FIFO
            return False

        # walking back from target (gold) --> start (mint)
        def getSolution(mode, row, col): # (row, col) = starting cell of path
            # base case
            if (row, col) == (mode.mazeRows-1, mode.mazeCols-1):
                return [(mode.mazeRows-1, mode.mazeCols-1)]
            # recursion
            else:
                (parentRow, parentCol) = childToParentDict[(row, col)]
                mode.solution = [(row,col)] +  getSolution(mode, parentRow, parentCol)
                return mode.solution
                 
        if BFSearch(mode, mode.mazeRows-1, mode.mazeCols-1) == True: #solution can be found from given source node
            solution = getSolution(mode, targetRow, targetCol)
            return solution # return (row, col) tuples of solution path
        else: 
            return False

    ####################### timer #######################           
    def timerFired(mode):
        if mode.userStartedMaze == True and mode.userSolvedMaze == False and mode.showSolution == False:
            mode.elapsedTime += 1
            if mode.elapsedTime % 10 == 0:
                mode.elapsedSeconds += 1
                print(mode.elapsedSeconds)
                mode.getElapsedMinutesAndSeconds()
                print('delay=', mode.timerDelay)
    
    def getElapsedMinutesAndSeconds(mode):
        mode.minutes = mode.elapsedSeconds // 60
        mode.seconds = mode.elapsedSeconds % 60

    def drawTimer(mode, canvas):
        if mode.seconds == 0: seconds = '00'
        elif mode.seconds < 10: seconds = '0' + str(mode.seconds)
        else: seconds = str(mode.seconds)

        if mode.minutes == 0: minutes = '00'
        elif mode.seconds < 10: minutes = '0' + str(mode.minutes)
        else: minutes = str(mode.minutes)

        timerText = minutes + ':' + seconds
        canvas.create_text(mode.width/2, 75, text=timerText, 
                            font=mode.timerFont, fill=mode.white)
    
    ####################### extra features #######################           
    def drawHintButton(mode, canvas):
        # hint button = left
        b1cx = (mode.mazeCX - (mode.mazeCols * mode.cellSize) / 2) / 2
        b1cy = mode.mazeCY
        canvas.create_rectangle(b1cx - mode.buttonW/2, b1cy - mode.buttonH/2, 
                                b1cx + mode.buttonW/2, b1cy + mode.buttonH/2, 
                                fill=mode.white, width=0)
        canvas.create_text(b1cx, b1cy, text='hint', 
                            font=mode.buttonFont, fill=mode.red)
    def drawSolutionButton(mode, canvas):
        # solution button = right
        b1cx = (mode.mazeCX - (mode.mazeCols * mode.cellSize) / 2) / 2
        b2cx = mode.width - b1cx
        b2cy = mode.mazeCY
        canvas.create_rectangle(b2cx - mode.buttonW/2, b2cy - mode.buttonH/2, 
                                b2cx + mode.buttonW/2, b2cy + mode.buttonH/2, 
                                fill=mode.red, width=0)
        canvas.create_text(b2cx, b2cy, text='give up', 
                            font=mode.buttonFont, fill=mode.white)

    def drawMenuButton(mode, canvas):
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
    def drawSolvedRed(mode, canvas):
        for row in range(mode.mazeRows):
            for col in range(mode.mazeCols):
                (x0, y0, x1, y1) = mode.getCellBounds(row, col) 
                if (row, col) not in mode.solution:
                    canvas.create_rectangle(x0, y0, x1, y1, fill=mode.red, width = 0)
    def drawKeepGoing(mode, canvas):
        canvas.create_text(mode.width/2, 687.5, text='Keep going!', 
                            font=mode.buttonFont, fill=mode.white)
    def drawTryAnotherMaze(mode, canvas):
        canvas.create_text(mode.width/2, 687.5, text='Return to menu to try another maze!', 
                            font=mode.buttonFont, fill=mode.white)
    #######################
    def redrawAll(mode, canvas):
        # always there
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill=mode.mint) #canvas background
        mode.drawMaze(canvas)
        mode.drawMenuButton(canvas)
        mode.drawUserPath(canvas)
        

        if mode.showSolution == False:
            mode.drawTimer(canvas)
            if mode.userStartedMaze == False :
                mode.drawMintToGoldInstructions(canvas)
            elif mode.userStartedMaze == True :
                if mode.userSolvedMaze == False:
                    mode.drawKeepGoing(canvas)

            if mode.userSolvedMaze == False:
                mode.drawSolutionButton(canvas)
                mode.drawHintButton(canvas)
            elif mode.userSolvedMaze == True:
                mode.drawSolvedText(canvas)
                mode.drawSolvedRed(canvas)

        elif mode.showSolution == True:
            mode.drawSolution(canvas)
            mode.drawTryAnotherMaze(canvas)

        
