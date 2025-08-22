import os
import json
import shutil
from typing import Any, Callable
from pathlib import Path
from natsort import natsorted

from .print_utils import print_status, print_warn, print_error, print_log
from .config import get_verbose
# ==========================================================================================
#                                       JSON 
# ==========================================================================================
def save_json(save_path: str, content: Any, verbose: bool = None):
    """
    Saves a Python object as a JSON file.

    Args:
        save_path (str): Full path including file name to save the JSON.
        content (Any): The content to save (must be JSON-serializable).
        verbose (bool): Wether to print or not. If not set, will follow general config.

    Returns:
        Any: The original content.
    """
    if get_verbose(verbose):
        print_log(f"Saving output at {save_path}...")
    
    # Extra safety for empty paths
    dir_path = os.path.dirname(save_path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)

    with open(save_path, "w", encoding="utf-8") as out_json:
        json.dump(content, out_json, indent=4)
    
    return content


def load_json(save_path: str, verbose: bool = None) -> Any:
    """
    Loads JSON content from a file. Returns an empty dict if the file does not exist.

    Args:
        save_path (str): Full path including file name to read the JSON from.
        verbose (bool): Wether to print or not. If not set, will follow general config.

    Returns:
        Any: The loaded content, or an empty dict if the file does not exist.
    """
    if not os.path.exists(save_path):
        if get_verbose(verbose):
            print_warn(f"NO FILE AT {save_path}. Returning empty dict...")
        return dict()

    if get_verbose(verbose):
        print_log(f"Loading output from {save_path}...")

    with open(save_path, "r", encoding="utf-8") as out_json:
        content = json.load(out_json)
    
    return content


# ==========================================================================================
#                                       DIRECTORIES
# ==========================================================================================
def check_dirs_existance(dir_or_dirs: str | list[str]) -> None:
    """
    Checks if all specified dir_or_dirs exist.

    Args:
        dir_or_dirs (str | list[str]): Directory or list of directory paths to check.

    Raises:
        KeyError: If any of the dir_or_dirs do not exist.
    """
    if isinstance(dir_or_dirs, str):
        dir_or_dirs = [dir_or_dirs]

    missing = [d for d in dir_or_dirs if not os.path.exists(d)]
    if missing:
        raise KeyError(f"Some paths were not found: {missing}")


def make_dirs(dir_or_dirs: str | list[str]) -> None:
    """
    Creates the specified dir_or_dirs if they do not already exist.

    Args:
        dir_or_dirs (str | list[str]): Directory or list of directory paths to create.
    """
    if isinstance(dir_or_dirs, str):
        dir_or_dirs = [dir_or_dirs]

    for directory in dir_or_dirs:
        os.makedirs(directory, exist_ok=True)


def clear_directories(dir_or_dirs: str | list[str], remove_folder: bool = False, verbose: bool = None):
    """Clears out each directory in `dir_or_dirs`. 
    If dir_or_dirs is just a directory (string) just clear that one. Else
    loop over all the directories and clean them all.
    If `remove_folder` is True, the entire folder is removed; otherwise only its contents are deleted.

    Args:
        dir_or_dirs (str | list[str]): Path/s to directories.
        remove_folder (bool): If True, delete the folder itself.
        verbose (bool): Wether to print or not. If not set, will follow general config.

    Notes:
        - If the folder does not exist or is not a directory, a message is printed.
        - This function is intended for temporary folders or cleanup tasks.
    """
    if isinstance(dir_or_dirs, str): 
        dir_or_dirs = [dir_or_dirs]

    for d in dir_or_dirs:
        p = Path(d)
        if not p.exists() or not p.is_dir():
            if get_verbose(verbose):
                print_warn(f"{d!r} not found or not a dir")
            continue

        if remove_folder:
            shutil.rmtree(p)
        else:
            for child in p.iterdir():
                (shutil.rmtree(child) if child.is_dir() else child.unlink())

        if get_verbose(verbose):
            print_log(f"{'Removed' if remove_folder else 'Cleared'} {d}")



# ==========================================================================================
#                                       LIST DIR
# ==========================================================================================
def list_dir_files(path: str, max_files: int = None, recursive: bool = False, nat_sorting: bool = True, absolute_path: bool = True) -> tuple[list[str], int]:
    """Given a path and (optionally) the number of max files, loads a sorted list of
    all the files that are found in that folder (with at most max_files if passed).
    Then returns tha list of files and the number of those that have been loaded.
    If max_files is less than the actual number of files, it's okey. 
    By default it sorts the files as the os / humans would do. If you need python sorting
    use nat_sorting = False

    Args:
        path (str): Path to the folder
        max_files (int, optional): Max number of files to load. Defaults to None.
        recursive (bool, optional): If false just return the root level files in the path. If true list ALL files in any sub folder. Default to False.
        nat_sorting (bool, optional): Whether or not to sort the files as the os (naturally humans) do. Defualt to True.
        absolute_path (bool, optional): Whether or not return the absolute path (path + file names) or just the file names from path (files names). Defualt to True.
            absolute_path = True: 
                >>> path = "./test" -> ["./test/file1","./test/file2","./test/folder/file3"]
            absolute_path = False: 
                >>> path = "./test" -> ["/file1","/file2","/folder/file3"]


    Returns:
        tuple[list[str], int]: The list of file names and the number of those that have been listed
    """
    if not os.path.isdir(path):
        print_error(f"NO SUCH DIRECTORY: {path!r}")
        return [], 0
    
    # ========= GET ALL THE FILES =========
    if not recursive:
        aux = os.listdir(path)
        dir_list = [
            os.path.join(path, entry)
            for entry in aux
            if os.path.isfile(os.path.join(path, entry))
        ]
            
    else: # Loop over each subfile and add the whole path
        dir_list = []
        for dirpath, _, filenames in os.walk(path):
            for f in filenames:
                full_path = os.path.join(dirpath, f)
                dir_list.append(full_path)

    # ========= SORTHING =========
    if nat_sorting:
        dir_list = natsorted(dir_list)
    else:
        dir_list = list(sorted(dir_list))

    # ========= REMOVE ABS PATH =========
    if not absolute_path:
        dir_list = [os.path.relpath(f, path) for f in dir_list]


    # ========= CUT THE LIST =========
    dir_list = dir_list[:max_files]
    n_files = len(dir_list)

    return dir_list, n_files


def change_file_ext(path: str, new_extension: str) -> str:
    """
    Changes the extension of a given file path.

    Args:
        path (str): The original file path.
        new_extension (str): The new file extension (with or without a leading dot: '.txt' or 'txt').

    Returns:
        str: The file path with the new extension.
    """
    if not new_extension.startswith("."):
        new_extension = "." + new_extension
        
    return str(Path(path).with_suffix(new_extension))


def manage_temp_files(call_key: str, temp_folder_path: str, function: Callable, _verbose: bool = None, *args, **kwargs) -> Any:
    """Manages temporal files for saving certain function outputs.

    When called for the first time, it will execute the function and save the file
    into a temporal folder. If by any reason (crash) this is called again with the
    same key, instead of executing process again, it will load the previous saved output

    Args:
        call_key (str): Unique as possible key for the call
        temp_folder_path (str): path to the temporal files folder
        to_execute (Callable): Function / process to be executed. Will pass all extra parameters
        *args: Positional arguments to pass to the function
        **kwargs: Keyword arguments to pass to the function

    Returns:
        Any: Whatever the process returns

    Examples:
    >>> for i in range(10):
    >>>     manage_temp_files(
    >>>         i,                     # call_key
    >>>         "./temp",              # temp_folder_path
    >>>         document_to_llm,       # function
    >>>         llm_client,            # *args -> function arg 1
    >>>         pages[i],              # *args -> function arg 2
    >>>         verbose=False          # **kwargs -> function keyword arg
    >>>     )
    """
    temp_path = os.path.join(temp_folder_path, f"{call_key}.json")

    if os.path.exists(temp_path):
        if get_verbose(_verbose):
            print_log(f" - Skiping '{call_key}': Temp file found at '{temp_path}'")
        return load_json(temp_path, verbose=False)

    if get_verbose(_verbose):
        print_status(f" - Executing '{function.__name__}' for '{call_key}'...")
    result = function(*args, **kwargs)

    save_json(temp_path, result, verbose=False)
    return result

