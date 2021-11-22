import logging
import typing

from PySide2.QtCore import Signal
from PySide2.QtWidgets import (
    QDialog,
    QPlainTextEdit,
    QVBoxLayout,
    QPushButton,
)
from PySide2.QtGui import QTextCursor, QIcon

from qt_ui.logging_handler import HookableInMemoryHandler


class QLogsWindow(QDialog):
    appendLogSignal = Signal(str)

    vbox: QVBoxLayout
    textbox: QPlainTextEdit
    clear_button: QPushButton
    _logging_handler: typing.Optional[HookableInMemoryHandler]

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Logs")
        self.setMinimumSize(400, 100)
        self.resize(1000, 450)
        self.setWindowIcon(QIcon("./resources/icon.png"))

        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

        self.textbox = QPlainTextEdit(self)
        self.textbox.setReadOnly(True)
        self.textbox.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.textbox.move(10, 10)
        self.textbox.resize(1000, 450)
        self.textbox.setStyleSheet(
            "font-family: 'Courier New', monospace; background: #1D2731;"
        )
        self.vbox.addWidget(self.textbox)

        self.clear_button = QPushButton(self)
        self.clear_button.setText("CLEAR")
        self.clear_button.setProperty("style", "btn-primary")
        self.clear_button.clicked.connect(self.clearLogs)
        self.vbox.addWidget(self.clear_button)

        self.appendLogSignal.connect(self.appendLog)

        self._logging_handler = None
        logger = logging.getLogger()
        for handler in logger.handlers:
            if isinstance(handler, HookableInMemoryHandler):
                self._logging_handler = handler
                break
        if self._logging_handler is not None:
            self.textbox.setPlainText(self._logging_handler.log)
            self.textbox.moveCursor(QTextCursor.End)
            # The Handler might be called from a different thread,
            # so use signal/slot to properly handle the event in the main thread.
            # https://github.com/dcs-liberation/dcs_liberation/issues/1493
            self._logging_handler.setHook(self.appendLogSignal.emit)
        else:
            self.textbox.setPlainText("WARNING: logging not initialized!")

    def clearLogs(self) -> None:
        if self._logging_handler is not None:
            self._logging_handler.clearLog()
        self.textbox.setPlainText("")

    def appendLog(self, msg: str):
        self.textbox.appendPlainText(msg)
        self.textbox.moveCursor(QTextCursor.End)
