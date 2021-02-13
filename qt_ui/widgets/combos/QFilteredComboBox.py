from PySide2.QtCore import QSortFilterProxyModel, Qt
from PySide2.QtWidgets import QComboBox, QCompleter


class QFilteredComboBox(QComboBox):
    def __init__(
        self,
        parent=None,
        include_targets=True,
        include_airbases=True,
        include_frontlines=True,
        include_units=True,
        include_enemy=True,
        include_friendly=True,
    ):
        super(QFilteredComboBox, self).__init__(parent)

        self.setFocusPolicy(Qt.StrongFocus)
        self.setEditable(True)
        self.completer = QCompleter(self)

        self.include_targets = include_targets
        self.include_airbases = include_airbases
        self.include_frontlines = include_frontlines
        self.include_units = include_units
        self.include_enemy = include_enemy
        self.include_friendly = include_friendly

        # always show all completions
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.pFilterModel = QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)

        self.completer.setPopup(self.view())

        self.setCompleter(self.completer)

        self.lineEdit().textEdited.connect(self.pFilterModel.setFilterFixedString)
        self.completer.activated.connect(self.setTextIfCompleterIsClicked)

    def setModel(self, model):
        super(QFilteredComboBox, self).setModel(model)
        self.pFilterModel.setSourceModel(model)
        self.completer.setModel(self.pFilterModel)
        self.model().sort(0)

    def setModelColumn(self, column):
        self.completer.setCompletionColumn(column)
        self.pFilterModel.setFilterKeyColumn(column)
        super(QFilteredComboBox, self).setModelColumn(column)

    def view(self):
        return self.completer.popup()

    def index(self):
        return self.currentIndex()

    def setTextIfCompleterIsClicked(self, text):
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)
