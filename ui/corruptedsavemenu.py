from tkinter import *
from tkinter.ttk import *
from .styles import STYLES

from ui.window import *


class CorruptedSaveMenu(Menu):
    def __init__(self, window: Window):
        super(CorruptedSaveMenu, self).__init__(window, None, None)
        self.frame = window.right_pane

    def display(self):
        self.window.clear_right_pane()

        Label(text="Your save game is either incompatible or was corrupted!", **STYLES["widget"]).grid(row=0, column=0)
        Label(text="Please restore it by replacing \"liberation_save\" file with \"liberation_save_tmp\" to restore last saved copy.", **STYLES["widget"]).grid(row=1, column=0)
        Label(text="You can find those files under user Saved Games\\DCS directory.", **STYLES["widget"]).grid(row=2, column=0)
