import os

class ConsoleColors:
    # ANSI escape sequences for text colors
    class Text:
        BLACK = "\033[30m"
        RED = "\033[31m"
        GREEN = "\033[32m"
        YELLOW = "\033[33m"
        BLUE = "\033[34m"
        PURPLE = "\033[35m"
        CYAN = "\033[36m"
        WHITE = "\033[37m"

    # ANSI escape sequences for background colors
    class Background:
        BLACK = "\033[40m"
        RED = "\033[41m"
        GREEN = "\033[42m"
        YELLOW = "\033[43m"
        BLUE = "\033[44m"
        PURPLE = "\033[45m"
        CYAN = "\033[46m"
        WHITE = "\033[47m"

    # ANSI escape sequence to reset all attributes
    RESET = "\033[0m"

    @staticmethod
    def print_with_colors(text, text_color, background_color):
        print(f"{text_color}{background_color}{text}{ConsoleColors.RESET}")

    def console_colors_init():
        if os.name == 'nt':
            os.system('')