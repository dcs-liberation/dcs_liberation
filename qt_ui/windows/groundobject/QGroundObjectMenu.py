import logging

from PySide2 import QtCore
from PySide2.QtGui import Qt
from PySide2.QtWidgets import QHBoxLayout, QDialog, QGridLayout, QLabel, QGroupBox, QVBoxLayout, QPushButton, \
    QComboBox, QSpinBox, QMessageBox
from dcs import Point

from game import Game, db
from game.data.building_data import FORTIFICATION_BUILDINGS
from game.db import PRICES, REWARDS, unit_type_of, PinpointStrike
from gen.defenses.armor_group_generator import generate_armor_group_of_type_and_size
from gen.sam.sam_group_generator import get_faction_possible_sams_generator
from qt_ui.uiconstants import EVENT_ICONS
from qt_ui.widgets.QBudgetBox import QBudgetBox
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal
from qt_ui.windows.groundobject.QBuildingInfo import QBuildingInfo
from theater import ControlPoint, TheaterGroundObject


class QGroundObjectMenu(QDialog):

    changed = QtCore.Signal()

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
        self.sell_all_button = None
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
            if self.cp.captured:
                self.mainLayout.addWidget(self.financesBox)

        self.actionLayout = QHBoxLayout()

        self.sell_all_button = QPushButton("Disband (+" + str(self.total_value) + "M)")
        self.sell_all_button.clicked.connect(self.sell_all)
        self.sell_all_button.setProperty("style", "btn-danger")

        self.buy_replace = QPushButton("Buy/Replace")
        self.buy_replace.clicked.connect(self.buy_group)
        self.buy_replace.setProperty("style", "btn-success")

        if self.total_value > 0:
            self.actionLayout.addWidget(self.sell_all_button)
        self.actionLayout.addWidget(self.buy_replace)

        if self.cp.captured and self.ground_object.dcs_identifier == "AA":
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
        stretch = QVBoxLayout()
        stretch.addStretch()
        self.intelLayout.addLayout(stretch, i, 0)

        self.buildingBox = QGroupBox("Buildings :")
        self.buildingsLayout = QGridLayout()
        j = 0

        total_income = 0
        received_income = 0
        for i, building in enumerate(self.buildings):
            if building.dcs_identifier not in FORTIFICATION_BUILDINGS:
                self.buildingsLayout.addWidget(QBuildingInfo(building, self.ground_object), j/3, j%3)
                j = j + 1

            if building.category in REWARDS.keys():
                total_income = total_income + REWARDS[building.category]
                if not building.is_dead:
                    received_income = received_income + REWARDS[building.category]


        self.financesBox = QGroupBox("Finances: ")
        self.financesBoxLayout = QGridLayout()

        str_total_income = 'Available: ' + str(total_income) + "M"
        str_percived_income = 'Receiving: ' + str(received_income) + "M"

        self.financesBoxLayout.addWidget(QLabel(str_total_income), 2, 1)
        self.financesBoxLayout.addWidget(QLabel(str_percived_income), 2, 2)

        self.financesBox.setLayout(self.financesBoxLayout)
        self.buildingBox.setLayout(self.buildingsLayout)
        self.intelBox.setLayout(self.intelLayout)

    def do_refresh_layout(self):
        try:
            for i in range(self.mainLayout.count()):
                item = self.mainLayout.itemAt(i)
                if item is not None and item.widget() is not None:
                    item.widget().setParent(None)
            self.sell_all_button.setParent(None)
            self.buy_replace.setParent(None)
            self.actionLayout.setParent(None)

            self.doLayout()
            if self.ground_object.dcs_identifier == "AA":
                self.mainLayout.addWidget(self.intelBox)
            else:
                self.mainLayout.addWidget(self.buildingBox)

            self.actionLayout = QHBoxLayout()
            if self.total_value > 0:
                self.actionLayout.addWidget(self.sell_all_button)
            self.actionLayout.addWidget(self.buy_replace)

            if self.cp.captured and self.ground_object.dcs_identifier == "AA":
                self.mainLayout.addLayout(self.actionLayout)

        except Exception as e:
            print(e)
        self.update_total_value()
        self.changed.emit()

    def update_total_value(self):
        total_value = 0
        for group in self.ground_object.groups:
            for u in group.units:
                utype = unit_type_of(u)
                if utype in PRICES:
                    total_value = total_value + PRICES[utype]
                else:
                    total_value = total_value + 1
        if self.sell_all_button is not None:
            self.sell_all_button.setText("Disband (+$" + str(self.total_value) + "M)")
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
        self.changed.emit()

    def sell_all(self):
        self.update_total_value()
        self.game.budget = self.game.budget + self.total_value
        self.ground_object.groups = []
        self.do_refresh_layout()
        GameUpdateSignal.get_instance().updateBudget(self.game)

    def buy_group(self):
        self.subwindow = QBuyGroupForGroundObjectDialog(self, self.ground_object, self.cp, self.game, self.total_value)
        self.subwindow.changed.connect(self.do_refresh_layout)
        self.subwindow.show()



class QBuyGroupForGroundObjectDialog(QDialog):

    changed = QtCore.Signal()

    def __init__(self, parent, ground_object: TheaterGroundObject, cp: ControlPoint, game: Game, current_group_value: int):
        super(QBuyGroupForGroundObjectDialog, self).__init__(parent)

        self.setMinimumWidth(350)
        self.ground_object = ground_object
        self.cp = cp
        self.game = game
        self.current_group_value = current_group_value

        self.setWindowTitle("Buy units @ " + self.ground_object.obj_name)
        self.setWindowIcon(EVENT_ICONS["capture"])

        self.buySamButton = QPushButton("Buy")
        self.buyArmorButton = QPushButton("Buy")
        self.buySamLayout = QGridLayout()
        self.buyArmorLayout = QGridLayout()
        self.amount = QSpinBox()
        self.buyArmorCombo = QComboBox()
        self.samCombo = QComboBox()
        self.buySamBox = QGroupBox("Buy SAM site :")
        self.buyArmorBox = QGroupBox("Buy defensive position :")



        self.init_ui()

    def init_ui(self):
        faction = self.game.player_name

        # Sams

        possible_sams = get_faction_possible_sams_generator(faction)
        for sam in possible_sams:
            self.samCombo.addItem(sam.name + " [$" + str(sam.price) + "M]", userData=sam)
        self.samCombo.currentIndexChanged.connect(self.samComboChanged)

        self.buySamLayout.addWidget(QLabel("Site Type :"), 0, 0, Qt.AlignLeft)
        self.buySamLayout.addWidget(self.samCombo, 0, 1, alignment=Qt.AlignRight)
        self.buySamLayout.addWidget(self.buySamButton, 1, 1, alignment=Qt.AlignRight)
        stretch = QVBoxLayout()
        stretch.addStretch()
        self.buySamLayout.addLayout(stretch, 2, 0)

        self.buySamButton.clicked.connect(self.buySam)

        # Armored units

        armored_units = db.find_unittype(PinpointStrike, faction) # Todo : refactor this legacy nonsense
        for unit in set(armored_units):
            self.buyArmorCombo.addItem(db.unit_type_name_2(unit) + " [$" + str(db.PRICES[unit]) + "M]", userData=unit)
        self.buyArmorCombo.currentIndexChanged.connect(self.armorComboChanged)

        self.amount.setMinimum(2)
        self.amount.setMaximum(8)
        self.amount.setValue(2)
        self.amount.valueChanged.connect(self.amountComboChanged)

        self.buyArmorLayout.addWidget(QLabel("Unit type :"), 0, 0, Qt.AlignLeft)
        self.buyArmorLayout.addWidget(self.buyArmorCombo, 0, 1, alignment=Qt.AlignRight)
        self.buyArmorLayout.addWidget(QLabel("Group size :"), 1, 0, alignment=Qt.AlignLeft)
        self.buyArmorLayout.addWidget(self.amount, 1, 1, alignment=Qt.AlignRight)
        self.buyArmorLayout.addWidget(self.buyArmorButton, 2, 1, alignment=Qt.AlignRight)
        stretch2 = QVBoxLayout()
        stretch2.addStretch()
        self.buyArmorLayout.addLayout(stretch2, 3, 0)

        self.buyArmorButton.clicked.connect(self.buyArmor)

        # Do layout
        self.buySamBox.setLayout(self.buySamLayout)
        self.buyArmorBox.setLayout(self.buyArmorLayout)

        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.buySamBox)

        if self.ground_object.airbase_group:
            self.mainLayout.addWidget(self.buyArmorBox)

        self.setLayout(self.mainLayout)

        try:
            self.samComboChanged(0)
            self.armorComboChanged(0)
        except:
            pass

    def samComboChanged(self, index):
        self.buySamButton.setText("Buy [$" + str(self.samCombo.itemData(index).price) + "M] [-$" + str(self.current_group_value) + "M]")

    def armorComboChanged(self, index):
        self.buyArmorButton.setText("Buy [$" + str(db.PRICES[self.buyArmorCombo.itemData(index)] * self.amount.value()) + "M][-$" + str(self.current_group_value) + "M]")

    def amountComboChanged(self):
        self.buyArmorButton.setText("Buy [$" + str(db.PRICES[self.buyArmorCombo.itemData(self.buyArmorCombo.currentIndex())] * self.amount.value()) + "M][-$" + str(self.current_group_value) + "M]")

    def buyArmor(self):
        print("Buy Armor ")
        utype = self.buyArmorCombo.itemData(self.buyArmorCombo.currentIndex())
        print(utype)
        price = db.PRICES[utype] * self.amount.value() - self.current_group_value
        if price > self.game.budget:
            self.error_money()
            self.close()
            return
        else:
            self.game.budget -= price

        # Generate Armor
        group = generate_armor_group_of_type_and_size(self.game, self.ground_object, utype, int(self.amount.value()))
        self.ground_object.groups = [group]

        GameUpdateSignal.get_instance().updateBudget(self.game)

        self.changed.emit()
        self.close()

    def buySam(self):
        sam_generator = self.samCombo.itemData(self.samCombo.currentIndex())
        price = sam_generator.price - self.current_group_value
        if price > self.game.budget:
            self.error_money()
            return
        else:
            self.game.budget -= price

        # Generate SAM
        generator = sam_generator(self.game, self.ground_object)
        generator.generate()
        generated_group = generator.get_generated_group()
        self.ground_object.groups = [generated_group]

        GameUpdateSignal.get_instance().updateBudget(self.game)

        self.changed.emit()
        self.close()

    def error_money(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Not enough money to buy these units !")
        msg.setWindowTitle("Not enough money")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setWindowFlags(Qt.WindowStaysOnTopHint)
        msg.exec_()
        self.close()