from collections.abc import Iterator
from contextlib import contextmanager

from PySide6.QtWidgets import QWidget


@contextmanager
def block_signals(widget: QWidget) -> Iterator[None]:
    blocked = widget.blockSignals(True)
    try:
        yield
    finally:
        widget.blockSignals(blocked)
