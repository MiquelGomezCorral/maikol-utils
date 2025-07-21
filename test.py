import time
import os
from maikol_utils.print_utils import clear_bash, print_clear_bash, set_logger, print_log
import logging
from logging.handlers import TimedRotatingFileHandler
# ======================================================================================================               
#                                              LOGGER FOR PRINT
# ======================================================================================================

from dataclasses import dataclass, field
@dataclass
class Configuration:
    logs_folder:           str = r"logs"
    logs_path_file: str = fr"{logs_folder}/app.log"

class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG:    "\033[32m",  # green
        logging.INFO:     "\033[34m",  # blue
        logging.WARNING:  "\033[33m",  # yellow-orange
        logging.ERROR:    "\033[31m",  # red
        logging.CRITICAL: "\033[1;31m" # bright red
    }
    RESET = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelno, "")
        record.levelname = f"{color}{record.levelname}{self.RESET}"
        return super().format(record)

os.makedirs(Configuration.logs_folder, exist_ok=True)
file_handler = TimedRotatingFileHandler(
    Configuration.logs_path_file, when="midnight", interval=1, backupCount=7, encoding="utf-8"
)
file_handler.setFormatter(logging.Formatter(
    "%(asctime)s | %(levelname)s: %(message)s", "%Y-%m-%d %H:%M"
))

# Create shared handler with your formatter
handler = logging.StreamHandler()
handler.setFormatter(ColorFormatter(
    "%(asctime)s | %(levelname)s: %(message)s", "%Y-%m-%d %H:%M"
))

# Apply to your logger
logger = logging.getLogger(__name__)
logger.handlers.clear()
logger.propagate = False
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.addHandler(file_handler)

# Also apply to FastAPI and Uvicorn loggers
for name in ["uvicorn", "uvicorn.access", "uvicorn.error"]:
    log = logging.getLogger(name)
    log.handlers.clear()
    log.propagate = False
    log.setLevel(logging.INFO)
    log.addHandler(handler)



set_logger(logger)  
print_log("Line A")
time.sleep(1)
print_log("Line B")
time.sleep(1)
clear_bash(2)   # removes both lines from the terminal
print_log("Clean slate!")


print_log("Loading data...")
time.sleep(1)
print_clear_bash("✔️ Data loaded successfully!", n_lines=1)

"""

>>> print("Line A")
>>> Line A

>>> print("Line B")
>>> Line A
>>> Line B

>>> clear_bash(2) 
>>> 

>>> print("Clean slate!")
>>> Clean state!

>>> print("Loading data...")
>>> Clean state!
>>> Loading data...

>>> print_clear_bash("✔️ Data loaded successfully!", n_lines=1)
>>> Clean state!
>>> ✔️ Data loaded successfully!
"""
