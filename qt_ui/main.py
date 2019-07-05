import sys
from time import sleep

from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QApplication, QLabel, QSplashScreen

from qt_ui import uiconstants
from qt_ui.windows.QLiberationWindow import QLiberationWindow
from userdata import persistency


if __name__ == "__main__":

    app = QApplication(sys.argv)

    # Splash screen setup
    pixmap = QPixmap("./resources/ui/splash_screen.png")
    splash = QSplashScreen(pixmap)
    splash.show()

    # Load stuff
    persistency.setup(sys.argv[1])

    css = ""
    with open("./qt_ui/stylesheets/style.css") as stylesheet:
        css = stylesheet.read()

    sleep(0.5)
    uiconstants.load_icons()
    app.processEvents()

    # Start window
    window = QLiberationWindow()
    window.setStyleSheet(css)
    window.show()

    splash.finish(window)
    sys.exit(app.exec_())