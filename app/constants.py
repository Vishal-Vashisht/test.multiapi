# Constant for app are defined HERE
import logging

SUCESS = "success"
START = "start"
FINSISH = "finish"
ERROR = "error"

ALL_STATUSES = {SUCESS, START, FINSISH, ERROR}

DATA_TYPE_MAPPING = {
    "string": "VARCHAR",
    "integer": "INTEGER",
    "text": "TEXT",
    "date": "DATE"
}

DEFAULT_COLUMN = {"id": {"type": "Integer", "constraint": "PRIMARY KEY"}}

# Create a logger object
logger = logging.getLogger(__name__)

# Create a handler for logging to console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Set the level for the handler

# Create a formatter for the log output
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(console_handler)
logger.setLevel(level=logging.INFO)
