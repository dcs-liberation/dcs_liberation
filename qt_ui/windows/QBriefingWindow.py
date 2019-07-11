import os

from PySide2.QtGui import QWindow
from PySide2.QtWidgets import QHBoxLayout, QLabel, QWidget, QDialog, QVBoxLayout, QGridLayout, QGroupBox, QCheckBox, \
    QSpinBox, QPushButton, QMessageBox, QComboBox
from pip._internal.utils import typing

from game.game import AWACS_BUDGET_COST, PinpointStrike, db, Event, FrontlineAttackEvent, FrontlinePatrolEvent, Task, \
    UnitType
from qt_ui.windows.QWaitingForMissionResultWindow import QWaitingForMissionResultWindow
from userdata.persistency import base_path
import qt_ui.uiconstants as CONST


class QBriefingWindow(QDialog):

    def __init__(self, gameEvent: Event):
        super(QBriefingWindow, self).__init__()
        self.gameEvent = gameEvent
        self.setWindowTitle("Briefing : " + str(gameEvent))
        self.setMinimumSize(200,200)
        self.setWindowIcon(CONST.EVENT_ICONS[self.gameEvent.__class__])
        self.setModal(True)
        self.base = self.gameEvent.from_cp.base
        self.game = self.gameEvent.game
        self.scramble_entries = {k: {} for k in self.gameEvent.tasks}
        self.initUi()

    def initUi(self):

        self.layout = QVBoxLayout()

        self.scramble_box = QGroupBox("Units")
        self.gridLayout = QGridLayout()
        self.scramble_box.setLayout(self.gridLayout)

        self.depart_box = QGroupBox("Departure")
        self.depart_layout = QHBoxLayout()
        self.depart_box.setLayout(self.depart_layout)
        self.depart_from_label = QLabel("Depart from : ")
        self.depart_from = QComboBox()

        for cp in [b for b in self.game.theater.controlpoints if b.captured]:
            self.depart_from.addItem(str(cp.name), cp)

        self.depart_layout.addWidget(self.depart_from_label)
        self.depart_layout.addWidget(self.depart_from)

        row = 0

        def header(text, row):
            self.gridLayout.addWidget(QLabel("<b>" + text + "</b>"), row, 0, 1, 2)

        def scramble_row(task_type, unit_type, unit_count, client_slots: bool, row: int):
            unit_name = QLabel("{} ({})".format(db.unit_type_name(unit_type), unit_count))
            self.gridLayout.addWidget(unit_name, row, 0)

            scramble_entry = QSpinBox()
            self.gridLayout.addWidget(scramble_entry, row, 1)

            if client_slots:
                client_entry = QSpinBox()
                self.gridLayout.addWidget(client_entry, row, 2)
            else:
                client_entry = None

            self.scramble_entries[task_type][unit_type] = scramble_entry, client_entry

        # Mission Description

        # Table headers
        self.gridLayout.addWidget(QLabel("Amount"), row, 1)
        self.gridLayout.addWidget(QLabel("Client slots"), row, 2)
        row += 1

        for flight_task in self.gameEvent.tasks:
            header("{}:".format(self.gameEvent.flight_name(flight_task)), row)
            row += 1

            if flight_task == PinpointStrike:
                if not self.base.armor:
                    self.gridLayout.addWidget(QLabel("No units"), row, 1)
                    row += 1
                for t, c in self.base.armor.items():
                    scramble_row(flight_task, t, c, False, row)
                    row += 1
            else:
                if not self.base.aircraft:
                    self.gridLayout.addWidget(QLabel("No units"), row, 1)
                    row += 1
                for t, c in self.base.aircraft.items():
                    scramble_row(flight_task, t, c, True, row)
                    row += 1

        self.action_layout = QHBoxLayout()
        self.commit_button = QPushButton("Commit")
        self.back_button = QPushButton("Cancel")
        self.commit_button.clicked.connect(self.start)
        self.back_button.clicked.connect(self.close)
        self.action_layout.addWidget(self.commit_button)
        self.action_layout.addWidget(self.back_button)

        self.support_box = self.initSupportBox()
        self.layout.addWidget(QLabel("<h2>{} on {}</h2>".format(self.gameEvent, self.gameEvent.to_cp.name)))
        self.layout.addWidget(self.depart_box)
        self.layout.addWidget(self.scramble_box)
        self.layout.addWidget(self.support_box)
        self.layout.addWidget(QLabel("<b>Ready?</b>"))
        self.layout.addLayout(self.action_layout)
        self.setLayout(self.layout)


    def initSupportBox(self):

        self.support_box = QGroupBox("Support")
        self.support_layout = QGridLayout()
        self.support_box.setLayout(self.support_layout)

        self.awacs_label = QLabel("AWACS ({}m)".format(AWACS_BUDGET_COST))
        self.awacs_checkbox = QCheckBox()

        self.ca_slot_label = QLabel("Combined Arms Slots")
        self.ca_slot_entry = QSpinBox()
        self.ca_slot_entry.setValue(0)
        self.ca_slot_entry.setMinimum(0)
        self.ca_slot_entry.setMaximum(32)

        self.support_layout.addWidget(self.awacs_label, 0, 0)
        self.support_layout.addWidget(self.awacs_checkbox, 0, 1)
        self.support_layout.addWidget(self.ca_slot_label, 1, 0)
        self.support_layout.addWidget(self.ca_slot_entry, 1, 1)
        return self.support_box


    def initWaitingForResults(self):

        layout = QVBoxLayout()

        layout.addWidget(QLabel("<b>You are clear for takeoff</b>"))
        layout.addWidget(QLabel("In DCS open and play the mission : "))
        layout.addWidget(QLabel("<i>liberation_nextturn</i>"))
        layout.addWidget(QLabel("or"))
        layout.addWidget(QLabel("<i>liberation_nextturn_quick</i>"))

        layout.addWidget(QLabel("<b>Then save the debriefing to folder :</b>"))
        layout.addWidget(QLabel("Then save the debriefing to the folder:"))
        layout.addWidget(QLabel("<i>" + self.debriefing_directory_location() + "</i>"))
        layout.addWidget(QLabel("Waiting for results..."))

        # layout.addWidget(QLabel("In DCS open and play the mission : "))
        # layout.addWidget(QLabel("<b>You are clear for takeoff</b>"))

        self.setLayout(layout)

        pass

    def debriefing_directory_location(self) -> str:
        return os.path.join(base_path(), "liberation_debriefings")

    def start(self):

        if self.awacs_checkbox.isChecked() == 1:
            self.gameEvent.is_awacs_enabled = True
            self.game.awacs_expense_commit()
        else:
            self.gameEvent.is_awacs_enabled = False

        ca_slot_entry_value = self.ca_slot_entry.value()
        try:
            ca_slots = int(ca_slot_entry_value and ca_slot_entry_value or "0")
        except:
            ca_slots = 0
        self.gameEvent.ca_slots = ca_slots


        # Resolve Departure CP
        self.gameEvent.departure_cp = self.depart_from.itemData(self.depart_from.currentIndex())


        flights = {k: {} for k in self.gameEvent.tasks}  # type: db.TaskForceDict
        units_scramble_counts = {}  # type: typing.Dict[typing.Type[UnitType], int]
        tasks_scramble_counts = {}  # type: typing.Dict[typing.Type[Task], int]
        tasks_clients_counts = {}  # type: typing.Dict[typing.Type[Task], int]

        def dampen_count(unit_type, count: int) -> int:
            nonlocal units_scramble_counts
            total_count = self.base.total_units_of_type(unit_type)

            total_scrambled = units_scramble_counts.get(unit_type, 0)
            dampened_value = count if count + total_scrambled < total_count else total_count - total_scrambled
            units_scramble_counts[unit_type] = units_scramble_counts.get(unit_type, 0) + dampened_value

            return dampened_value

        for task_type, dict in self.scramble_entries.items():
            for unit_type, (count_entry, clients_entry) in dict.items():
                try:
                    count = int(count_entry.value())
                except:
                    count = 0

                try:
                    clients_count = int(clients_entry and clients_entry.value() or 0)
                except:
                    clients_count = 0

                dampened_count = dampen_count(unit_type, count)
                tasks_clients_counts[task_type] = tasks_clients_counts.get(task_type, 0) + clients_count
                tasks_scramble_counts[task_type] = tasks_scramble_counts.get(task_type, 0) + dampened_count

                flights[task_type][unit_type] = dampened_count, clients_count

        for task in self.gameEvent.ai_banned_tasks:
            if tasks_clients_counts.get(task, 0) == 0 and tasks_scramble_counts.get(task, 0) > 0:
                self.showErrorMessage("Need at least one player in flight {}".format(self.gameEvent.flight_name(task)))
                return

        for task in self.gameEvent.player_banned_tasks:
            if tasks_clients_counts.get(task, 0) != 0:
                self.showErrorMessage("Players are not allowed on flight {}".format(self.gameEvent.flight_name(task)))
                return

        if self.game.is_player_attack(self.gameEvent):
            if isinstance(self.gameEvent, FrontlineAttackEvent) or isinstance(self.gameEvent, FrontlinePatrolEvent):
                if self.gameEvent.from_cp.base.total_armor == 0:
                    self.showErrorMessage("No ground vehicles available to attack!")
                    return

            self.gameEvent.player_attacking(flights)
        else:
            if isinstance(self.gameEvent, FrontlineAttackEvent) or isinstance(self.gameEvent, FrontlinePatrolEvent):
                if self.gameEvent.to_cp.base.total_armor == 0:
                    self.showErrorMessage("No ground vehicles available to defend!")
                    return

            self.gameEvent.player_defending(flights)

        self.game.initiate_event(self.gameEvent)

        waiting = QWaitingForMissionResultWindow(self.gameEvent, self.game)
        waiting.show()

        self.close()

    def showErrorMessage(self, text):
        about = QMessageBox()
        about.setWindowTitle("Error")
        about.setIcon(QMessageBox.Icon.Critical)
        about.setText(text)
        about.exec_()