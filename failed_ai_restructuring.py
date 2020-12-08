##########################################
# Game AI Mode
# Perfect maze generation: Binary Tree (to be switched to Random later)
# Maze solving: Dijkstra's
##########################################
# Citations referenced in this file #
    # Wikipedia: pseudocode
    # https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm

    # geeksforgeeks: pseudocode
    # https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-greedy-algo-7/
##########################################
import math, copy, random
from cmu_112_graphics import *
from tkinter import *
import time

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

####################### AIMode_class #######################       

class AIMode_class(Mode):
    def appStarted(mode):
        #mode.timerDelay = 250

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
        mode.mazeRows = 4
        mode.mazeCols = 4
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

        # ai pathfinding
        # mode.priorityQueue is just a normal list
        mode.priorityQueue = [] # init, [(distance, mode.tieBreaker, (row, col))]
        mode.tieBreaker = 0
        mode.nodeSearchDirections = [NORTH, EAST, SOUTH, WEST] 
        # mode.visited = [[False] * mode.mazeCols for i in range(mode.mazeRows)] # 2d list, True=visited
        mode.visited = []
        mode.distance = [[0] * mode.mazeCols for i in range(mode.mazeRows)] # 2d list, distance from Source Node
        mode.predeterminedEdgeValue = 1 # can change for diff graphs
        mode.edgeValuesDict = mode.createEdgeValuesDict()
        mode.aiSolution  = [] # list of tuples
        mode.createSolution()

        # ai visualization
        mode.indexOfVisitedCell = 0
        
        # flags
        mode.aiSolvedMaze = False
        mode.userSolvedMaze = False
        mode.userStartedMaze = False
        mode.gameOver = False #true if there's a winner

    def createEdgeValuesDict(mode):
    # Saving edge values is unnecessary for my specific mazes, but
    # this maintains the spirit of Dijkstra's algorithm.
    # mode.edgeValuesDict can be manually edited for other graphs
    # to assign varying edge values (instead of constant value mode.predeterminedEdgeValue=1)
        # key: ((row1, col1), (row2, col2))
        # value: edge value between cell1 and cell2
        mode.edgeValuesDict = dict()
        for row in range(mode.mazeRows):
            for col in range(mode.mazeCols):
                curRow, curCol = row, col
                for direction in mode.nodeSearchDirections: # N, E, S, W
                    (drow, dcol) = direction 
                    if mode.validMove(curRow, curCol, direction, 'aiMaze') == True: 
                        (neighborRow, neighborCol) = (curRow+drow, curCol+dcol)
                        mode.edgeValuesDict[((curRow, curCol), (neighborRow, neighborCol))] = mode.predeterminedEdgeValue
        return mode.edgeValuesDict

    def getCellBounds(mode, row, col, mazeType): 
    # Citation: CMU 15112 course notes
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
   
   
    def gameOver(mode):
        #if (mode.userPosition == (0,0)) or aiSolvedMaze :
            # mode.gameOver = True
        pass

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
            mode.aiGrid[row][col] = MazeCell(True, True, False, True)
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
        # thicker maze border
        halfwidth = mode.mazeCols * mode.cellSize / 2
        halfheight = mode.mazeRows * mode.cellSize / 2
        canvas.create_rectangle(mode.userMazeCX-halfwidth, mode.userMazeCY-halfheight,
                                mode.userMazeCX+halfwidth, mode.userMazeCY+halfheight, 
                                outline=mode.red, width=6)
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
        # thicker maze border
        halfwidth = mode.mazeCols * mode.cellSize / 2
        halfheight = mode.mazeRows * mode.cellSize / 2
        canvas.create_rectangle(mode.aiMazeCX-halfwidth, mode.aiMazeCY-halfheight,
                                mode.aiMazeCX+halfwidth, mode.aiMazeCY+halfheight, 
                                outline=mode.red, width=6)
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
            canvas.create_line(x0, y0, x1, y0, fill=mode.mint, width=6)
        if (row, col) == (mode.mazeRows-1, mode.mazeCols-1):
            canvas.create_line(x0, y1, x1, y1, fill=mode.mint, width=6)
            
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
# Citation: geeksforgeeks, wikipedia (see Citations section at top for more details)
# No copied code!

    def createSolution(mode): 
        print('here')
        (targetRow, targetCol) = (0, 0)
        if mode.dijkstraSearch(mode.mazeRows-1, mode.mazeCols-1) == True: #solution found from given source node
            mode.aiSolution = mode.getShortestPath(targetRow, targetCol)
            print('visited at finish sol=', mode.visited)
            return mode.aiSolution # return (row, col) tuples of solution path
        else: 
            print('else')
            return False

    def dijkstraSearch(mode, row, col):
        (targetRow, targetCol) = (0, 0)

        # set up Source Node
        # [row][col] = True 
        mode.visited.append((row, col))
        mode.distance[row][col] = 0
        mode.priorityQueue.append((mode.distance[row][col], mode.tieBreaker, (row, col))) # enqueue given source node

        while len(mode.priorityQueue) != 0:
            mode.priorityQueue.sort()
            (d, t, (curRow, curCol)) = mode.priorityQueue.pop(0) # pop node w/ smallest distance & mode.tiebreaker
            if (curRow, curCol) == (targetRow, targetCol):
                return True # exit loop
            mode.doAIMazeSearchStep(curRow, curCol)
        return False

    def doAIMazeSearchStep(mode, curRow, curCol):
        #loop over neighbors
        for direction in mode.nodeSearchDirections:
            (drow, dcol) = direction # N, E, S, W 
            if mode.validMove(curRow, curCol, direction, 'aiMaze') == True:
                (neighborRow, neighborCol) = (curRow+drow, curCol+dcol) #the neighbor node
                # if mode.visited[neighborRow][neighborCol] == False:
                if (neighborRow, neighborCol) in mode.visited:
                    mode.tieBreaker+= 1
                    # mode.visited[neighborRow][neighborCol] = True
                    mode.visited.append((neighborRow, neighborCol))
                    mode.distance[neighborRow][neighborCol] = (mode.edgeValuesDict[((curRow, curCol), (neighborRow, neighborCol))]
                                                                + mode.distance[curRow][curCol])
                    updatedDistance = mode.distance[neighborRow][neighborCol]
                    mode.priorityQueue.append((updatedDistance, mode.tieBreaker, (neighborRow, neighborCol)))

    def getShortestPath(mode, row, col): # DONE
    # walking back from target (gold) --> start (mint)
        (curRow, curCol) = (row, col)
        # base case
        if (row, col) == (mode.mazeRows-1, mode.mazeCols-1):
            return [(mode.mazeRows-1, mode.mazeCols-1)]
        # recursion
        else:
            for direction in mode.nodeSearchDirections:
                (drow, dcol) = direction # N, E, S, W
                if mode.validMove(curRow, curCol, direction, 'aiMaze') == True: 
                    (neighborRow, neighborCol) = (curRow+drow, curCol+dcol) 
                    if mode.distance[neighborRow][neighborCol] == mode.distance[curRow][curCol] - 1:
                        (prevRow, prevCol) = (neighborRow,neighborCol)
                        mode.aiSolution = [(curRow, curCol)] + mode.getShortestPath(prevRow, prevCol)
                        return mode.aiSolution

    '''
    def timerFired(mode):
        if mode.gameOver == False:
            mode.getIndexOfVisitedCellToPrint()
            print('index=', mode.indexOfVisitedCell)
            #mode.doAIMazeSearchStep(curRow, curCol)
        
    def getIndexOfVisitedCellToPrint(mode):
        time.sleep(1)
        mode.indexOfVisitedCell += 1
    ''' 

    def drawAIVisitedCells(mode, canvas):
    # ai maze solving HELPER function
        '''
        index = mode.indexOfVisitedCell
        (row, col) = mode.visited[index]
        (x0, y0, x1, y1) = mode.getCellBounds(row, col, 'aiMaze') 
        canvas.create_rectangle(x0, y0, x1, y1, fill=mode.mint, width = 0)
        '''
        for row in range(mode.mazeRows):
            for col in range(mode.mazeCols):
                # if mode.visited[row][col] == True:
                if (row, col) in mode.visited:
                    (x0, y0, x1, y1) = mode.getCellBounds(row, col, 'aiMaze') 
                    canvas.create_rectangle(x0, y0, x1, y1, fill=mode.red, width = 0)
                    time.sleep(1)


    def drawAISolution(mode, canvas): # DONE
    # ai maze solving HELPER function
        for row in range(mode.mazeRows):
            for col in range(mode.mazeCols):
                (x0, y0, x1, y1) = mode.getCellBounds(row, col, 'aiMaze') 
                if (row, col) in mode.aiSolution:
                    canvas.create_rectangle(x0, y0, x1, y1, fill=mode.mint, width = 0)
                else:
                    canvas.create_rectangle(x0, y0, x1, y1, fill=mode.red, width = 0)

    def drawAIMazeProgress(mode, canvas): #DONE
    # ai maze solving MAIN function
        mode.drawAIVisitedCells(canvas)
        (targetRow, targetCol) = (0, 0)
        if (targetRow, targetCol) in mode.visited:
            mode.drawAISolution(canvas)
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

    def drawPlayerLabels(mode, canvas): #DONE
        canvas.create_text(mode.userLabelCX, mode.userLabelCY, text='you', 
                            font=mode.playerLabelFont, fill=mode.white)
        canvas.create_text(mode.aiLabelCX, mode.aiLabelCY, text='ai', 
                            font=mode.playerLabelFont, fill=mode.white)
                   
    def drawWinnerLoserLabels(mode, canvas):
        if mode.winner == 'user':
            canvas.create_text(mode.userLabelCX, mode.userLabelCY, text='you win :)', 
                            font=mode.playerLabelFont, fill=mode.white)
            canvas.create_text(mode.aiLabelCX, mode.aiLabelCY, text='ai', 
                            font=mode.playerLabelFont, fill=mode.white)
        elif mode.winner == 'ai':
            canvas.create_text(mode.userLabelCX, mode.userLabelCY, text='you lose :(', 
                            font=mode.playerLabelFont, fill=mode.white)
            canvas.create_text(mode.aiLabelCX, mode.aiLabelCY, text='ai', 
                            font=mode.playerLabelFont, fill=mode.white)

    def drawTimer(mode, canvas): #important for game ai mode!
        pass

    #####################################################################

    def redrawAll(mode, canvas):
        #screen background
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill=mode.mint)
        mode.drawGameButtons(canvas)
        mode.drawUserMaze(canvas)
        mode.drawAIMaze(canvas)
        mode.drawUserPath(canvas)
        mode.drawAIMazeProgress(canvas)
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
