from PySide2.QtCore import QItemSelectionModel, QPoint
from PySide2.QtGui import QStandardItemModel
from PySide2.QtWidgets import QListView

from game import Game, game
from qt_ui.windows.infos.QInfoItem import QInfoItem


class QInfoList(QListView):
    def __init__(self, game: Game):
        super(QInfoList, self).__init__()
        self.model = QStandardItemModel(self)
        self.setModel(self.model)
        self.game = game
        self.update_list()

        self.selectionModel().setCurrentIndex(
            self.indexAt(QPoint(1, 1)), QItemSelectionModel.Select
        )
        self.selectionModel().selectionChanged.connect(self.on_selected_info_changed)

    def on_selected_info_changed(self):
        index = self.selectionModel().currentIndex().row()

    def update_list(self):
        self.model.clear()
        if self.game is not None:
            for i, info in enumerate(reversed(self.game.informations)):
                self.model.appendRow(QInfoItem(info))
            self.selectionModel().setCurrentIndex(
                self.indexAt(QPoint(1, 1)), QItemSelectionModel.Select
            )

    def setGame(self, game):
        self.game = game
        self.update_list()
