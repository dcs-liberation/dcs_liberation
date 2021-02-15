from contextlib import contextmanager
from typing import ContextManager

from PySide2.QtGui import QPainter


@contextmanager
def painter_context(painter: QPainter) -> ContextManager[None]:
    try:
        painter.save()
        yield
    finally:
        painter.restore()
