import os

from PySide2.QtGui import QWindow
from PySide2.QtWidgets import QHBoxLayout, QLabel, QWidget, QDialog, QVBoxLayout, QGridLayout, QGroupBox, QCheckBox, \
    QSpinBox, QPushButton

from game.game import AWACS_BUDGET_COST, PinpointStrike, db, Event
from userdata.persistency import base_path
import qt_ui.uiconstants as CONST


class QBriefingWindow(QDialog):

    def __init__(self, parent, gameEvent: Event):
        super(QBriefingWindow, self).__init__(parent)
        self.gameEvent = gameEvent
        self.setWindowTitle("Briefing : " + str(gameEvent))
        self.setMinimumSize(200,200)
        self.setWindowIcon(CONST.EVENT_ICONS[self.gameEvent.__class__])
        self.setModal(True)
        self.base = self.gameEvent.from_cp.base
        self.scramble_entries = {k: {} for k in self.gameEvent.tasks}
        self.initUi()

    def initUi(self):

        self.layout = QVBoxLayout()

        self.scramble_box = QGroupBox("Units")
        self.gridLayout = QGridLayout()
        self.scramble_box.setLayout(self.gridLayout)
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

        # Options


        """
        header("Ready?")
        self.error_label = label("", columnspan=4)
        self.error_label["fg"] = RED
        Button(self.frame, text="Commit", command=self.start, **STYLES["btn-primary"]).grid(column=0, row=row,
                                                                                            sticky=E, padx=5,
                                                                                            pady=(10, 10))
        Button(self.frame, text="Back", command=self.dismiss, **STYLES["btn-warning"]).grid(column=3, row=row,
                                                                                            sticky=E, padx=5,
                                                                                            pady=(10, 10))"""

        self.action_layout = QHBoxLayout()
        self.commit_button = QPushButton("Commit")
        self.back_button = QPushButton("Commit")
        self.action_layout.addWidget(self.commit_button)
        self.action_layout.addWidget(self.back_button)

        self.support_box = self.initSupportBox()
        self.layout.addWidget(QLabel("<h2>{} on {}</h2>".format(self.gameEvent, self.gameEvent.to_cp.name)))
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