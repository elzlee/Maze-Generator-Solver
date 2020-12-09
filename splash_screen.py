##########################################
# splash screen #
##########################################

import math, copy, random
from cmu_112_graphics import *
from tkinter import *

class SplashScreenMode(Mode):
    def appStarted(mode):
        mode.cellSize = 25
        mode.buttonFont = ('Calibri', 15)
        mode.logoCX = mode.width/2
        mode.logoCY = 300
        mode.logoWidth = 600
        mode.logoHeight = 200
        mode.logoGridRows = 8
        mode.logoGridCols = 24

        #colors shortcut
        mode.mint = '#a2d5c6'
        mode.red = '#b85042'
        mode.white = '#FFFFFF'
        mode.gold = '#fbbc04'

    def getCellBounds(mode, row, col): 
        # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
        gridWidth  = mode.logoWidth
        gridHeight = mode.logoHeight
        logoTopLeftCornerX = mode.logoCX - mode.logoWidth/2
        logoTopLeftCornerY = mode.logoCY - mode.logoHeight/2
        x0 = logoTopLeftCornerX +  col * mode.cellSize
        x1 = logoTopLeftCornerX + (col+1) * mode.cellSize
        y0 = logoTopLeftCornerY + row * mode.cellSize
        y1 = logoTopLeftCornerY + (row+1) * mode.cellSize
        return (x0, y0, x1, y1)

    def mousePressed(mode, event):
        # sectActiveMode of the variable name, not class name
        # BUTTON: 'how to play'
        if (500 <= event.x <= 700) and (500 <= event.y <= 550):
            mode.app.setActiveMode(mode.app.howToPlayMode)
        # BUTTON: 'scoreboard'
        if (500 <= event.x <= 700) and (575 <= event.y <= 625):
            mode.app.setActiveMode(mode.app.scoreboardMode)
        # BUTTON: 'play against AI'
        if (500 <= event.x <= 700) and (650 <= event.y <= 700):
            mode.app.setActiveMode(mode.app.aiMode)
        # BUTTON: 'easy'
        if (275 <= event.x <= 475) and (650 <= event.y <= 700):
            mode.app.setActiveMode(mode.app.easyMode)
        # BUTTON: 'hard'
        if (725 <= event.x <= 925) and (650 <= event.y <= 700):
            mode.app.setActiveMode(mode.app.hardMode)


    def drawLogo(mode, canvas):
        # hardcoded list of 63 (row,col) cells making up 'M A Z E' in logo
        logoLetterCells = [(1,2), (1,3), (1,4), (1,5), (1,6), 
                            (1,8), (1,9), (1,10), (1,11), (1,13), 
                            (1,14), (1,15), (1,16), (1,18), (1,19), 
                            (1,20), (1,21),
                            (2,2), (2,4), (2,6), (2,8), (2,11), 
                            (2,16), (2,18),
                            (3,2), (3,4), (3,6), (3,8), (3,9), 
                            (3,10), (3,11), (3,15), (3,18), (3,19), 
                            (3,20), (3,21),
                            (4,2), (4,4), (4,6), (4,8), (4,11), 
                            (4,14), (4,18),
                            (5,2), (5,4), (5,6), (5,8), (5,11), 
                            (5,13), (5,18),
                            (6,2), (6,4), (6,6), (6,8), (6,11), 
                            (6,13), (6,14), (6,15), (6,16), (6,18), 
                            (6,19), (6,20), (6,21)]
        # draw grid in logo for *aesthetic* effect!
        for row in range(mode.logoGridRows):
            for col in range(mode.logoGridCols):
                (x0, y0, x1, y1) = mode.getCellBounds(row, col)
                if (row, col) in [(0,0), (mode.logoGridRows-1, mode.logoGridCols-1)]:
                    logoCellColor = mode.gold
                elif (row,col) in logoLetterCells:
                    logoCellColor = mode.mint
                    outlineColor = mode.red
                else:
                    logoCellColor = mode.red
                    outlineColor = mode.red

                #doing this if statement at the end somehow solves the bug...
                if (row == 0 or row == mode.logoGridRows-1 or
                    col == 0 or col == mode.logoGridCols-1):
                    outlineColor = ''

                canvas.create_rectangle(x0, y0, x1, y1, fill=logoCellColor,
                                                outline=outlineColor, width=3) 

    def drawSplashButtons(mode, canvas):
        # 5 buttons
        canvas.create_rectangle(500, 500, 700, 550, fill=mode.red, width=0)
        canvas.create_text(mode.width/2, 525,  text='how to play', 
                            font=mode.buttonFont, fill=mode.white)

        canvas.create_rectangle(500, 575, 700, 625, fill=mode.red, width=0)
        canvas.create_text(mode.width/2, 600,  text='scoreboard', 
                            font=mode.buttonFont, fill=mode.white)

        canvas.create_rectangle(500, 650, 700, 700, fill=mode.red, width=0)
        canvas.create_text(mode.width/2, 675,  text='play against ai', 
                            font=mode.buttonFont, fill=mode.white)

        canvas.create_rectangle(275, 650, 475, 700, fill=mode.red, width=0)
        canvas.create_text(mode.width/2 - 225, 675,  text='play solo - easy', 
                            font=mode.buttonFont, fill=mode.white)

        canvas.create_rectangle(725, 650, 925, 700, fill=mode.red, width=0)
        canvas.create_text(mode.width/2 + 225, 675,  text='play solo - hard', 
                            font=mode.buttonFont, fill=mode.white)

    def redrawAll(mode, canvas):
        #screen background
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill=mode.mint)
        #MAZE logo
        mode.drawLogo(canvas)
        #description
        #canvas.create_text(mode.width/2, 450,  
                            #text='15112 Fall 2020 Term Project by Elizabeth Lee', 
                            #font='Calibri 13', fill=mode.white)
        # 5 buttons
        mode.drawSplashButtons(canvas)

