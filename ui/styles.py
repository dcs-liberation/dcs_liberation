# Style for UI

# Padding
PADDING_X = 5
PADDING_Y = 5

# Colors
FG_COLOR = "white"
BG_COLOR = "#4E5760"
BTN_COLOR = "#699245"
YELLOW = "#FDB731"
RED = "#D0232E"
BG_TITLE_COLOR = "#2D3E50"

# Fonts
FONT_FAMILY = "Trebuchet MS"
DEFAULT_FONT = (FONT_FAMILY, 8)
BOLD_FONT = (FONT_FAMILY, 10, "bold italic")
TITLE_FONT = (FONT_FAMILY, 16, "bold italic")

# List of styles
STYLES = {}
STYLES["label-frame"] = {"font": BOLD_FONT, "bg": BG_COLOR, "fg": FG_COLOR}
STYLES["frame-wrapper"] = {"bg": BG_COLOR, "relief":"sunken"}

STYLES["body"] = {"bg": BG_COLOR, "padx": 25, "pady": 35}
STYLES["strong"] = {"font": BOLD_FONT, "bg": BG_TITLE_COLOR, "fg": FG_COLOR}
STYLES["widget"] = {"bg": BG_COLOR, "fg": FG_COLOR, "padx": PADDING_X, "pady": PADDING_Y, "font": DEFAULT_FONT}
STYLES["radiobutton"] = {"bg": BG_COLOR, "fg": "black", "padx": PADDING_X, "pady": PADDING_Y, "font": DEFAULT_FONT,
                         "activebackground": BG_COLOR, "highlightbackground": BG_COLOR, "selectcolor": "white"}
STYLES["title"] = {"bg": BG_TITLE_COLOR, "fg": FG_COLOR, "padx": PADDING_X, "pady": PADDING_Y, "font": TITLE_FONT}
STYLES["header"] = {"bg": BG_TITLE_COLOR}

STYLES["btn-primary"] = {"bg": BTN_COLOR, "fg": FG_COLOR, "padx": PADDING_X, "pady": 2, "font": DEFAULT_FONT}
STYLES["btn-danger"] = {"bg": RED, "fg": FG_COLOR, "padx": PADDING_X, "pady": 2, "font": DEFAULT_FONT}
STYLES["btn-warning"] = {"bg": YELLOW, "fg": FG_COLOR, "padx": PADDING_X, "pady": 2, "font": DEFAULT_FONT}
