import traceback

from PySide2.QtCore import Qt
from PySide2.QtGui import QCloseEvent
from PySide2.QtWidgets import QHBoxLayout, QLabel, QWidget, QDialog, QVBoxLayout, QGridLayout, QPushButton, \
    QGroupBox, QSizePolicy, QSpacerItem
from dcs.unittype import UnitType

from game.event import UnitsDeliveryEvent, ControlPointType
from qt_ui.widgets.QBudgetBox import QBudgetBox
from qt_ui.widgets.base.QAirportInformation import QAirportInformation
from qt_ui.widgets.base.QBaseInformation import QBaseInformation
from qt_ui.windows.basemenu.QBaseMenuTabs import QBaseMenuTabs
from qt_ui.windows.mission.QPlannedFlightsView import QPlannedFlightsView
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal
from theater import ControlPoint, CAP, Embarking, CAS, PinpointStrike, db
from game import Game


class QBaseMenu2(QDialog):

    def __init__(self, parent, cp: ControlPoint, game: Game):
        super(QBaseMenu2, self).__init__(parent)

        # Attrs
        self.cp = cp
        self.game = game
        self.is_carrier = self.cp.cptype in [ControlPointType.AIRCRAFT_CARRIER_GROUP, ControlPointType.LHA_GROUP]

        # Widgets
        self.qbase_menu_tab = QBaseMenuTabs(cp, game)

        try:
            self.airport = game.theater.terrain.airport_by_id(self.cp.id)
        except:
            self.airport = None

        if self.cp.captured:
            self.deliveryEvent = None

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setMinimumSize(300, 200)
        self.setModal(True)
        self.initUi()

    def initUi(self):
        self.setWindowTitle(self.cp.name)
        self.topLayoutWidget = QWidget()
        self.topLayout = QHBoxLayout()

        self.topLayoutWidget = QWidget()
        self.topLayout = QHBoxLayout()

        title = QLabel("<b>" + self.cp.name + "</b>")
        title.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        title.setProperty("style", "base-title")
        unitsPower = QLabel("{} / {} /  Runway : {}".format(self.cp.base.total_planes, self.cp.base.total_armor,
                                                            "Available" if self.cp.has_runway() else "Unavailable"))

        self.topLayout.addWidget(title)
        self.topLayout.addWidget(unitsPower)
        self.topLayout.setAlignment(Qt.AlignTop)
        self.topLayoutWidget.setProperty("style", "baseMenuHeader")
        self.topLayoutWidget.setLayout(self.topLayout)

        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.topLayoutWidget, 0, 0)
        self.mainLayout.addWidget(self.qbase_menu_tab, 1, 0)

        self.setLayout(self.mainLayout)

    def closeEvent(self, closeEvent:QCloseEvent):
        GameUpdateSignal.get_instance().updateGame(self.game)