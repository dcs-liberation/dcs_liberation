# URL for UI links
from PySide2.QtGui import QColor, QFont, QPixmap

URLS = {
    "Manual": "https://github.com/shdwp/dcs_liberation/wiki/Manual",
    "Troubleshooting": "https://github.com/shdwp/dcs_liberation/wiki/Troubleshooting",
    "Modding": "https://github.com/shdwp/dcs_liberation/wiki/Modding-tutorial",
    "Repository": "https://github.com/shdwp/dcs_liberation",
    "ForumThread": "https://forums.eagle.ru/showthread.php?t=214834",
    "Issues": "https://github.com/shdwp/dcs_liberation/issues"
}

COLORS = {
    "red": QColor(255, 125, 125),
    "bright_red": QColor(200, 64, 64),
    "blue": QColor(164, 164, 255),
    "dark_blue": QColor(45, 62, 80),
    "white": QColor(255, 255, 255),
    "green": QColor(128, 186, 128),
    "bright_green": QColor(64, 200, 64),
    "black": QColor(0, 0, 0)
}


CP_SIZE = 25


FONT = QFont("Arial", 12, weight=5, italic=True)

"""
ICONS = {
    "Dawn": QPixmap("../resources/ui/daytime/dawn.png"),
    "Day": QPixmap("../resources/ui/daytime/day.png"),
    "Dusk": QPixmap("../resources/ui/daytime/dusk.png"),
    "Night": QPixmap("../resources/ui/daytime/night.png"),
    "Money": QPixmap("../resources/ui/misc/money_icon.png"),
    "Ordnance": QPixmap("../resources/ui/misc/ordnance_icon.png"),
}
"""
