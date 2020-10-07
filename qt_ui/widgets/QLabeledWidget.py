"""A layout containing a widget with an associated label."""
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QHBoxLayout, QLabel, QWidget


class QLabeledWidget(QHBoxLayout):
    """A layout containing a widget with an associated label.

    Best used for vertical forms, where the given widget is the input and the
    label is used to name the input.
    """

    def __init__(self, text: str, widget: QWidget) -> None:
        super().__init__()
        self.addWidget(QLabel(text))
        self.addStretch()
        self.addWidget(widget, alignment=Qt.AlignRight)
