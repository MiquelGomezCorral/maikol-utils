from typing import Literal

# ==========================================================================================
#                                       GENERAL
# ==========================================================================================

separators = {
    "separator_short" : "_"*32,
    "separator_normal": "_"*64,
    "separator_long"  : "_"*128,
    "separator_super" : "="*128,
}

colors = {
    "red":    "\033[31m",
    "green":  "\033[32m",
    "yellow": "\033[33m",
    "blue":   "\033[34m",
    "white":  "\033[0m",
}

Colors = Literal["red", "green", "blue", "yellow", "white"]

def print_separator(text: str, sep_type: Literal["SHORT", "NORMAL", "LONG", "SUPER", "START"] = "NORMAL") -> None:
    """Prints a text with a line that separes the bash outputs. The size of this line is controled by sep_type

    Args:
        text (str): Text to print.
        sep_type (Literal['SHORT', 'NORMAL', 'LONG', 'SUPER'], optional): Type of the separation line. Defaults to "NORMAL".
    """
    if sep_type == "SHORT":
        sep = separators["separator_short"]
    elif sep_type == "NORMAL":
        sep = separators["separator_normal"]
    elif sep_type == "LONG":
        sep = separators["separator_long"]
    elif sep_type == "SUPER" or sep_type == "START":
        sep = separators["separator_super"]
    else:
        sep = separator_normal
        print_warn("WARNING: No separator with that label")
    
    if sep_type == "SUPER":
        print(sep)
        print(f"{text:^{len(sep)}}")
        print(sep + "\n")
    elif sep_type == "START":
        print_color(sep + "\n", color="blue")
        print_color(f"{text:^{len(sep)}}\n", color="blue")
        print_color(sep + "\n", color="blue")
    else:
        print(sep)
        print(f"{text:^{len(sep)}}\n")


def print_color(text: str, color: Colors = "white", print_text: bool = True) -> str:
    """Prints the text with a certain color

    Args:
        text (str): Text to print
        color (Literal['red', 'green', 'blue', 'white'], optional): Color to use. Defaults to "white".
        print_text bool: Whether or not to print the color text (if false it will return it)

    Return: 
        str: Text with colors
    """
    if color == "red":
        color = colors["color_red"]
    elif color == "green":
        color = colors["color_green"]
    elif color == "blue":
        color = colors["color_blue"]
    elif color == "yellow":
        color = colors["color_yellow"]
    else:
        color = colors["color_reset"]

    text: str = f"{color}{text}{colors["color_reset"]}"

    if print_text:
        print(f"{text}")

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
    clear_line = " " * 200  # assume max 200 chars per line
    print(f"\r{clear_line}\r{msg}", end="", flush=True)


def clear_bash(n_lines: int = 1) -> None:
    """Cleans the bash output by removing the last n lines.

    Args:
        n_lines (int, optional): Number of lines to remove. Defaults to 1.
    """
    print("\033[F\033[K"*n_lines, end="")  # Move cursor up one line and clear that line

def print_clear_bash(text: str, n_lines: int = 1) -> None:
    """Cleans the bash output by removing the last n lines.

    Args:
        n_lines (int, optional): Number of lines to remove. Defaults to 1.
    """
    clear_bash(n_lines)
    print(text)