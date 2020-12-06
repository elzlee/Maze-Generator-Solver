#################
# __main__.py #
#################
# mode. = self. = 1st arg

import math, copy, random
from cmu_112_graphics import *
from tkinter import *
from splash_screen import *
from how_to_play import *
from easy_level import *
from ai_mode import *
#from medium_level import *


# class = capital first letters
# functions = camel style 

class ScoreBoardMode(Mode):
    pass

class MediumMode(Mode):
    pass

class HardMode(Mode):
    pass

class MyModalApp(ModalApp):
    def appStarted(app):
        app.splashScreenMode = SplashScreenMode()
        app.howToPlayMode = HowToPlayMode()
        #app.scoreBoardMode = ScoreBoardMode()print('nodesQueue=', nodesQueue)
        #app.mediumMode = MediumMode()
        app.easyMode = EasyMode()
        #app.hardMode = HardMode()
        app.aiMode = AIMode_class()
        app.setActiveMode(app.splashScreenMode)
        #app.timerDelay = 50

app = MyModalApp(width=1200, height=800)
