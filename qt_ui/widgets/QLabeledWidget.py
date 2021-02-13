"""A layout containing a widget with an associated label."""
from typing import Optional

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QHBoxLayout, QLabel, QWidget


class QLabeledWidget(QHBoxLayout):
    """A layout containing a widget with an associated label.

    Best used for vertical forms, where the given widget is the input and the
    label is used to name the input.
    """

    def __init__(
        self, text: str, widget: QWidget, tooltip: Optional[str] = None
    ) -> None:
        super().__init__()
        label = QLabel(text)
        self.addWidget(label)
        self.addStretch()
        self.addWidget(widget, alignment=Qt.AlignRight)
        if tooltip is not None:
            label.setToolTip(tooltip)
            widget.setToolTip(tooltip)
