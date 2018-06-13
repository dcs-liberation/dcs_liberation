from tkinter import *
from tkinter.ttk import *

from ui.window import *


class NewGameMenu(Menu):
    selected_country = None  # type: IntVar

    def __init__(self, window: Window, callback: typing.Callable):
        super(NewGameMenu, self).__init__(window, None, None)
        self.frame = window.right_pane
        self.callback = callback

        self.selected_country = IntVar()
        self.selected_country.set(0)

    @property
    def player_country_name(self):
        if self.selected_country.get() == 0:
            return "USA"
        else:
            return "Russia"

    @property
    def enemy_country_name(self):
        if self.selected_country.get() == 1:
            return "USA"
        else:
            return "Russia"

    def display(self):
        self.window.clear_right_pane()

        Label(self.frame, text="Player country").grid(row=0, column=0)
        Radiobutton(self.frame, text="USA", variable=self.selected_country, value=0).grid(row=1, column=0)
        Radiobutton(self.frame, text="Russia", variable=self.selected_country, value=1).grid(row=2, column=0)
        Button(self.frame, text="Proceed", command=self.proceed).grid(row=3, column=0)

    def proceed(self):
        self.callback(self.player_country_name, self.enemy_country_name)
