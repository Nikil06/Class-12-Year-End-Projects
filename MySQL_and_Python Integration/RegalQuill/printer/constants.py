class Colors:
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"


class Styles:
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"


reset = "\033[0m"
reset_colours = "\033[39m"

colours = {
    ########################
    # BASIC COLOURS
    "black": Colors.BLACK,
    "blue": Colors.BLUE,
    "red": Colors.RED,
    "green": Colors.GREEN,
    "brown": Colors.BROWN,
    "purple": Colors.PURPLE,
    "cyan": Colors.CYAN,
    "yellow": Colors.YELLOW,
    ########################
    # LIGHT COLOURS
    "l gray": Colors.LIGHT_GRAY,
    "d gray": Colors.DARK_GRAY,  # I know
    "l white": Colors.LIGHT_WHITE,

    "l blue": Colors.LIGHT_BLUE,
    "l red": Colors.LIGHT_RED,
    "l green": Colors.LIGHT_GREEN,
    # no light brown tag
    "l purple": Colors.LIGHT_PURPLE,
    "l cyan": Colors.LIGHT_CYAN,
    ########################
}

styles = {
    # STYLES
    "bold": Styles.BOLD,
    "faint": Styles.FAINT,
    "italic": Styles.ITALIC,
    "underline": Styles.UNDERLINE,
    "blink": Styles.BLINK,
    "negative": Styles.NEGATIVE,
    "crossed": Styles.CROSSED,
}

tag_map = {**colours, **styles, "reset": reset, "reset_colours": reset_colours}
