from typing import Literal
import logging

# ==========================================================================================
#                                       LOGGER
# ==========================================================================================
_logger: logging.Logger | None = None

def set_logger(logger: logging.Logger) -> None:
    global _logger
    _logger = logger

def print_log(text: str, end: str = "\n", log_type: Literal["error", "warning", "info"] = "info") -> None:
    if _logger:
        if log_type == "error":
            _logger.error(text)
        elif log_type == "warning":
            _logger.warning(text)
        else: # log_type == "info":
            _logger.info(text)
    else:
        print(text, end=end)
# ==========================================================================================
#                                       GENERAL
# ==========================================================================================




_separators = {
    "short" : "_"*32,
    "normal": "_"*64,
    "long"  : "_"*128,
    "super" : "="*128,
    "start" : "="*128,
}
SepType = Literal["SHORT", "NORMAL", "LONG", "SUPER", "START"]

_colors = {
    "red":    "\033[31m",
    "green":  "\033[32m",
    "yellow": "\033[33m",
    "blue":   "\033[34m",
    "white":  "\033[0m",
}
Colors = Literal["red", "green", "blue", "yellow", "white"]

def print_separator(text: str, sep_type: SepType = "NORMAL") -> None:
    """Prints a text with a line that separes the bash outputs. The size of this line is controled by sep_type

    Args:
        text (str): Text to print.
        sep_type (Literal['SHORT', 'NORMAL', 'LONG', 'SUPER', 'START'], optional): Type of the separation line. Defaults to "NORMAL".
    """

    sep = _separators.get(sep_type.lower(), "") # If the separator is not there do it with ''
    if not sep:
        print_warn("WARNING: No separator with that label")

    if sep_type == "SUPER":
        print_log(sep)
        print_log(f"{text:^{len(sep)}}")
        print_log(sep + "\n")
    elif sep_type == "START":
        print_color(sep + "\n", color="blue")
        print_color(f"{text:^{len(sep)}}\n", color="blue")
        print_color(sep + "\n", color="blue")
    else:
        print_log(sep)
        print_log(f"{text:^{len(sep)}}\n")


def print_color(text: str, color: Colors = "white", print_text: bool = True) -> str:
    """Prints the text with a certain color

    Args:
        text (str): Text to print
        color (Literal['red', 'green', 'blue', 'white'], optional): Color to use. Defaults to "white".
        print_text bool: Whether or not to print the color text (if false it will return it)

    Return: 
        str: Text with colors
    """
    color =  _colors.get(color, _colors['white'])
    text: str = f"{color}{text}{_colors['white']}"

    if print_text:
        print_log(f"{text}")

    return text


def print_warn(text: str, color: Colors = "yellow") -> str:
    """Adds the text between teh following emoji ⚠️...⚠️

    Args:
        text (str): Text to print in warn
        color (Colors, optional): Color of the warning text. Defaults to "yellow".

    Returns:
        str: Text with color and emojis
    """
    return print_color(f"⚠️{text}⚠️", color=color)

def print_error(text: str, color: Colors = "red") -> str:
    """Adds the text between teh following emoji ❌...❌

    Args:
        text (str): Text to print in warn
        color (Colors, optional): Color of the error text. Defaults to "red".

    Returns:
        str: Text with color and emojis
    """
    return print_color(f"❌{text}❌", color=color)


# ==========================================================================================
#                                    CLEAR LINES
# ==========================================================================================
def print_status(msg: str):
    """Prints a dynamic status message on the same terminal line.

    Useful for updating progress or status in-place (e.g. during loops),
    preventing multiple lines of output.

    Args:
        msg (str): Message to display.
    """
    clear_line = " " * 120  # assume max 120 chars per line
    print_log(f"{clear_line}\r{msg}\r", end="\r")

def clear_status():
    """Clears the previous status line
    """
    print_status("")

def clear_bash(n_lines: int = 1) -> None:
    """Cleans the bash output by removing the last n lines.

    Args:
        n_lines (int, optional): Number of lines to remove. Defaults to 1.
    """
    print_log("\033[F\033[K"*n_lines, end="")  # Move cursor up one line and clear that line

def print_clear_bash(text: str, n_lines: int = 1) -> None:
    """Cleans the bash output by removing the last n lines.

    Args:
        n_lines (int, optional): Number of lines to remove. Defaults to 1.
    """
    clear_bash(n_lines)
    print_log(text)