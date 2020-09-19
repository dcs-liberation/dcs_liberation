import logging

from PySide2.QtGui import QCloseEvent
from PySide2.QtWidgets import QHBoxLayout, QWidget, QDialog, QGridLayout, QLabel, QGroupBox, QVBoxLayout, QPushButton
from dcs import Point

from game import Game
from game.data.building_data import FORTIFICATION_BUILDINGS
from game.db import PRICES, unit_type_of
from qt_ui.uiconstants import EVENT_ICONS
from qt_ui.widgets.QBudgetBox import QBudgetBox
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal
from qt_ui.windows.groundobject.QBuildingInfo import QBuildingInfo
from theater import ControlPoint, TheaterGroundObject


class QGroundObjectMenu(QDialog):

    def __init__(self, parent, ground_object: TheaterGroundObject, buildings:[], cp: ControlPoint, game: Game):
        super(QGroundObjectMenu, self).__init__(parent)
        self.setMinimumWidth(350)
        self.ground_object = ground_object
        self.buildings = buildings
        self.cp = cp
        self.game = game
        self.setWindowTitle("Location " + self.ground_object.obj_name)
        self.setWindowIcon(EVENT_ICONS["capture"])
        self.intelBox = QGroupBox("Units :")
        self.buildingBox = QGroupBox("Buildings :")
        self.intelLayout = QGridLayout()
        self.buildingsLayout = QGridLayout()
        self.total_value = 0
        self.init_ui()

    def init_ui(self):

        self.mainLayout = QVBoxLayout()
        self.budget = QBudgetBox(self.game)
        self.budget.setGame(self.game)

        self.doLayout()

        if self.ground_object.dcs_identifier == "AA":
            self.mainLayout.addWidget(self.intelBox)
        else:
            self.mainLayout.addWidget(self.buildingBox)

        self.actionLayout = QHBoxLayout()
        sell_all_button = QPushButton("Disband (+" + str(self.total_value) + "M)")
        sell_all_button.clicked.connect(self.sell_all)
        self.actionLayout.addWidget(sell_all_button)

        if self.total_value > 0:
            self.mainLayout.addLayout(self.actionLayout)
        self.setLayout(self.mainLayout)

    def doLayout(self):

        self.update_total_value()
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
                if self.cp.captured:
                    repair = QPushButton("Repair [" + str(price) + "M]")
                    repair.setProperty("style", "btn-success")
                    repair.clicked.connect(lambda u=u, g=g, p=price: self.repair_unit(g, u, p))
                    self.intelLayout.addWidget(repair, i, 1)
                i = i + 1

        self.buildingBox = QGroupBox("Buildings :")
        self.buildingsLayout = QGridLayout()
        j = 0
        for i, building in enumerate(self.buildings):
            if building.dcs_identifier not in FORTIFICATION_BUILDINGS:
                self.buildingsLayout.addWidget(QBuildingInfo(building, self.ground_object), j/3, j%3)
                j = j + 1

        self.buildingBox.setLayout(self.buildingsLayout)
        self.intelBox.setLayout(self.intelLayout)

    def do_refresh_layout(self):
        try:
            for i in range(self.mainLayout.count()):
                self.mainLayout.removeItem(self.mainLayout.itemAt(i))
            self.doLayout()
            if len(self.ground_object.groups) > 0:
                self.mainLayout.addWidget(self.intelBox)
            else:
                self.mainLayout.addWidget(self.buildingBox)
        except Exception as e:
            print(e)
        self.update_total_value()

    def update_total_value(self):
        total_value = 0
        for group in self.ground_object.groups:
            for u in group.units:
                utype = unit_type_of(u)
                if utype in PRICES:
                    total_value = total_value + PRICES[utype]
                else:
                    total_value = total_value + 1
        self.total_value = total_value

    def repair_unit(self, group, unit, price):
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

    def sell_all(self):
        self.update_total_value()
        self.game.budget = self.game.budget + self.total_value
        self.ground_object.groups = []
        GameUpdateSignal.get_instance().updateGame(self.game)

    def buy_group(self):
        pass

    def closeEvent(self, closeEvent: QCloseEvent):
        pass
