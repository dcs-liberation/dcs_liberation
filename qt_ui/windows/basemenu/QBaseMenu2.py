from PySide2.QtCore import Qt
from PySide2.QtGui import QCloseEvent, QPixmap
from PySide2.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from game.theater import ControlPoint, ControlPointType
from gen.flights.flight import FlightType
from qt_ui.dialogs import Dialog
from qt_ui.models import GameModel
from qt_ui.uiconstants import EVENT_ICONS
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal
from qt_ui.windows.basemenu.QBaseMenuTabs import QBaseMenuTabs
from qt_ui.windows.basemenu.QRecruitBehaviour import QRecruitBehaviour


class QBaseMenu2(QDialog):

    def __init__(self, parent, cp: ControlPoint, game_model: GameModel):
        super(QBaseMenu2, self).__init__(parent)

        # Attrs
        self.cp = cp
        self.game_model = game_model
        self.objectName = "menuDialogue"

        try:
            game = self.game_model.game
            self.airport = game.theater.terrain.airport_by_id(self.cp.id)
        except:
            self.airport = None

        if self.cp.captured:
            self.deliveryEvent = None

        self.setWindowIcon(EVENT_ICONS["capture"])

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setMinimumSize(300, 200)
        self.setMinimumWidth(800)
        self.setMaximumWidth(800)
        self.setModal(True)

        self.setWindowTitle(self.cp.name)

        base_menu_header = QWidget()
        top_layout = QHBoxLayout()

        header = QLabel(self)
        header.setGeometry(0, 0, 655, 106)
        pixmap = QPixmap(self.get_base_image())
        header.setPixmap(pixmap)

        title = QLabel("<b>" + self.cp.name + "</b>")
        title.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        title.setProperty("style", "base-title")
        aircraft = self.cp.base.total_aircraft
        armor = self.cp.base.total_armor
        runway_status = "operational" if self.cp.has_runway() else "damaged"
        intel_summary = QLabel("\n".join([
            f"{aircraft} aircraft",
            f"{armor} ground units",
            f"Runway {runway_status}"
        ]))
        top_layout.addWidget(title)
        top_layout.addWidget(intel_summary)
        top_layout.setAlignment(Qt.AlignTop)
        base_menu_header.setProperty("style", "baseMenuHeader")
        base_menu_header.setLayout(top_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(header)
        main_layout.addWidget(base_menu_header)
        main_layout.addWidget(QBaseMenuTabs(cp, self.game_model))
        bottom_row = QHBoxLayout()
        main_layout.addLayout(bottom_row)

        if FlightType.OCA_RUNWAY in self.cp.mission_types(for_player=True):
            runway_attack_button = QPushButton("Attack airfield")
            bottom_row.addWidget(runway_attack_button)

            runway_attack_button.setProperty("style", "btn-danger")
            runway_attack_button.clicked.connect(self.new_package)

        budget_display = QLabel(
            QRecruitBehaviour.BUDGET_FORMAT.format(self.game_model.game.budget)
        )
        budget_display.setObjectName("budgetField")
        budget_display.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        budget_display.setProperty("style", "budget-label")
        bottom_row.addWidget(budget_display)
        self.setLayout(main_layout)

    def closeEvent(self, closeEvent:QCloseEvent):
        GameUpdateSignal.get_instance().updateGame(self.game_model.game)

    def get_base_image(self):
        if self.cp.cptype == ControlPointType.AIRCRAFT_CARRIER_GROUP:
            return "./resources/ui/carrier.png"
        elif self.cp.cptype == ControlPointType.LHA_GROUP:
            return "./resources/ui/lha.png"
        else:
            return "./resources/ui/airbase.png"

    def new_package(self) -> None:
        Dialog.open_new_package_dialog(self.cp, parent=self.window())
