import webbrowser

from PySide2.QtCore import Qt
from PySide2.QtGui import QGuiApplication
from PySide2.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QWidget

from game.version import BUILD_NUMBER, GIT_SHA, VERSION_NUMBER


class BugReportDialog(QDialog):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setWindowTitle("Report an issue")
        self.setModal(True)
        self.setMaximumWidth(600)

        layout = QVBoxLayout()
        self.setLayout(layout)

        components = [f"DCS Liberation {VERSION_NUMBER}"]
        if BUILD_NUMBER is not None:
            components.append(f"Build {BUILD_NUMBER}")
        if GIT_SHA is not None:
            components.append(f"Git revision {GIT_SHA}")

        self.report_data = "\n".join(components)

        label = QLabel(
            "Use the button below to file a bug. The version information will be "
            "automatically copied to your clipboard. Paste that information into the "
            "box in the bug template that asks for the version.<br />"
            "<br />"
            "<strong>Look for duplicate bugs before filing.</strong><br />"
            "<br />"
            "<strong>If the template asks for a save game, it is required. No matter "
            "how easily reproducible the bug may appear, it rarely is. If it were "
            "obvious you wouldn't be the first to find it.</strong><br />"
            "<br />"
            f"{'<br />'.join(components)}<br />"
        )
        label.setTextInteractionFlags(
            Qt.TextSelectableByMouse
            | Qt.LinksAccessibleByMouse
            | Qt.LinksAccessibleByKeyboard
        )
        label.setWordWrap(True)
        label.setOpenExternalLinks(True)
        layout.addWidget(label)

        copy_button = QPushButton("Copy details to clipboard and go to bug page")
        copy_button.clicked.connect(self.on_file_bug)
        layout.addWidget(copy_button)

    def on_file_bug(self) -> None:
        QGuiApplication.clipboard().setText(self.report_data)
        webbrowser.open_new_tab(
            "https://github.com/dcs-liberation/dcs_liberation/issues/new/choose"
        )
