from PySide2 import QtCore, QtGui
from PySide2.QtWidgets import QCalendarWidget


class QLiberationCalendar(QCalendarWidget):
    def __init__(self, parent=None):
        super(QLiberationCalendar, self).__init__(parent)
        self.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.setGridVisible(False)

        # Overrride default QCalendar behaviour that is rendering week end days in red
        for d in (
            QtCore.Qt.Monday,
            QtCore.Qt.Tuesday,
            QtCore.Qt.Wednesday,
            QtCore.Qt.Thursday,
            QtCore.Qt.Friday,
            QtCore.Qt.Saturday,
            QtCore.Qt.Sunday,
        ):
            fmt = self.weekdayTextFormat(d)
            fmt.setForeground(QtCore.Qt.darkGray)
            self.setWeekdayTextFormat(d, fmt)

    def paintCell(self, painter, rect, date):
        if date == self.selectedDate():
            painter.save()
            painter.fillRect(rect, QtGui.QColor("#D3D3D3"))
            painter.setPen(QtCore.Qt.NoPen)
            painter.setBrush(QtGui.QColor(52, 68, 85))
            r = QtCore.QRect(
                QtCore.QPoint(), min(rect.width(), rect.height()) * QtCore.QSize(1, 1)
            )
            r.moveCenter(rect.center())
            painter.drawEllipse(r)
            painter.setPen(QtGui.QPen(QtGui.QColor("white")))
            painter.drawText(rect, QtCore.Qt.AlignCenter, str(date.day()))
            painter.restore()
        else:
            super(QLiberationCalendar, self).paintCell(painter, rect, date)
