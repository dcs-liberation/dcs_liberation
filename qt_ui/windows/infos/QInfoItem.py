from PySide2.QtGui import QStandardItem

from game.infos.information import Information


class QInfoItem(QStandardItem):

    def __init__(self, info: Information):
        super(QInfoItem, self).__init__()
        self.info = info
        self.setText("[%02d]" % self.info.turn + " " + self.info.title + ' : {:<16}'.format(info.text))
        self.setEditable(False)
