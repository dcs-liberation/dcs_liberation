from __future__ import annotations

import json
import os
from typing import Sized

from PySide2 import QtCore
from PySide2.QtCore import QObject, Qt, Signal
from PySide2.QtGui import QIcon, QMovie, QPixmap
from PySide2.QtWidgets import (
    QDialog,
    QFileDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTextBrowser,
)
from jinja2 import Environment, FileSystemLoader, select_autoescape

from game.debriefing import Debriefing, wait_for_debriefing
from game.game import Event, Game, logging
from game.persistency import base_path
from game.profiling import logged_duration
from game.unitmap import UnitMap
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal


class DebriefingFileWrittenSignal(QObject):

    instance = None
    debriefingReceived = Signal(Debriefing)

    def __init__(self):
        super(DebriefingFileWrittenSignal, self).__init__()
        DebriefingFileWrittenSignal.instance = self

    def sendDebriefing(self, debriefing: Debriefing):
        self.debriefingReceived.emit(debriefing)

    @staticmethod
    def get_instance() -> DebriefingFileWrittenSignal:
        return DebriefingFileWrittenSignal.instance


DebriefingFileWrittenSignal()


class QWaitingForMissionResultWindow(QDialog):
    def __init__(self, gameEvent: Event, game: Game, unit_map: UnitMap) -> None:
        super(QWaitingForMissionResultWindow, self).__init__()
        self.setModal(True)
        self.gameEvent = gameEvent
        self.game = game
        self.unit_map = unit_map
        self.setWindowTitle("Waiting for mission completion.")
        self.setWindowIcon(QIcon("./resources/icon.png"))
        self.setMinimumHeight(570)

        self.initUi()
        DebriefingFileWrittenSignal.get_instance().debriefingReceived.connect(
            self.updateLayout
        )
        self.wait_thread = wait_for_debriefing(
            lambda debriefing: self.on_debriefing_update(debriefing),
            self.game,
            self.unit_map,
        )

    def initUi(self):
        self.layout = QGridLayout()

        header = QLabel(self)
        header.setGeometry(0, 0, 655, 106)
        pixmap = QPixmap("./resources/ui/conflict.png")
        header.setPixmap(pixmap)
        self.layout.addWidget(header, 0, 0)

        self.gridLayout = QGridLayout()

        jinja = Environment(
            loader=FileSystemLoader("resources/ui/templates"),
            autoescape=select_autoescape(
                disabled_extensions=("",),
                default_for_string=True,
                default=True,
            ),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self.instructions_text = QTextBrowser()
        self.instructions_text.setHtml(
            jinja.get_template("mission_start_EN.j2").render()
        )
        self.instructions_text.setOpenExternalLinks(True)
        self.gridLayout.addWidget(self.instructions_text, 1, 0)

        progress = QLabel("")
        progress.setAlignment(QtCore.Qt.AlignCenter)
        progress_bar = QMovie("./resources/ui/loader.gif")
        progress.setMovie(progress_bar)

        self.actions = QGroupBox("Actions :")
        self.actions_layout = QHBoxLayout()
        self.actions.setLayout(self.actions_layout)

        self.manually_submit = QPushButton("Manually Submit [Advanced users]")
        self.manually_submit.clicked.connect(self.submit_manually)
        self.actions_layout.addWidget(self.manually_submit)
        self.cancel = QPushButton("Abort mission")
        self.cancel.clicked.connect(self.close)
        self.actions_layout.addWidget(self.cancel)
        self.gridLayout.addWidget(self.actions, 2, 0)

        self.actions2 = QGroupBox("Actions :")
        self.actions2_layout = QHBoxLayout()
        self.actions2.setLayout(self.actions2_layout)
        self.manually_submit2 = QPushButton("Manually Submit [Advanced users]")
        self.manually_submit2.clicked.connect(self.submit_manually)
        self.actions2_layout.addWidget(self.manually_submit2)
        self.cancel2 = QPushButton("Abort mission")
        self.cancel2.clicked.connect(self.close)
        self.actions2_layout.addWidget(self.cancel2)
        self.proceed = QPushButton("Accept results")
        self.proceed.setProperty("style", "btn-success")
        self.proceed.clicked.connect(self.process_debriefing)
        self.actions2_layout.addWidget(self.proceed)

        progress_bar.start()
        self.layout.addLayout(self.gridLayout, 1, 0)
        self.setLayout(self.layout)

    @staticmethod
    def add_update_row(description: str, count: Sized, layout: QGridLayout) -> None:
        row = layout.rowCount()
        layout.addWidget(QLabel(f"<b>{description}</b>"), row, 0)
        layout.addWidget(QLabel(f"{len(count)}"), row, 1)

    def updateLayout(self, debriefing: Debriefing) -> None:
        updateBox = QGroupBox("Mission status")
        update_layout = QGridLayout()
        updateBox.setLayout(update_layout)
        self.debriefing = debriefing

        self.add_update_row(
            "Aircraft destroyed", list(debriefing.air_losses.losses), update_layout
        )
        self.add_update_row(
            "Front line units destroyed",
            list(debriefing.front_line_losses),
            update_layout,
        )
        self.add_update_row(
            "Convoy units destroyed", list(debriefing.convoy_losses), update_layout
        )
        self.add_update_row(
            "Shipping cargo destroyed",
            list(debriefing.cargo_ship_losses),
            update_layout,
        )
        self.add_update_row(
            "Airlift cargo destroyed", list(debriefing.airlift_losses), update_layout
        )
        self.add_update_row(
            "Ground units lost at objective areas",
            list(debriefing.ground_object_losses),
            update_layout,
        )
        self.add_update_row(
            "Buildings destroyed", list(debriefing.building_losses), update_layout
        )
        self.add_update_row(
            "Base capture events", debriefing.base_captures, update_layout
        )

        # Clear previous content of the window
        for i in reversed(range(self.gridLayout.count())):
            try:
                self.gridLayout.itemAt(i).widget().setParent(None)
            except:
                logging.exception("Failed to clear window")

        # Set new window content
        self.gridLayout.addWidget(updateBox, 0, 0)

        if not debriefing.state_data.mission_ended:
            self.gridLayout.addWidget(QLabel("<b>Mission is being played</b>"), 1, 0)
            self.gridLayout.addWidget(self.actions, 2, 0)
        else:
            self.gridLayout.addWidget(QLabel("<b>Mission is over</b>"), 1, 0)
            self.gridLayout.addWidget(self.actions2, 2, 0)

    def on_debriefing_update(self, debriefing: Debriefing) -> None:
        try:
            logging.info("On Debriefing update")
            logging.debug(debriefing)
            DebriefingFileWrittenSignal.get_instance().sendDebriefing(debriefing)
        except Exception:
            logging.exception("Got an error while sending debriefing")
        self.wait_thread = wait_for_debriefing(
            lambda d: self.on_debriefing_update(d), self.game, self.unit_map
        )

    def process_debriefing(self):
        with logged_duration("Turn processing"):
            self.game.finish_event(event=self.gameEvent, debriefing=self.debriefing)
            self.game.pass_turn()

            GameUpdateSignal.get_instance().sendDebriefing(self.debriefing)
            GameUpdateSignal.get_instance().updateGame(self.game)
        self.close()

    def debriefing_directory_location(self) -> str:
        return os.path.join(base_path(), "liberation_debriefings")

    def closeEvent(self, evt):
        super(QWaitingForMissionResultWindow, self).closeEvent(evt)
        if self.wait_thread is not None:
            self.wait_thread.stop()

    def submit_manually(self):
        file = QFileDialog.getOpenFileName(
            self, "Select game file to open", filter="json(*.json)", dir="."
        )
        print(file)
        try:
            with open(file[0], "r") as json_file:
                json_data = json.load(json_file)
                json_data["mission_ended"] = True
                debriefing = Debriefing(json_data, self.game, self.unit_map)
                self.on_debriefing_update(debriefing)
        except Exception as e:
            logging.error(e)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Invalid file : " + file[0])
            msg.setWindowTitle("Invalid file.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            msg.exec_()
            return
