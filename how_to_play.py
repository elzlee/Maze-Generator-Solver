from cmu_112_graphics import *
from tkinter import *

class HowToPlayMode(Mode):

    def appStarted(mode):
        mode.buttonFont = ('Calibri', 15)
        mode.titleFont = ('Calibri', 50)
        mode.buttonH = 50 # height
        mode.buttonW = 200 # width

        #colors shortcut
        mode.mint = '#a2d5c6'
        mode.red = '#b85042'
        mode.white = '#FFFFFF'
        mode.gold = '#fbbc04'

    def mousePressed(mode, event):
        # BUTTON: 'menu'
        b3cx = mode.width/2
        b3cy = mode.height - 50 
        if (((b3cx - mode.buttonW/2) <= event.x <= (b3cx + mode.buttonW/2)) and 
            ((b3cy - mode.buttonH/2) <= event.y <= (b3cy + mode.buttonH/2))):
            mode.app.setActiveMode(mode.app.splashScreenMode)

    def drawText(mode, canvas):
        canvas.create_text(mode.width/2, 100, font=mode.titleFont, fill=mode.white,
                            text = 'how to play')
        howToPlayText = (
                        '*** SOLO MODE ***\n' 
                        '\n'
                        '2 Levels: Easy & Hard\n'
                        '\n'
                        '\n'
                        '\n'
                        '*** GAME AI MODE ***\n' 
                        '\n'
                        'Compete against the game AI!\n'
                        '\n'
                        'Be ready! The timer and the AI starts as soon as you enter the mode.\n' 
                        '\n'
                        '\n'
                        '\n'
                        '*** GENERAL GAMEPLAY ***\n' 
                        '\n'
                        'Bring the Mint square to the Gold square to complete the maze!\n' 
                        '\n'
                        'Use the UP/DOWN/LEFT/RIGHT keys to traverse the maze.'
                        )
        canvas.create_text(mode.width/2, mode.height/2, 
                            font = mode.buttonFont, fill = mode.red,
                            text = howToPlayText)

    def drawGameButtons(mode, canvas):
        # return to menu button = bottom center
        b3cx = mode.width/2
        b3cy = mode.height - 50 
        canvas.create_rectangle(b3cx - mode.buttonW/2, b3cy - mode.buttonH/2, 
                                b3cx + mode.buttonW/2, b3cy + mode.buttonH/2, 
                                fill=mode.red, width=0)
        canvas.create_text(b3cx, b3cy, text='MENU', 
                            font=mode.buttonFont, fill=mode.white)

    def redrawAll(mode, canvas):
        #screen background
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill=mode.mint)
        mode.drawGameButtons(canvas)
        mode.drawText(canvas)


