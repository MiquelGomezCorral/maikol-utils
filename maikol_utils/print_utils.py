import logging
from typing import Literal, Optional, TextIO


from .other_utils import parse_seconds_to_minutes
from .config import get_logger, get_base_log_level, LogLevel

# ==========================================================================================
#                                       LOGGER
# ==========================================================================================

def print_log(
    text: str, 
    end: str = "\n", 
    logger: logging.Logger = None,
    log_level: LogLevel = None
) -> None:
    if logger is None:
        logger = get_logger()
    if log_level is None:
        log_level = get_base_log_level()

    if logger: # Make sense bc get_logger may return None
        # get he correct level and if not listed use info
        log_func = getattr(logger, log_level, logger.info)
        log_func(text)
    else:
        print(text, end=end)


# ==========================================================================================
#                                       GENERAL
# ==========================================================================================
_separators_max_length = 128
_separators = {
    "short" : "_"*int(_separators_max_length/4),
    "normal": "_"*int(_separators_max_length/2),
    "long"  : "_"*int(_separators_max_length),
    "super" : "="*int(_separators_max_length),
    "start" : "="*int(_separators_max_length),
}
SepType = Literal["SHORT", "NORMAL", "LONG", "SUPER", "START"]

_colors = {
    # Regular colors
    "black": "\033[0;30m",
    "red": "\033[0;31m",
    "green": "\033[0;32m",
    "yellow": "\033[0;33m",
    "blue": "\033[0;34m",
    "purple": "\033[0;35m",
    "cyan": "\033[0;36m",
    "white": "\033[0;37m",

    # Other styles
    "reset": "\033[0m",
    "italic": "\033[3m",
    "bold_italic": "\033[1;3m",
    "underline": "\033[4m",
    "strikethrough": "\033[9m",

    # Bold
    "bold_black": "\033[1;30m",
    "bold_red": "\033[1;31m",
    "bold_green": "\033[1;32m",
    "bold_yellow": "\033[1;33m",
    "bold_blue": "\033[1;34m",
    "bold_purple": "\033[1;35m",
    "bold_cyan": "\033[1;36m",
    "bold_white": "\033[1;37m",

    # Underline
    "underline_black": "\033[4;30m",
    "underline_red": "\033[4;31m",
    "underline_green": "\033[4;32m",
    "underline_yellow": "\033[4;33m",
    "underline_blue": "\033[4;34m",
    "underline_purple": "\033[4;35m",
    "underline_cyan": "\033[4;36m",
    "underline_white": "\033[4;37m",

    # Background
    "bg_black": "\033[40m",
    "bg_red": "\033[41m",
    "bg_green": "\033[42m",
    "bg_yellow": "\033[43m",
    "bg_blue": "\033[44m",
    "bg_purple": "\033[45m",
    "bg_cyan": "\033[46m",
    "bg_white": "\033[47m",

    # High Intensity
    "hi_black": "\033[0;90m",
    "hi_red": "\033[0;91m",
    "hi_green": "\033[0;92m",
    "hi_yellow": "\033[0;93m",
    "hi_blue": "\033[0;94m",
    "hi_purple": "\033[0;95m",
    "hi_cyan": "\033[0;96m",
    "hi_white": "\033[0;97m",

    # Bold High Intensity
    "bold_hi_black": "\033[1;90m",
    "bold_hi_red": "\033[1;91m",
    "bold_hi_green": "\033[1;92m",
    "bold_hi_yellow": "\033[1;93m",
    "bold_hi_blue": "\033[1;94m",
    "bold_hi_purple": "\033[1;95m",
    "bold_hi_cyan": "\033[1;96m",
    "bold_hi_white": "\033[1;97m",

    # High Intensity backgrounds
    "bg_hi_black": "\033[0;100m",
    "bg_hi_red": "\033[0;101m",
    "bg_hi_green": "\033[0;102m",
    "bg_hi_yellow": "\033[0;103m",
    "bg_hi_blue": "\033[0;104m",
    "bg_hi_purple": "\033[0;105m",
    "bg_hi_cyan": "\033[0;106m",
    "bg_hi_white": "\033[0;107m",
}
Colors = Literal[
    "black", 
    "red", 
    "green", 
    "yellow", 
    "blue", 
    "purple", 
    "cyan", 
    "white", 

    "reset", 
    "italic", 
    "bold_italic", 
    "underline", 
    "strikethrough"

    "bold_black", 
    "bold_red", 
    "bold_green", 
    "bold_yellow", 
    "bold_blue", 
    "bold_purple", 
    "bold_cyan", 
    "bold_white", 

    "underline_black", 
    "underline_red", 
    "underline_green", 
    "underline_yellow", 
    "underline_blue", 
    "underline_purple", 
    "underline_cyan", 
    "underline_white", 

    "bg_black", 
    "bg_red", 
    "bg_green", 
    "bg_yellow", 
    "bg_blue", 
    "bg_purple", 
    "bg_cyan", 
    "bg_white", 

    "hi_black", 
    "hi_red", 
    "hi_green", 
    "hi_yellow", 
    "hi_blue", 
    "hi_purple", 
    "hi_cyan", 
    "hi_white", 

    "bold_hi_black", 
    "bold_hi_red", 
    "bold_hi_green", 
    "bold_hi_yellow", 
    "bold_hi_blue", 
    "bold_hi_purple", 
    "bold_hi_cyan", 
    "bold_hi_white", 

    "bg_hi_black", 
    "bg_hi_red", 
    "bg_hi_green", 
    "bg_hi_yellow", 
    "bg_hi_blue", 
    "bg_hi_purple", 
    "bg_hi_cyan", 
    "bg_hi_white", 
]


def print_separator(text: str = None, sep_type: SepType = "NORMAL") -> None:
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
        if text:
            print_log(f"{text:^{len(sep)}}")
        print_log(sep + "\n")
    elif sep_type == "START":
        print_color(sep + "\n", color="blue")
        if text:
            print_color(f"{text:^{len(sep)}}\n", color="blue")
        print_color(sep + "\n", color="blue")
    else:
        print_log(sep)
        if text:
            print_log(f"{text:^{len(sep)}}\n")


def print_color(text: str, color: Colors = "reset", log_level: LogLevel = 'info', print_text: bool = True) -> str:
    """Prints the text with a certain color

    Args:
        text (str): Text to print
        color (Literal['red', 'green', 'blue', 'reset'...], optional): Color to use. Defaults to "reset".
        print_text bool: Whether or not to print the color text (if false it will return it)

    Return: 
        str: Text with colors
    """
    color =  _colors.get(color, _colors['reset'])
    text: str = f"{color}{text}{_colors['reset']}"

    if print_text:
        print_log(f"{text}", log_level=log_level)

    return text


def print_warn(text: str, color: Colors = "yellow", prefix: str = '', suffix: str = '') -> str:
    """Format and print a warning message surrounded by ⚠️ emojis.

    Args:
        text (str): The message to display as a warning.
        color (Colors, optional): The color of the warning text. Defaults to "yellow".
        prefix (str, optional): Text to prepend before the warning. Defaults to ''.
        suffix (str, optional): Text to append after the warning. Defaults to ''.

    Returns:
        str: The formatted warning text with color and emojis.
    """
    return print_color(f"{prefix}⚠️{text}⚠️{suffix}", color=color, log_level="warning")

def print_error(text: str, color: Colors = "red", prefix: str = '', suffix: str = '') -> str:
    """Format and print an error message surrounded by ❌ emojis.

    Args:
        text (str): The message to display as an error.
        color (Colors, optional): The color of the error text. Defaults to "red".
        prefix (str, optional): Text to prepend before the error. Defaults to ''.
        suffix (str, optional): Text to append after the error. Defaults to ''.

    Returns:
        str: The formatted error text with color and emojis.
    """
    return print_color(f"{prefix}❌{text}❌{suffix}", color=color, log_level="error")


# ==========================================================================================
#                                    CLEAR LINES
# ==========================================================================================
def print_status(msg: str, log_level: LogLevel = None):
    """Prints a dynamic status message on the same terminal line.

    Useful for updating progress or status in-place (e.g. during loops),
    preventing multiple lines of output.

    Args:
        msg (str): Message to display.
    """
    if log_level is None:
        log_level = get_base_log_level()
    clear_line = " " * _separators_max_length  # assume max 120 chars per line
    print_log(f"{clear_line}\r{msg}\r", end="\r", log_level=log_level)

def clear_status(log_level: LogLevel = None):
    """Clears the previous status line
    """
    if log_level is None:
        log_level = get_base_log_level()
    print_status("", log_level=log_level)

def clear_bash(n_lines: int = 1) -> None:
    """Cleans the bash output by removing the last n lines.

    Args:
        n_lines (int, optional): Number of lines to remove. Defaults to 1.
    """
    print_log("\033[F\033[K"*n_lines, end="")  # Move cursor up one line and clear that line

def print_clear_bash(text: str, n_lines: int = 1, log_level: LogLevel = None) -> None:
    """Cleans the bash output by removing the last n lines.

    Args:
        n_lines (int, optional): Number of lines to remove. Defaults to 1.
    """
    if log_level is None:
        log_level = get_base_log_level()
    clear_bash(n_lines)
    print_log(text, log_level=log_level)


def print_utf_8(text: str, print_text: bool = True) -> str:
    """Decode escaped Unicode sequences in a string and optionally print it.

    Encodes the input string to UTF-8, decodes escape sequences (e.g. "\\u00e9"),
    replaces "\\n" with newlines, and returns the processed text.

    Args:
        text (str): Input text containing escaped Unicode characters.
        print_text (bool, optional): If True, print the processed text. Defaults to True.

    Returns:
        str: The decoded and formatted text.
    """
    text = text.encode("utf-8").decode("unicode_escape").replace("\\n", "\n")
    if print_text:
        print(text)
    return text

# ==========================================================================================
#                                    TIME FORMATTING
# ==========================================================================================
def print_time(sec: float, n_files: Optional[int] = None, space: bool = False, prefix: str = "", sufix: str = "", out_file: Optional[TextIO] = None) -> None:
    """Given a certain number of seconds, parse it to Formatted time string (e.g., '01 hrs, 05 mins, 30.1234 sec').
    If not enough seconds for hours, just '05 mins, 30.1234 sec'.
    If neither enogh seconds for minuts, just parse '30.1234 sec'.
    Optionally you can add a 'number of files' to get avg metrics as well as extra config for better printing. 
    Optionally you can pass a file to print everyting there.

    Args:
        sec (float): Number of seconds
        n_files (Optional[int], optional): Number of files to add an avg. Defaults to None.
        space (bool, optional): To add a space before the print. Defaults to False.
        prefix (str, optional): To add a prefix before the print. Defaults to "".
        sufix (str, optional): To add a sufix after the print. Defaults to "".
        out_file (Optional[TextIO], optional): To print the line somewere that's not the std bash (keed None for bash). Defaults to None.
    """
    if space:
        print_log("")
    
    if n_files is not None:
        message = f"{n_files:4} files in: {parse_seconds_to_minutes(sec)}."
        message += f" Per document: {parse_seconds_to_minutes(sec / n_files)}"
    else:
        message = f"Time: {parse_seconds_to_minutes(sec)}"

    message = f"{prefix}{message}{sufix}."
    
    if out_file:
        print_log(message, file=out_file)
    else:
        print_log(message)
