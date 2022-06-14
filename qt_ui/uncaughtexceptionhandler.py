# From https://timlehr.com/python-exception-hooks-with-qt-message-box/
import logging
import sys
import traceback

from PySide2.QtCore import Signal, QObject
from PySide2.QtWidgets import QMessageBox, QApplication


class UncaughtExceptionHandler(QObject):
    _exception_caught = Signal(str, str)

    def __init__(self, parent: QObject):
        super().__init__(parent)
        sys.excepthook = self.exception_hook
        # Use a signal so that the message box always comes from the main thread.
        self._exception_caught.connect(self.show_exception_box)

    def exception_hook(self, exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            # Ignore keyboard interrupt to support console applications.
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        logging.exception(
            "Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback)
        )
        self._exception_caught.emit(
            str(exc_value),
            "".join(traceback.format_exception(exc_type, exc_value, exc_traceback)),
        )

    def show_exception_box(self, message: str, exception: str) -> None:
        if QApplication.instance() is not None:
            QMessageBox().critical(
                QApplication.focusWidget(),
                "An unexpected error occurred",
                "\n".join([message, "", exception]),
                QMessageBox.Ok,
            )
        else:
            logging.critical("No QApplication instance available.")
