from tkinter import *
from tkinter import Menu as TkMenu
from tkinter import messagebox

from .styles import BG_COLOR,BG_TITLE_COLOR
from game.game import *
from theater import persiangulf, nevada, caucasus, start_generator
from userdata import logging as logging_module

import sys
import webbrowser


class Window:

    image = None
    left_pane = None  # type: Frame
    right_pane = None  # type: Frame

    def __init__(self):
        self.tk = Tk()
        self.tk.title("DCS Liberation")
        self.tk.iconbitmap("resources/icon.ico")
        self.tk.resizable(False, False)
        self.tk.grid_columnconfigure(0, weight=1)
        self.tk.grid_rowconfigure(0, weight=1)

        self.frame = None
        self.right_pane = None
        self.left_pane = None
        self.build()

        menubar = TkMenu(self.tk)
        filemenu = TkMenu(menubar, tearoff=0)
        filemenu.add_command(label="New Game", command=lambda: self.new_game_confirm())
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=lambda: self.exit())
        menubar.add_cascade(label="File", menu=filemenu)

        helpmenu = TkMenu(menubar, tearoff=0)
        helpmenu.add_command(label="Online Manual", command=lambda: webbrowser.open_new_tab("https://github.com/shdwp/dcs_liberation/wiki/Manual"))
        helpmenu.add_command(label="Troubleshooting Guide", command=lambda: webbrowser.open_new_tab("https://github.com/shdwp/dcs_liberation/wiki/Troubleshooting"))
        helpmenu.add_command(label="Modding Guide", command=lambda: webbrowser.open_new_tab("https://github.com/shdwp/dcs_liberation/wiki/Modding-tutorial"))
        helpmenu.add_separator()
        helpmenu.add_command(label="Contribute", command=lambda: webbrowser.open_new_tab("https://github.com/shdwp/dcs_liberation"))
        helpmenu.add_command(label="Forum Thread", command=lambda: webbrowser.open_new_tab("https://forums.eagle.ru/showthread.php?t=214834"))
        helpmenu.add_command(label="Report an issue", command=self.report_issue)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.tk.config(menu=menubar)
        self.tk.focus()


    def build(self):
        self.frame = Frame(self.tk, bg=BG_COLOR)
        self.frame.grid(column=0, row=0, sticky=NSEW)
        self.frame.grid_columnconfigure(0)
        self.frame.grid_columnconfigure(1)

        self.frame.grid_columnconfigure(0, weight=0)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)

        self.left_pane = Frame(self.frame, bg=BG_TITLE_COLOR)
        self.left_pane.grid(row=0, column=0, sticky=NSEW)
        self.right_pane = Frame(self.frame, bg=BG_COLOR)
        self.right_pane.grid(row=0, column=1, sticky=NSEW)

    def clear_right_pane(self):
        for i in range(100):
            self.right_pane.grid_columnconfigure(1, weight=0)
            self.right_pane.grid_rowconfigure(1, weight=0)

        for x in self.right_pane.winfo_children():
            x.grid_remove()

    def clear(self):
        def clear_recursive(x, n=50):
            if n < 0:
                return
            for y in x.winfo_children():
                clear_recursive(y, n-1)
            x.grid_forget()

        clear_recursive(self.frame, 50)
        self.left_pane.grid_remove()
        self.right_pane.grid_remove()
        self.build()

    def start_new_game(self, player_name: str, enemy_name: str, terrain: str, sams: bool, midgame: bool, multiplier: float, period:datetime):

        player_country = db.FACTIONS[player_name]["country"]
        enemy_country = db.FACTIONS[enemy_name]["country"]

        if terrain == "persiangulf":
            conflicttheater = persiangulf.PersianGulfTheater()
        elif terrain == "nevada":
            conflicttheater = nevada.NevadaTheater()
        else:
            conflicttheater = caucasus.CaucasusTheater()

        if midgame:
            for i in range(0, int(len(conflicttheater.controlpoints) / 2)):
                conflicttheater.controlpoints[i].captured = True

        start_generator.generate_inital_units(conflicttheater, enemy_name, sams, multiplier)
        game = Game(player_name=player_name,
                    enemy_name=enemy_name,
                    theater=conflicttheater,
                    start_date=period)
        start_generator.generate_groundobjects(conflicttheater, game)
        game.budget = int(game.budget * multiplier)
        game.settings.multiplier = multiplier
        game.settings.sams = sams
        game.settings.version = logging_module.version_string()

        if midgame:
            game.budget = game.budget * 4 * len(list(conflicttheater.conflicts()))

        self.proceed_to_main_menu(game)

    def proceed_to_main_menu(self, game: Game):
        from ui.mainmenu import MainMenu
        self.clear()
        m = MainMenu(self, None, game)
        m.display()

    def proceed_to_new_game_menu(self):
        from ui.newgamemenu import NewGameMenu
        self.clear()
        new_game_menu = NewGameMenu(self, self.start_new_game)
        new_game_menu.display()

    def new_game_confirm(self):
        result = messagebox.askquestion("Start a new game", "Are you sure you want to start a new game ? Your current campaign will be overriden and there is no going back !", icon='warning')
        if result == 'yes':
            self.proceed_to_new_game_menu()
        else:
            pass

    def report_issue(self):
        raise logging_module.ShowLogsException()

    def exit(self):
        self.tk.destroy()
        sys.exit(0)

    def run(self):
        self.tk.mainloop()


class Menu:
    parent = None  # type: Menu

    def __init__(self, window: Window, parent, game: Game):
        self.window = window
        self.parent = parent
        self.game = game

    def dismiss(self):
        self.parent.display()

    def display(self):
        pass
