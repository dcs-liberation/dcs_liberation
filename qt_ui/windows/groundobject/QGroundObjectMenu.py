import logging
from typing import List, Optional

from PySide2.QtGui import Qt
from PySide2.QtWidgets import (
    QComboBox,
    QDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
)
from dcs import Point
from dcs import vehicles

from game import Game
from game.data.building_data import FORTIFICATION_BUILDINGS
from game.db import REWARDS
from game.dcs.groundunittype import GroundUnitType
from game.theater import ControlPoint, TheaterGroundObject
from game.theater.theatergroundobject import (
    VehicleGroupGroundObject,
    SamGroundObject,
    EwrGroundObject,
    BuildingGroundObject,
)
from gen.defenses.armor_group_generator import generate_armor_group_of_type_and_size
from gen.sam.ewr_group_generator import get_faction_possible_ewrs_generator
from gen.sam.sam_group_generator import get_faction_possible_sams_generator
from qt_ui.uiconstants import EVENT_ICONS
from qt_ui.widgets.QBudgetBox import QBudgetBox
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal
from qt_ui.windows.groundobject.QBuildingInfo import QBuildingInfo


class QGroundObjectMenu(QDialog):
    def __init__(
        self,
        parent,
        ground_object: TheaterGroundObject,
        buildings: Optional[List[TheaterGroundObject]],
        cp: ControlPoint,
        game: Game,
    ):
        super().__init__(parent)
        self.setMinimumWidth(350)
        self.ground_object = ground_object
        if buildings is None:
            self.buildings = []
        else:
            self.buildings = buildings
        self.cp = cp
        self.game = game
        self.setWindowTitle(
            f"Location - {self.ground_object.obj_name} ({self.cp.name})"
        )
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

        if isinstance(self.ground_object, BuildingGroundObject):
            self.mainLayout.addWidget(self.buildingBox)
            if self.cp.captured:
                self.mainLayout.addWidget(self.financesBox)
        else:
            self.mainLayout.addWidget(self.intelBox)

        self.actionLayout = QHBoxLayout()

        self.sell_all_button = QPushButton("Disband (+" + str(self.total_value) + "M)")
        self.sell_all_button.clicked.connect(self.sell_all)
        self.sell_all_button.setProperty("style", "btn-danger")

        self.buy_replace = QPushButton("Buy/Replace")
        self.buy_replace.clicked.connect(self.buy_group)
        self.buy_replace.setProperty("style", "btn-success")

        if self.ground_object.purchasable:
            if self.total_value > 0:
                self.actionLayout.addWidget(self.sell_all_button)
            self.actionLayout.addWidget(self.buy_replace)

        if self.cp.captured and self.ground_object.purchasable:
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
            for unit in g.units:
                unit_display_name = unit.type
                dcs_unit_type = vehicles.vehicle_map.get(unit.type)
                if dcs_unit_type is not None:
                    # Hack: Don't know which variant is used.
                    try:
                        unit_display_name = next(
                            GroundUnitType.for_dcs_type(dcs_unit_type)
                        ).name
                    except StopIteration:
                        pass
                self.intelLayout.addWidget(
                    QLabel(
                        "<b>Unit #"
                        + str(unit.id)
                        + " - "
                        + str(unit_display_name)
                        + "</b>"
                    ),
                    i,
                    0,
                )
                i = i + 1

            for unit in g.units_losts:
                dcs_unit_type = vehicles.vehicle_map.get(unit.type)
                if dcs_unit_type is None:
                    continue

                # Hack: Don't know which variant is used.

                try:
                    unit_type = next(GroundUnitType.for_dcs_type(dcs_unit_type))
                    name = unit_type.name
                    price = unit_type.price
                except StopIteration:
                    name = dcs_unit_type.name
                    price = 0

                self.intelLayout.addWidget(
                    QLabel(f"<b>Unit #{unit.id} - {name}</b> [DEAD]"), i, 0
                )
                if self.cp.captured:
                    repair = QPushButton(f"Repair [{price}M]")
                    repair.setProperty("style", "btn-success")
                    repair.clicked.connect(
                        lambda u=unit, g=g, p=unit_type.price: self.repair_unit(g, u, p)
                    )
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
                self.buildingsLayout.addWidget(
                    QBuildingInfo(building, self.ground_object), j / 3, j % 3
                )
                j = j + 1

            if building.category in REWARDS.keys():
                total_income = total_income + REWARDS[building.category]
                if not building.is_dead:
                    received_income = received_income + REWARDS[building.category]
            else:
                logging.warning(building.category + " not in REWARDS")

        self.financesBox = QGroupBox("Finances: ")
        self.financesBoxLayout = QGridLayout()
        self.financesBoxLayout.addWidget(
            QLabel("Available: " + str(total_income) + "M"), 2, 1
        )
        self.financesBoxLayout.addWidget(
            QLabel("Receiving: " + str(received_income) + "M"), 2, 2
        )

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
            if isinstance(self.ground_object, BuildingGroundObject):
                self.mainLayout.addWidget(self.buildingBox)
            else:
                self.mainLayout.addWidget(self.intelBox)

            self.actionLayout = QHBoxLayout()
            if self.total_value > 0:
                self.actionLayout.addWidget(self.sell_all_button)
            self.actionLayout.addWidget(self.buy_replace)

            if self.cp.captured and self.ground_object.purchasable:
                self.mainLayout.addLayout(self.actionLayout)
        except Exception as e:
            logging.exception(e)
        self.update_total_value()

    def update_total_value(self):
        total_value = 0
        if not self.ground_object.purchasable:
            return
        for u in self.ground_object.units:
            # Hack: Unknown variant.
            unit_type = next(GroundUnitType.for_dcs_type(vehicles.vehicle_map[u.type]))
            total_value += unit_type.price
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

    def sell_all(self):
        self.update_total_value()
        self.game.budget = self.game.budget + self.total_value
        self.ground_object.groups = []

        # Replan if the tgo was a target of the redfor
        if any(
            package.target == self.ground_object
            for package in self.game.ato_for(player=False).packages
        ):
            self.game.initialize_turn(for_red=True, for_blue=False)

        self.do_refresh_layout()
        GameUpdateSignal.get_instance().updateGame(self.game)

    def buy_group(self):
        self.subwindow = QBuyGroupForGroundObjectDialog(
            self, self.ground_object, self.cp, self.game, self.total_value
        )
        self.subwindow.show()


class QBuyGroupForGroundObjectDialog(QDialog):
    def __init__(
        self,
        parent,
        ground_object: TheaterGroundObject,
        cp: ControlPoint,
        game: Game,
        current_group_value: int,
    ):
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

        faction = self.game.blue.faction

        # Sams

        possible_sams = get_faction_possible_sams_generator(faction)
        for sam in possible_sams:
            # Pre Generate SAM to get the real price
            generator = sam(self.game, self.ground_object)
            generator.generate()
            self.samCombo.addItem(
                generator.name + " [$" + str(generator.price) + "M]", userData=generator
            )
        self.samCombo.currentIndexChanged.connect(self.samComboChanged)

        self.buySamLayout.addWidget(QLabel("Site Type :"), 0, 0, Qt.AlignLeft)
        self.buySamLayout.addWidget(self.samCombo, 0, 1, alignment=Qt.AlignRight)
        self.buySamLayout.addWidget(self.buySamButton, 1, 1, alignment=Qt.AlignRight)
        stretch = QVBoxLayout()
        stretch.addStretch()
        self.buySamLayout.addLayout(stretch, 2, 0)

        self.buySamButton.clicked.connect(self.buySam)

        # EWRs

        buy_ewr_box = QGroupBox("Buy EWR:")
        buy_ewr_layout = QGridLayout()
        buy_ewr_box.setLayout(buy_ewr_layout)

        buy_ewr_layout.addWidget(QLabel("Radar type:"), 0, 0, Qt.AlignLeft)

        self.ewr_selector = QComboBox()
        buy_ewr_layout.addWidget(self.ewr_selector, 0, 1, alignment=Qt.AlignRight)
        ewr_types = get_faction_possible_ewrs_generator(faction)
        for ewr_type in ewr_types:
            # Pre Generate to get the real price
            generator = ewr_type(self.game, self.ground_object)
            generator.generate()
            self.ewr_selector.addItem(
                generator.name() + " [$" + str(generator.price) + "M]",
                userData=generator,
            )
        self.ewr_selector.currentIndexChanged.connect(self.on_ewr_selection_changed)

        self.buy_ewr_button = QPushButton("Buy")
        self.buy_ewr_button.clicked.connect(self.buy_ewr)
        buy_ewr_layout.addWidget(self.buy_ewr_button, 1, 1, alignment=Qt.AlignRight)
        stretch = QVBoxLayout()
        stretch.addStretch()
        buy_ewr_layout.addLayout(stretch, 2, 0)

        # Armored units
        for unit in set(faction.ground_units):
            self.buyArmorCombo.addItem(f"{unit} [${unit.price}M]", userData=unit)
        self.buyArmorCombo.currentIndexChanged.connect(self.armorComboChanged)

        self.amount.setMinimum(2)
        self.amount.setMaximum(8)
        self.amount.setValue(2)
        self.amount.valueChanged.connect(self.amountComboChanged)

        self.buyArmorLayout.addWidget(QLabel("Unit type :"), 0, 0, Qt.AlignLeft)
        self.buyArmorLayout.addWidget(self.buyArmorCombo, 0, 1, alignment=Qt.AlignRight)
        self.buyArmorLayout.addWidget(
            QLabel("Group size :"), 1, 0, alignment=Qt.AlignLeft
        )
        self.buyArmorLayout.addWidget(self.amount, 1, 1, alignment=Qt.AlignRight)
        self.buyArmorLayout.addWidget(
            self.buyArmorButton, 2, 1, alignment=Qt.AlignRight
        )
        stretch2 = QVBoxLayout()
        stretch2.addStretch()
        self.buyArmorLayout.addLayout(stretch2, 3, 0)

        self.buyArmorButton.clicked.connect(self.buyArmor)

        # Do layout
        self.buySamBox.setLayout(self.buySamLayout)
        self.buyArmorBox.setLayout(self.buyArmorLayout)

        self.mainLayout = QHBoxLayout()

        if isinstance(self.ground_object, SamGroundObject):
            self.mainLayout.addWidget(self.buySamBox)
        elif isinstance(self.ground_object, VehicleGroupGroundObject):
            self.mainLayout.addWidget(self.buyArmorBox)
        elif isinstance(self.ground_object, EwrGroundObject):
            self.mainLayout.addWidget(buy_ewr_box)

        self.setLayout(self.mainLayout)

        try:
            self.samComboChanged(0)
            self.armorComboChanged(0)
            self.on_ewr_selection_changed(0)
        except:
            pass

    def samComboChanged(self, index):
        self.buySamButton.setText(
            "Buy [$"
            + str(self.samCombo.itemData(index).price)
            + "M] [-$"
            + str(self.current_group_value)
            + "M]"
        )

    def on_ewr_selection_changed(self, index):
        ewr = self.ewr_selector.itemData(index)
        self.buy_ewr_button.setText(
            f"Buy [${ewr.price}M][-${self.current_group_value}M]"
        )

    def armorComboChanged(self, index):
        unit_type = self.buyArmorCombo.itemData(self.buyArmorCombo.currentIndex())
        price = unit_type.price * self.amount.value()
        self.buyArmorButton.setText(f"Buy [${price}M][-${self.current_group_value}M]")

    def amountComboChanged(self):
        unit_type = self.buyArmorCombo.itemData(self.buyArmorCombo.currentIndex())
        price = unit_type.price * self.amount.value()
        self.buyArmorButton.setText(f"Buy [${price}M][-${self.current_group_value}M]")

    def buyArmor(self):
        logging.info("Buying Armor ")
        utype = self.buyArmorCombo.itemData(self.buyArmorCombo.currentIndex())
        price = utype.price * self.amount.value() - self.current_group_value
        if price > self.game.budget:
            self.error_money()
            self.close()
            return
        else:
            self.game.budget -= price

        # Generate Armor
        group = generate_armor_group_of_type_and_size(
            self.game, self.ground_object, utype, int(self.amount.value())
        )
        self.ground_object.groups = [group]

        # Replan redfor missions
        self.game.initialize_turn(for_red=True, for_blue=False)

        GameUpdateSignal.get_instance().updateGame(self.game)

    def buySam(self):
        sam_generator = self.samCombo.itemData(self.samCombo.currentIndex())
        price = sam_generator.price - self.current_group_value
        if price > self.game.budget:
            self.error_money()
            return
        else:
            self.game.budget -= price

        self.ground_object.groups = list(sam_generator.groups)

        # Replan redfor missions
        self.game.initialize_turn(for_red=True, for_blue=False)

        GameUpdateSignal.get_instance().updateGame(self.game)

    def buy_ewr(self):
        ewr_generator = self.ewr_selector.itemData(self.ewr_selector.currentIndex())
        price = ewr_generator.price - self.current_group_value
        if price > self.game.budget:
            self.error_money()
            return
        else:
            self.game.budget -= price

        self.ground_object.groups = [ewr_generator.vg]

        # Replan redfor missions
        self.game.initialize_turn(for_red=True, for_blue=False)

        GameUpdateSignal.get_instance().updateGame(self.game)

    def error_money(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Not enough money to buy these units !")
        msg.setWindowTitle("Not enough money")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setWindowFlags(Qt.WindowStaysOnTopHint)
        msg.exec_()
        self.close()
