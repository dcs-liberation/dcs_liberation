from PySide2.QtCore import Qt
from PySide2.QtGui import QCloseEvent, QPixmap
from PySide2.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from game import Game, db
from game.theater import ControlPoint, ControlPointType
from gen.flights.flight import FlightType
from qt_ui.dialogs import Dialog
from qt_ui.models import GameModel
from qt_ui.uiconstants import EVENT_ICONS
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal
from qt_ui.windows.basemenu.NewUnitTransferDialog import NewUnitTransferDialog
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
        self.intel_summary = QLabel()
        self.update_intel_summary()
        top_layout.addWidget(title)
        top_layout.addWidget(self.intel_summary)
        top_layout.setAlignment(Qt.AlignTop)

        self.repair_button = QPushButton()
        self.repair_button.clicked.connect(self.begin_runway_repair)
        self.update_repair_button()
        top_layout.addWidget(self.repair_button)

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

        if self.cp.captured and self.has_transfer_destinations:
            transfer_button = QPushButton("Transfer Units")
            transfer_button.setProperty("style", "btn-success")
            bottom_row.addWidget(transfer_button)
            transfer_button.clicked.connect(self.open_transfer_dialog)

        self.budget_display = QLabel(
            QRecruitBehaviour.BUDGET_FORMAT.format(self.game_model.game.budget)
        )
        self.budget_display.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.budget_display.setProperty("style", "budget-label")
        bottom_row.addWidget(self.budget_display)
        GameUpdateSignal.get_instance().budgetupdated.connect(self.update_budget)
        self.setLayout(main_layout)

    @property
    def has_transfer_destinations(self) -> bool:
        return self.game_model.game.transit_network_for(
            self.cp.captured
        ).has_destinations(self.cp)

    @property
    def can_repair_runway(self) -> bool:
        return self.cp.captured and self.cp.runway_can_be_repaired

    @property
    def can_afford_runway_repair(self) -> bool:
        return self.game_model.game.budget >= db.RUNWAY_REPAIR_COST

    def begin_runway_repair(self) -> None:
        if not self.can_afford_runway_repair:
            QMessageBox.critical(
                self,
                "Cannot repair runway",
                f"Runway repair costs ${db.RUNWAY_REPAIR_COST}M but you have "
                f"only ${self.game_model.game.budget}M available.",
                QMessageBox.Ok,
            )
            return
        if not self.can_repair_runway:
            QMessageBox.critical(
                self,
                "Cannot repair runway",
                f"Cannot repair this runway.",
                QMessageBox.Ok,
            )
            return

        self.cp.begin_runway_repair()
        self.game_model.game.budget -= db.RUNWAY_REPAIR_COST
        self.update_repair_button()
        self.update_intel_summary()
        GameUpdateSignal.get_instance().updateGame(self.game_model.game)

    def update_repair_button(self) -> None:
        self.repair_button.setVisible(True)
        turns_remaining = self.cp.runway_status.repair_turns_remaining
        if self.cp.captured and turns_remaining is not None:
            self.repair_button.setText("Repairing...")
            self.repair_button.setDisabled(True)
            return

        if self.can_repair_runway:
            if self.can_afford_runway_repair:
                self.repair_button.setText(f"Repair ${db.RUNWAY_REPAIR_COST}M")
                self.repair_button.setDisabled(False)
                return
            else:
                self.repair_button.setText(
                    f"Cannot afford repair ${db.RUNWAY_REPAIR_COST}M"
                )
                self.repair_button.setDisabled(True)
                return

        self.repair_button.setVisible(False)
        self.repair_button.setDisabled(True)

    def update_intel_summary(self) -> None:
        aircraft = self.cp.base.total_aircraft
        parking = self.cp.total_aircraft_parking
        self.intel_summary.setText(
            "\n".join(
                [
                    f"{aircraft}/{parking} aircraft",
                    f"{self.cp.base.total_armor} ground units",
                    str(self.cp.runway_status),
                ]
            )
        )

    def closeEvent(self, close_event: QCloseEvent):
        GameUpdateSignal.get_instance().updateGame(self.game_model.game)

    def get_base_image(self):
        if self.cp.cptype == ControlPointType.AIRCRAFT_CARRIER_GROUP:
            return "./resources/ui/carrier.png"
        elif self.cp.cptype == ControlPointType.LHA_GROUP:
            return "./resources/ui/lha.png"
        elif self.cp.cptype == ControlPointType.FOB:
            return "./resources/ui/fob.png"
        else:
            return "./resources/ui/airbase.png"

    def new_package(self) -> None:
        Dialog.open_new_package_dialog(self.cp, parent=self.window())

    def open_transfer_dialog(self) -> None:
        NewUnitTransferDialog(self.game_model, self.cp, parent=self.window()).show()

    def update_budget(self, game: Game) -> None:
        self.budget_display.setText(QRecruitBehaviour.BUDGET_FORMAT.format(game.budget))
