from typing import Literal
import logging

# ==========================================================================================
#                                       LOGGER
# ==========================================================================================
_logger: logging.Logger | None = None

LogLevel = Literal["debug", "info", "warning", "error", "critical"]
_LOG_LEVELS = ("debug", "info", "warning", "error", "critical") # For runetime use
_base_log_level = "info"

def set_logger(logger: logging.Logger) -> None:
    """Sets a global logger to log all the function print to it

    Args:
        logger (logging.Logger): Logger
    """
    global _logger
    _logger = logger

def get_logger() -> logging.Logger | None:
    """Get the logger instance used in the module

    Returns:
        logging.Logger | None: Logger
    """
    return _logger


def set_base_log_level(base_log_level: LogLevel):
    """Sets the base log level for 'print_log' without spcifying the log level

    Args:
        base_log_level (LogLevel): Log level of logger from logging

    Raises:
        ValueError: If the log level is not a valid one.
    """
    global _base_log_level
    if base_log_level not in _LOG_LEVELS:
        raise ValueError(f"The log level '{base_log_level}' is not in those listed: {_LOG_LEVELS}")
    _base_log_level = base_log_level

def get_base_log_level() -> LogLevel:
    """Get the Module base log levelv

    Returns:
        LogLevel: Module base log levelv
    """
    return _base_log_level

# ==========================================================================================
#                                       Verbose
# ==========================================================================================
_verbose: bool = True
def set_verbose(verbose: bool) -> None:
    """Sets the module verbose to true or false. If false none of the functions that print debug
    lines will print. Yet, the print_... functions like print_separator or print_log will still print.
    Yet, this value can be ignored when calling some functions with parameter verbose.

    Args:
        verbose (bool): Verbose or not
    """
    global _verbose
    _verbose = verbose

def get_verbose(verbose: bool = None) -> bool:
    """Returns general verbose if one is not passed. Else 
    follows function passed verbose. 

    Args:
        verbose (bool, optional): _description_. Defaults to None.

    Returns:
        bool: _description_
    """
    return verbose if verbose is not None else _verbose