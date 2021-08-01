import logging
import typing

from PySide2.QtWidgets import (
    QDialog,
    QPlainTextEdit,
    QVBoxLayout,
    QPushButton,
)
from PySide2.QtGui import QTextCursor

from qt_ui.logging_handler import HookableInMemoryHandler


class QLogsWindow(QDialog):
    vbox: QVBoxLayout
    textbox: QPlainTextEdit
    clear_button: QPushButton
    _logging_handler: typing.Optional[HookableInMemoryHandler]

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Logs")
        self.setMinimumSize(400, 100)
        self.resize(1000, 450)

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

        self._logging_handler = None
        logger = logging.getLogger()
        for handler in logger.handlers:
            if isinstance(handler, HookableInMemoryHandler):
                self._logging_handler = handler
                break
        if self._logging_handler is not None:
            self.textbox.setPlainText(self._logging_handler.log)
            self.textbox.moveCursor(QTextCursor.End)
            self._logging_handler.setHook(self.appendLog)
        else:
            self.textbox.setPlainText("WARNING: logging not initialized!")

    def clearLogs(self) -> None:
        if self._logging_handler is not None:
            self._logging_handler.clearLog()
        self.textbox.setPlainText("")

    def appendLog(self, msg: str):
        self.textbox.appendPlainText(msg)
        self.textbox.moveCursor(QTextCursor.End)
