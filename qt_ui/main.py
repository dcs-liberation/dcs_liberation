import sys
from time import sleep

from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QApplication, QLabel, QSplashScreen

from qt_ui.windows.QLiberationWindow import QLiberationWindow
from userdata import persistency

if __name__ == "__main__":

    app = QApplication(sys.argv)

    pixmap = QPixmap("../resources/ui/splash_screen.png")
    splash = QSplashScreen(pixmap)
    splash.show()

    persistency.setup(sys.argv[1])
    sleep(2)
    app.processEvents()

    window = QLiberationWindow()
    window.show()

    splash.finish(window)
    sys.exit(app.exec_())