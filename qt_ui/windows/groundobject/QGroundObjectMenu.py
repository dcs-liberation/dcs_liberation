import logging

from PySide2.QtGui import QTransform
from PySide2.QtWidgets import (
    QDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QSpinBox,
)
from dcs import Point

from game import Game
from game.config import REWARDS
from game.data.building_data import FORTIFICATION_BUILDINGS
from game.server import EventStream
from game.sim.gameupdateevents import GameUpdateEvents
from game.theater import ControlPoint, TheaterGroundObject
from game.theater.theatergroundobject import (
    BuildingGroundObject,
)
from game.utils import Heading
from qt_ui.uiconstants import EVENT_ICONS, ICONS
from qt_ui.widgets.QBudgetBox import QBudgetBox
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal
from qt_ui.windows.groundobject.QBuildingInfo import QBuildingInfo
from qt_ui.windows.groundobject.QGroundObjectBuyMenu import QGroundObjectBuyMenu


class QGroundObjectMenu(QDialog):
    def __init__(
        self,
        parent,
        ground_object: TheaterGroundObject,
        cp: ControlPoint,
        game: Game,
    ):
        super().__init__(parent)
        self.setMinimumWidth(350)
        self.ground_object = ground_object
        self.cp = cp
        self.game = game
        self.setWindowTitle(
            f"Location - {self.ground_object.obj_name} ({self.cp.name})"
        )
        self.setWindowIcon(EVENT_ICONS["capture"])
        self.intelBox = QGroupBox("Units :")
        self.buildingBox = QGroupBox("Buildings :")
        self.orientationBox = QGroupBox("Orientation :")
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
            self.mainLayout.addWidget(self.orientationBox)

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
            for unit in g.units:
                self.intelLayout.addWidget(
                    QLabel(f"<b>Unit {str(unit.display_name)}</b>"), i, 0
                )

                if not unit.alive and unit.repairable and self.cp.captured:
                    price = unit.unit_type.price if unit.unit_type else 0
                    repair = QPushButton(f"Repair [{price}M]")
                    repair.setProperty("style", "btn-success")
                    repair.clicked.connect(
                        lambda u=unit, p=price: self.repair_unit(u, p)
                    )
                    self.intelLayout.addWidget(repair, i, 1)
                i += 1

        stretch = QVBoxLayout()
        stretch.addStretch()
        self.intelLayout.addLayout(stretch, i, 0)

        self.buildingBox = QGroupBox("Buildings :")
        self.buildingsLayout = QGridLayout()

        j = 0
        total_income = 0
        received_income = 0
        for static in self.ground_object.statics:
            if static not in FORTIFICATION_BUILDINGS:
                self.buildingsLayout.addWidget(
                    QBuildingInfo(static, self.ground_object), j / 3, j % 3
                )
                j = j + 1

            if self.ground_object.category in REWARDS.keys():
                total_income += REWARDS[self.ground_object.category]
                if static.alive:
                    received_income += REWARDS[self.ground_object.category]
            else:
                logging.warning(self.ground_object.category + " not in REWARDS")

        self.financesBox = QGroupBox("Finances: ")
        self.financesBoxLayout = QGridLayout()
        self.financesBoxLayout.addWidget(
            QLabel("Available: " + str(total_income) + "M"), 2, 1
        )
        self.financesBoxLayout.addWidget(
            QLabel("Receiving: " + str(received_income) + "M"), 2, 2
        )

        # Orientation Box
        self.orientationBox = QGroupBox("Orientation :")
        self.orientationBoxLayout = QHBoxLayout()

        heading_image = QLabel()
        heading_image.setPixmap(
            ICONS["heading"].transformed(
                QTransform().rotate(self.ground_object.heading.degrees)
            )
        )
        self.orientationBoxLayout.addWidget(heading_image)
        self.headingLabel = QLabel("Heading:")
        self.orientationBoxLayout.addWidget(self.headingLabel)
        self.headingSelector = QSpinBox()
        self.headingSelector.setEnabled(False)  # Disable for now
        self.headingSelector.setMinimum(0)
        self.headingSelector.setMaximum(360)
        self.headingSelector.setValue(self.ground_object.heading.degrees)
        self.orientationBoxLayout.addWidget(self.headingSelector)
        if self.cp.captured:
            # TODO Let the user choose the heading with the SpinBox
            self.headingSelector.setEnabled(False)
            self.head_to_conflict_button = QPushButton("Head to conflict")
            heading = (
                self.game.theater.heading_to_conflict_from(self.ground_object.position)
                or self.ground_object.heading
            )
            self.head_to_conflict_button.clicked.connect(
                lambda: self.rotate_tgo(heading)
            )
            self.orientationBoxLayout.addWidget(self.head_to_conflict_button)
        else:
            self.headingSelector.setEnabled(False)

        # Set the layouts
        self.financesBox.setLayout(self.financesBoxLayout)
        self.buildingBox.setLayout(self.buildingsLayout)
        self.intelBox.setLayout(self.intelLayout)
        self.orientationBox.setLayout(self.orientationBoxLayout)

    def do_refresh_layout(self):
        try:
            for i in reversed(range(self.mainLayout.count())):
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
                self.mainLayout.addWidget(self.orientationBox)

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
        if not self.ground_object.purchasable:
            return
        self.total_value = self.ground_object.value
        if self.sell_all_button is not None:
            self.sell_all_button.setText("Disband (+$" + str(self.total_value) + "M)")

    def repair_unit(self, unit, price):
        if self.game.blue.budget > price:
            self.game.blue.budget -= price
            unit.alive = True
            GameUpdateSignal.get_instance().updateGame(self.game)

            # Remove destroyed units in the vicinity
            destroyed_units = self.game.get_destroyed_units()
            for d in destroyed_units:
                p = Point(d["x"], d["z"], self.game.theater.terrain)
                if p.distance_to_point(unit.position) < 15:
                    destroyed_units.remove(d)
                    logging.info("Removed destroyed units " + str(d))
            logging.info(f"Repaired unit: {unit.unit_name}")

        self.update_game()

    def rotate_tgo(self, heading: Heading) -> None:
        self.ground_object.rotate(heading)
        self.do_refresh_layout()

    def sell_all(self):
        self.update_total_value()
        self.game.blue.budget += self.total_value
        self.ground_object.groups = []
        self.update_game()

    def buy_group(self) -> None:
        self.subwindow = QGroundObjectBuyMenu(
            self, self.ground_object, self.game, self.total_value
        )
        if self.subwindow.exec_():
            self.update_game()

    def update_game(self) -> None:
        events = GameUpdateEvents()
        events.update_tgo(self.ground_object)
        self.game.theater.iads_network.update_tgo(self.ground_object, events)
        if any(
            package.target == self.ground_object
            for package in self.game.ato_for(player=False).packages
        ):
            # Replan if the tgo was a target of the redfor
            self.game.initialize_turn(events, for_red=True, for_blue=False)
        EventStream.put_nowait(events)
        GameUpdateSignal.get_instance().updateGame(self.game)
        # Refresh the dialog
        self.do_refresh_layout()
