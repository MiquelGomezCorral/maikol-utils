import os
import json
from typing import Any

from .print_utils import print_warn

def save_json(save_path: str, content: Any):
    """
    Saves a Python object as a JSON file.

    Args:
        save_path (str): Full path including file name to save the JSON.
        content (Any): The content to save (must be JSON-serializable).

    Returns:
        Any: The original content.
    """
    print(f"Saving output at {save_path}...")
    
    # Extra safety for empty paths
    dir_path = os.path.dirname(save_path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)

    with open(save_path, "w", encoding="utf-8") as out_json:
        json.dump(content, out_json, indent=4)
    
    return content

def load_json(save_path: str) -> Any:
    """
    Loads JSON content from a file. Returns an empty dict if the file does not exist.

    Args:
        save_path (str): Full path including file name to read the JSON from.

    Returns:
        Any: The loaded content, or an empty dict if the file does not exist.
    """
    if not os.path.exists(save_path):
        print_warn(f"NO FILE AT {save_path}. Returning empty dict...")
        return dict()

    print(f"Loading output from {save_path}...")
    with open(save_path, "r", encoding="utf-8") as out_json:
        content = json.load(out_json)
    
    return content




def check_dirs_existance(directories: list[str]) -> None:
    """
    Checks if all specified directories exist.

    Args:
        directories (list[str]): List of directory paths to check.

    Raises:
        KeyError: If any of the directories do not exist.
    """
    missing = [d for d in directories if not os.path.exists(d)]
    if missing:
        raise KeyError(f"Some paths were not found: {missing}")


def make_dirs(directories: list[str]) -> None:
    """
    Creates the specified directories if they do not already exist.

    Args:
        directories (list[str]): List of directory paths to create.
    """
    for directory in directories:
        os.makedirs(directory, exist_ok=True)