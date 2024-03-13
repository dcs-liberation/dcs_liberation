import typing

from PySide6.QtCore import Signal
from PySide6.QtGui import QTextCursor, QIcon
from PySide6.QtWidgets import (
    QDialog,
    QPlainTextEdit,
    QVBoxLayout,
    QPushButton,
)

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

        try:
            # This assumes that there's never more than one in memory handler. We don't
            # configure more than one by default, but logging is customizable with
            # resources/logging.yaml. If someone adds a second in-memory handler, only
            # the first one (in arbitrary order) will be shown.
            self._logging_handler = next(
                HookableInMemoryHandler.iter_registered_handlers()
            )
        except StopIteration:
            self._logging_handler = None

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
