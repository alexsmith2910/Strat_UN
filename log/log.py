import os
from pathlib import Path
from datetime import datetime

log_path = Path(os.path.dirname(os.path.realpath(__file__))) / "log.txt"


def log_write(text, file_path=log_path):
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # dir_path = Path(sys.path[0]) # Allows a consistent relative path to the main script across all operating systems
    # file_path = dir_path / "log" / "log.txt"
    with open(file_path, "a+") as f:
        f.write(str(datetime.now()) + ": " + str(text) + "\n")


def error_write(description, error, *, file_path=log_path):
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # dir_path = Path(sys.path[0]) # Allows a consistent relative path to the main script across all operating systems
    # file_path = dir_path / "log" / "log.txt"
    with open(file_path, "a+") as f:
        f.write(str(datetime.now()) + ": Error occurred - " + str(description) + ", error message: " + str(
            error) + ", error type: " + str(type(error)) + "\n")
