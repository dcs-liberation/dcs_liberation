from contextlib import contextmanager
from typing import ContextManager, Optional

from PySide2.QtCore import QModelIndex, Qt, QSize
from PySide2.QtGui import QPainter, QFont, QFontMetrics, QIcon
from PySide2.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem, QStyle


@contextmanager
def painter_context(painter: QPainter) -> ContextManager[None]:
    try:
        painter.save()
        yield
    finally:
        painter.restore()


class TwoColumnRowDelegate(QStyledItemDelegate):
    HMARGIN = 4
    VMARGIN = 4

    def __init__(self, rows: int, columns: int, font_size: int = 12) -> None:
        if columns not in (1, 2):
            raise ValueError(f"Only one or two columns may be used, not {columns}")
        super().__init__()
        self.font_size = font_size
        self.rows = rows
        self.columns = columns

    def get_font(self, option: QStyleOptionViewItem) -> QFont:
        font = QFont(option.font)
        font.setPointSize(self.font_size)
        return font

    def text_for(self, index: QModelIndex, row: int, column: int) -> str:
        raise NotImplementedError

    def paint(
        self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex
    ) -> None:
        # Draw the list item with all the default selection styling, but with an
        # invalid index so text formatting is left to us.
        super().paint(painter, option, QModelIndex())

        rect = option.rect.adjusted(
            self.HMARGIN, self.VMARGIN, -self.HMARGIN, -self.VMARGIN
        )

        with painter_context(painter):
            painter.setFont(self.get_font(option))

            icon: Optional[QIcon] = index.data(Qt.DecorationRole)

            if icon is not None:
                icon.paint(
                    painter,
                    rect,
                    Qt.AlignLeft | Qt.AlignVCenter,
                    self.icon_mode(option),
                    self.icon_state(option),
                )
            rect = rect.adjusted(self.icon_size(option).width() + self.HMARGIN, 0, 0, 0)

            row_height = rect.height() / self.rows
            for row in range(self.rows):
                y = row_height * row
                location = rect.adjusted(0, y, 0, y)
                painter.drawText(location, Qt.AlignLeft, self.text_for(index, row, 0))
                if self.columns == 2:
                    painter.drawText(
                        location, Qt.AlignRight, self.text_for(index, row, 1)
                    )

    @staticmethod
    def icon_mode(option: QStyleOptionViewItem) -> QIcon.Mode:
        if not (option.state & QStyle.State_Enabled):
            return QIcon.Disabled
        elif option.state & QStyle.State_Selected:
            return QIcon.Selected
        elif option.state & QStyle.State_Active:
            return QIcon.Active
        return QIcon.Normal

    @staticmethod
    def icon_state(option: QStyleOptionViewItem) -> QIcon.State:
        return QIcon.On if option.state & QStyle.State_Open else QIcon.Off

    @staticmethod
    def icon_size(option: QStyleOptionViewItem) -> QSize:
        icon_size: Optional[QSize] = option.decorationSize
        if icon_size is None:
            return QSize(0, 0)
        else:
            return icon_size

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        metrics = QFontMetrics(self.get_font(option))
        widths = []
        heights = []

        icon_size = self.icon_size(option)
        icon_width = 0
        icon_height = 0
        if icon_size.width():
            icon_width = icon_size.width() + self.HMARGIN
        if icon_size.height():
            icon_height = icon_size.height() + self.VMARGIN

        for row in range(self.rows):
            width = 0
            height = 0
            for column in range(self.columns):
                size = metrics.size(0, self.text_for(index, row, column))
                width += size.width()
                height = max(height, size.height())
            widths.append(width)
            heights.append(height)

        return QSize(
            icon_width + max(widths) + 2 * self.HMARGIN,
            max(icon_height, sum(heights)) + 2 * self.VMARGIN,
        )
