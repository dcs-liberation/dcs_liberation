from PySide6.QtWidgets import QFrame


class QDebriefingInformation(QFrame):
    """
    UI component to display debreifing information
    """

    def __init__(self):
        super(QDebriefingInformation, self).__init__()
        self.init_ui()
