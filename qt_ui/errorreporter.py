import logging
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Type

from PySide2.QtWidgets import QDialog, QMessageBox


@contextmanager
def report_errors(
    title: str, parent: QDialog, error_type: Type[Exception] = Exception
) -> Iterator[None]:
    try:
        yield
    except error_type as ex:
        logging.exception(title)
        QMessageBox().critical(parent, title, str(ex), QMessageBox.Ok)
