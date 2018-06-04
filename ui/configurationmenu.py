from tkinter import *
from tkinter.ttk import *

from ui.window import *


class ConfigurationMenu(Menu):
    def __init__(self, window: Window, parent, game: Game):
        super(ConfigurationMenu, self).__init__(window, parent, game)
