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
from bt_ai_mode import *
from hard_level import *

# class = capital first letters
# functions = camel style 

class MyModalApp(ModalApp):
    def appStarted(app):
        app.splashScreenMode = SplashScreenMode()
        app.howToPlayMode = HowToPlayMode()
        app.easyMode = EasyMode()
        app.hardMode = HardMode()
        app.aiMode = AIMode_class()
        app.setActiveMode(app.splashScreenMode)

app = MyModalApp(width=1200, height=800)
