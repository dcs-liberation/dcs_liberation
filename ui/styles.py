# Style for UI

# Padding
PADDING_X = 5
PADDING_Y = 5

# Colors
FG_COLOR = "white"
FG_COLOR_LIGHT = "#dddddd"
BG_COLOR = "#4E5760"
GREEN = "#699245"
YELLOW = "#BF9A46"
RED = "#D0232E"
BG_TITLE_COLOR = "#2D3E50"
BG_SUBTITLE_COLOR = "#3E4F61"

# Fonts
FONT_FAMILY = "Trebuchet MS"
DEFAULT_FONT = (FONT_FAMILY, 8)
ITALIC = (FONT_FAMILY, 8, "italic")
BOLD_FONT = (FONT_FAMILY, 10, "bold italic")
TITLE_FONT = (FONT_FAMILY, 16, "bold italic")

# List of styles
STYLES = {}
STYLES["label-frame"] = {"font": BOLD_FONT, "bg": BG_COLOR, "fg": FG_COLOR}
STYLES["frame-wrapper"] = {"bg": BG_COLOR, "relief":"sunken"}

STYLES["body"] = {"bg": BG_COLOR, "padx": 10, "pady": 10}
STYLES["strong"] = {"font": BOLD_FONT, "bg": BG_TITLE_COLOR, "fg": FG_COLOR}
STYLES["substrong"] = {"font": BOLD_FONT, "bg": BG_SUBTITLE_COLOR, "fg": FG_COLOR}
STYLES["strong-grey"] = {"font": BOLD_FONT, "bg": BG_TITLE_COLOR, "fg": FG_COLOR_LIGHT}

STYLES["mission-preview"] = {"font": BOLD_FONT, "bg": YELLOW, "fg": FG_COLOR}

STYLES["widget"] = {"bg": BG_COLOR, "fg": FG_COLOR, "padx": PADDING_X, "pady": PADDING_Y, "font": DEFAULT_FONT}
STYLES["italic"] = {"bg": BG_COLOR, "fg": FG_COLOR, "padx": PADDING_X, "pady": PADDING_Y, "font": ITALIC}
STYLES["radiobutton"] = {"bg": BG_COLOR, "fg": "black", "padx": PADDING_X, "pady": PADDING_Y, "font": DEFAULT_FONT,
                         "activebackground": BG_COLOR, "highlightbackground": BG_COLOR, "selectcolor": "white"}
STYLES["title"] = {"bg": BG_TITLE_COLOR, "fg": FG_COLOR, "padx": PADDING_X, "pady": PADDING_Y, "font": TITLE_FONT}
STYLES["title-green"] = {"bg": GREEN, "fg": FG_COLOR, "padx": PADDING_X, "pady": PADDING_Y, "font": TITLE_FONT}
STYLES["title-red"] = {"bg": RED, "fg": FG_COLOR, "padx": PADDING_X, "pady": PADDING_Y, "font": TITLE_FONT}
STYLES["header"] = {"bg": BG_TITLE_COLOR}
STYLES["subheader"] = {"bg": BG_SUBTITLE_COLOR}

STYLES["btn-primary"] = {"bg": GREEN, "fg": FG_COLOR, "padx": PADDING_X, "pady": 2, "font": DEFAULT_FONT}
STYLES["btn-danger"] = {"bg": RED, "fg": FG_COLOR, "padx": PADDING_X, "pady": 2, "font": DEFAULT_FONT}
STYLES["btn-warning"] = {"bg": YELLOW, "fg": FG_COLOR, "padx": PADDING_X, "pady": 2, "font": DEFAULT_FONT}
