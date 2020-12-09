##########################################
# Hard maze level
# Perfect maze generation: Prim's
# Maze Searching: Breadth First Search 
# Pathfinding: parent/child connection
##########################################
# Citations referenced in this file #
    # Jamis Buck: 'An Example' section only
    # https://weblog.jamisbuck.org/2011/1/10/maze-generation-prim-s-algorithm


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

class HardMode(Mode):
    ####################### init #######################
    def appStarted(mode):
        #colors shortcut
        mode.mint = '#a2d5c6'
        mode.red = '#b85042'
        mode.white = '#FFFFFF'
        mode.gold = '#fbbc04'

        # general maze 
        mode.cellSize = 25
        mode.mazeRows = 3
        mode.mazeCols = 3
        mode.mazeCX = mode.width/2
        mode.mazeCY = mode.height/2
        mode.mazeTopLeftCornerX = mode.mazeCX - (mode.cellSize * mode.mazeCols / 2)
        mode.mazeTopLeftCornerY = mode.mazeCY - (mode.cellSize * mode.mazeRows / 2)
        mode.mazeCellColor = mode.white
        mode.mazeWallColor = mode.red

        # maze generation - Prim's
        mode.primSearchDirections = [NORTH, EAST, SOUTH, WEST] 
        mode.predeterminedEdgeValue = 1 # can change for diff graphs
        #mode.edgeValuesDict = mode.createEdgeValuesDict()
        mode.mazeGenStartRow = mode.mazeRows - 1 # bottom R corner
        mode.mazeGenStartCol = mode.mazeCols - 1 # bottom R corner
        (mode.targetRow, mode.targetCol) = (0, 0) # top L corner
        mode.visitedPrim = []
        mode.frontier = set()
        mode.grid = [[MazeCell(True, True, True, True)] * mode.mazeCols for i in range(mode.mazeRows)] #board = 2d list
        mode.createMaze()
        #print('mode.grid=', mode.grid)
        #print('mode.visitedPrim=', mode.visitedPrim)

        # user, path
        mode.userPosition = (mode.mazeRows-1, mode.mazeCols-1) #update with row, drow, etc.
        mode.userPath = set() # to be filled...
        mode.userPath.add((mode.mazeRows-1, mode.mazeCols-1)) # add first position
        mode.userStartedMaze = False
        mode.userSolvedMaze = False

        # extra
        mode.buttonFont = ('Calibri', 15)
        mode.buttonH = 50 # height
        mode.buttonW = 200 # width

    '''
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
                for direction in mode.primSearchDirections: # N, E, S, W
                    (drow, dcol) = direction 
                    if mode.validMove(curRow, curCol, direction, 'aiMaze') == True: 
                        (neighborRow, neighborCol) = (curRow+drow, curCol+dcol)
                        mode.edgeValuesDict[((curRow, curCol), (neighborRow, neighborCol))] = mode.predeterminedEdgeValue
        return mode.edgeValuesDict
    '''

    def getCellBounds(mode, row, col): 
    # Citation: CMU 15112 course notes
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
        x0 = mode.mazeTopLeftCornerX +  col * mode.cellSize
        x1 = mode.mazeTopLeftCornerX + (col+1) * mode.cellSize
        y0 = mode.mazeTopLeftCornerY + row * mode.cellSize
        y1 = mode.mazeTopLeftCornerY + (row+1) * mode.cellSize
        return (x0, y0, x1, y1)
  
    ####################### maze generation #######################

    def createMaze(mode): # Prim's algorithm

        (curRow, curCol) = (mode.mazeGenStartRow, mode.mazeGenStartCol)
        mode.visitedPrim.append((curRow, curCol))
        location = None
        
        counter = 0
        while len(mode.visitedPrim) <= mode.mazeRows * mode.mazeCols - 1:
        # while there are unvisited cells
            print('##########################')
            print('iteration', counter)
            #if counter == 4: break
            # add to Frontier list: Unvisited neighbors of curCell 
            visitedNeighborsOfFrontierCell = set()

            for direction in mode.primSearchDirections:
                if mode.moveIsWithinBounds(curRow, curCol, direction) == True:
                    (drow, dcol) = direction # N, E, S, W 
                    (neighborRow, neighborCol) = (curRow+drow, curCol+dcol) #the neighbor node
                    if (neighborRow, neighborCol) not in (mode.visitedPrim and mode.frontier):
                        mode.frontier.add((neighborRow, neighborCol))

            # from now on, curCell doesn't matter!!! very cool

            # randomly choose 1 frontier cell from list
            (chosenFrontierRow, chosenFrontierCol) = random.choice(tuple(mode.frontier))
            print('frontier=', mode.frontier)

            # create list of fNeighbors of the frontier cells
            for direction in mode.primSearchDirections:
                if mode.moveIsWithinBounds(chosenFrontierRow, chosenFrontierCol, direction) == True:
                    (drow, dcol) = direction # N, E, S, W
                    (fNeighborRow, fNeighborCol) = (chosenFrontierRow+drow, chosenFrontierCol+dcol)
                    if (fNeighborRow, fNeighborCol) in mode.visitedPrim:
                        visitedNeighborsOfFrontierCell.add((fNeighborRow, fNeighborCol))
            
            # randomly choose 1 fNeighbor cell (in case there are more than 1)
            (chosenFNeighborRow, chosenFNeighborCol) = random.choice(tuple(visitedNeighborsOfFrontierCell))
            # find chosenFNeighborCell's LOCATION relative to chosenFrontierCell
            if chosenFNeighborRow == chosenFrontierRow - 1: location = 'north'
            elif chosenFNeighborCol == chosenFrontierCol + 1: location = 'east'
            elif chosenFNeighborRow == chosenFrontierRow + 1: location = 'south'
            elif chosenFNeighborCol == chosenFrontierCol -1: location = 'west'

            # carve passage
            print('chosenFrontier visited?=', (chosenFrontierRow, chosenFrontierCol),(chosenFrontierRow, chosenFrontierCol) in mode.visitedPrim)
            print('chosenFNeighbor visited?=', (chosenFNeighborRow, chosenFNeighborCol), (chosenFNeighborRow, chosenFNeighborCol) in mode.visitedPrim)
            chosenFrontierCell = mode.grid[chosenFrontierRow][chosenFrontierCol]
            chosenFNeighborCell = mode.grid[chosenFNeighborRow][chosenFNeighborCol]
            if location == 'north':
                chosenFrontierCell.north = False
                chosenFNeighborCell.south = False
            elif location == 'east':
                chosenFrontierCell.east = False
                chosenFNeighborCell.west = False
            elif location == 'south':
                chosenFrontierCell.south = False
                chosenFNeighborCell.north = False
            elif location == 'west':
                chosenFrontierCell.west = False
                chosenFNeighborCell.east = False

            # remove from frontier, add to visited
            #print('frontier:', mode.frontier)
            mode.frontier.remove((chosenFrontierRow, chosenFrontierCol))
            mode.visitedPrim.append((chosenFrontierRow, chosenFrontierCol))

            # prepare for new iteration
            (curRow, curCol) = (chosenFrontierRow, chosenFrontierCol)

            counter +=1 
            
            print('mode.visitedPrim=', mode.visitedPrim)
            '''
            print(mode.grid[4][4].west)
            print(mode.grid[4][4].north)
            print(mode.grid[4][3].north)
            print(mode.grid[3][3].south)
            print(mode.grid[4][2].north)
            print(mode.grid[3][2].south)
            print(mode.grid[4][1].north)
            print(mode.grid[3][1].south)
            '''
            
        return mode.grid # modified list
    
    
    def moveIsWithinBounds(mode, row, col, direction): #done
    # given current position (row,col), is moving in 'direction' within bounds of grid?
        (drow, dcol) = direction
        (newrow, newcol) = (row+drow, col+dcol)
        if (not 0 <= newrow < mode.mazeRows) or (not 0 <= newcol < mode.mazeCols):
            return False
        else:
            return True

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
    '''
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
            mode.showSolution = not mode.showSolution

        # BUTTON: 'menu'
        b3cx = mode.width/2
        b3cy = mode.height - 50 
        if (((b3cx - mode.buttonW/2) <= event.x <= (b3cx + mode.buttonW/2)) and 
            ((b3cy - mode.buttonH/2) <= event.y <= (b3cy + mode.buttonH/2))):
            mode.app.setActiveMode(mode.app.splashScreenMode)
        '''
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


    #def undoUserMove(mode, row, col):

    def drawUserPath(mode, canvas):
        for (row, col) in mode.userPath:
            (x0, y0, x1, y1) = mode.getCellBounds(row, col)
            canvas.create_rectangle(x0, y0, x1, y1, fill=mode.mint, width = 0)

    #######################
    def redrawAll(mode, canvas):
        #screen background
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill=mode.mint)
        mode.drawMaze(canvas)
        mode.drawUserPath(canvas)
        '''
        mode.drawMenuButton(canvas)
        mode.drawUserPath(canvas)
        if mode.userStartedMaze == False and mode.showSolution == False:
            mode.drawMintToGoldInstructions(canvas)
        if mode.userSolvedMaze == True:
            mode.drawSolvedText(canvas)
            mode.drawSolvedRed(canvas)
        else:
            mode.drawHintSolutionButtons(canvas)
        if mode.showSolution == True:
            mode.drawSolution(canvas)
        '''

