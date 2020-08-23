import logging

from PySide2.QtGui import QCloseEvent
from PySide2.QtWidgets import QHBoxLayout, QWidget, QDialog, QGridLayout, QLabel, QGroupBox, QVBoxLayout, QPushButton
from dcs import Point

from game import Game
from game.db import PRICES, unit_type_of
from qt_ui.widgets.QBudgetBox import QBudgetBox
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal
from theater import ControlPoint, TheaterGroundObject


class QGroundObjectMenu(QDialog):

    def __init__(self, parent, ground_object: TheaterGroundObject, cp: ControlPoint, game: Game):
        super(QGroundObjectMenu, self).__init__(parent)
        self.setMinimumWidth(350)
        self.ground_object = ground_object
        self.cp = cp
        self.game = game
        self.setWindowTitle("Location " + self.ground_object.obj_name)
        self.intelBox = QGroupBox("Units :")
        self.intelLayout = QGridLayout()
        self.init_ui()

    def init_ui(self):

        self.mainLayout = QVBoxLayout()
        self.budget = QBudgetBox(self.game)
        self.budget.setGame(self.game)

        self.doLayout()

        self.mainLayout.addWidget(self.intelBox)
        self.setLayout(self.mainLayout)

    def doLayout(self):
        self.intelBox = QGroupBox("Units :")
        self.intelLayout = QGridLayout()
        i = 0
        for g in self.ground_object.groups:
            if not hasattr(g, "units_losts"):
                g.units_losts = []
            for u in g.units:
                self.intelLayout.addWidget(QLabel("<b>Unit #" + str(u.id) + " - " + str(u.type) + "</b>"), i, 0)
                i = i + 1

            for u in g.units_losts:

                utype = unit_type_of(u)
                if utype in PRICES:
                    price = PRICES[utype]
                else:
                    price = 6

                self.intelLayout.addWidget(QLabel("<b>Unit #" + str(u.id) + " - " + str(u.type) + "</b> [DEAD]"), i, 0)
                repair = QPushButton("Repair [" + str(price) + "M]")
                repair.setProperty("style", "btn-primary")
                repair.clicked.connect(lambda u=u, g=g, p=price: self.repair_unit(g, u, p))
                self.intelLayout.addWidget(repair, i, 1)
                i = i + 1
        self.intelBox.setLayout(self.intelLayout)

    def do_refresh_layout(self):
        try:
            for i in range(self.mainLayout.count()):
                self.mainLayout.removeItem(self.mainLayout.itemAt(i));
            self.doLayout()
            self.mainLayout.addWidget(self.intelBox)
        except Exception as e:
            print(e)

    def repair_unit(self, group, unit, price):

        print(group)
        print(unit.type)
        [print(u.id) for u in group.units]

        if self.game.budget > price:
            self.game.budget -= price
            group.units_losts = [u for u in group.units_losts if u.id != unit.id]
            group.units.append(unit)
            GameUpdateSignal.get_instance().updateGame(self.game)

            # Remove destroyed units in the vicinity
            destroyed_units = self.game.get_destroyed_units()
            for d in destroyed_units:
                p = Point(d["x"], d["z"])
                if p.distance_to_point(unit.position) < 15:
                    destroyed_units.remove(d)
                    logging.info("Removed destroyed units " + str(d))
            logging.info("Repaired unit : " + str(unit.id) + " " + str(unit.type))

        self.do_refresh_layout()

    def closeEvent(self, closeEvent: QCloseEvent):
        GameUpdateSignal.get_instance().updateGame(self.game)
