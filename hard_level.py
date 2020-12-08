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
        mode.mazeRows = 20
        mode.mazeCols = 20
        mode.mazeCX = mode.width/2
        mode.mazeCY = mode.height/2
        mode.mazeTopLeftCornerX = mode.mazeCX - (mode.cellSize * mode.mazeCols / 2)
        mode.mazeTopLeftCornerY = mode.mazeCY - (mode.cellSize * mode.mazeRows / 2)

        # maze generation - Prim's
        mode.grid = [[MazeCell(False, False, False, False)] * mode.mazeCols for i in range(mode.mazeRows)] #board = 2d list
        mode.predeterminedEdgeValue = 1 # can change for diff graphs
        mode.edgeValuesDict = mode.createEdgeValuesDict()
        mode.mazeGenStartRow = mode.mazeRows - 1 # bottom R corner
        mode.mazeGenStartCol = mode.mazeCols - 1 # bottom R corner
        (mode.targetRow, mode.targetCol) = (0, 0) # top L corner
        mode.visitedPrim = []
        mode.PrimSearchDirections = [NORTH, EAST, SOUTH, WEST] 
        mode.frontier = []

        # extra
        mode.buttonFont = ('Calibri', 15)
        mode.buttonH = 50 # height
        mode.buttonW = 200 # width

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
    # Citation: Jamis Buck (see Citations section at top for more details)
    # No copied code!
        (curRow, curCol) = (mode.mazeGenStartRow, mode.mazeGenStartCol)
        mode.visited.append((curRow, curCol))
        location = None

        while len(mode.visited) < mode.mazeRows * mode.mazeCols:

            # add to Frontier: Unvisited neighbors of curCell 
            for direction in mode.PrimSearchDirections:
                (drow, dcol) = direction # N, E, S, W 
                (neighborRow, neighborCol) = (curRow+drow, curCol+dcol) #the neighbor node
                if (neighborRow, neighborCol) not in mode.visited:
                    mode.frontier.append((neighborRow, neighborCol))
            
            # randomly choose 1 frontier cell
            randomIndex = random.randint(0, len(mode.frontier) - 1) 
            (chosenFrontierRow, chosenFrontierCol) = mode.frontier[randomIndex] 

            # determine chosenCell's LOCATION relative to curCell
            if chosenFrontierCol == curCol - 1: location = 'north'
            elif chosenFrontierRow == curRow + 1: location = 'east'
            elif chosenFrontierCol == curCol + 1: location = 'south'
            elif chosenFrontierRow == curRow -1: location = 'west'

            # carve passage
            if location == 'north':
                mode.grid[curRow][curCol] = MazeCell(False, True, True, True)
            elif location == 'east':
                mode.grid[curRow][curCol] = MazeCell(False, True, False, False)
            elif location == 'south':
                mode.grid[curRow][curCol] = MazeCell(False, False, True, False)
            elif location == 'west':
                mode.grid[curRow][curCol] = MazeCell(False, False, False, True)

            # remove from frontier, add to visited
            mode.frontier.remove((chosenFrontierRow, chosenFrontierCol))
            mode.visited.append((chosenFrontierRow, chosenFrontierCol))

            # prepare for new iteration
            (curRow, curCol) = (chosenFrontierRow, chosenFrontierCol)
            # what should be the new curCell?




                

        
        
        
        return mode.grid # modified list
    def moveIsWithinBounds(mode, row, col, direction):
    # given current position (row,col), is moving in 'direction' within bounds of grid?
        (drow, dcol) = direction
        (newrow, newcol) = (row+drow, col+dcol)
        if (not 0 <= newrow < mode.mazeRows) or (not 0 <= newcol < mode.mazeCols):
            return False
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
    