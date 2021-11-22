from PySide2.QtWidgets import QFrame


class QDebriefingInformation(QFrame):
    """
    UI component to display debreifing informations
    """

    def __init__(self):
        super(QDebriefingInformation, self).__init__()
        self.init_ui()
