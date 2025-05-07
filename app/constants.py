# Constant for app are defined HERE
import logging

SUCESS = "success"
START = "start"
FINSISH = "finish"
ERROR = "error"

ALL_STATUSES = {SUCESS, START, FINSISH, ERROR}

API_PREFIX = "api/v1/"

DATA_TYPE_MAPPING = {
    "string": "VARCHAR",
    "integer": "INTEGER",
    "text": "TEXT",
    "date": "DATE"
}

DEFAULT_COLUMN = {"id": {"type": "Integer", "constraint": "PRIMARY KEY"}}

INITIAL_DATA_TYPES = {'integer': 'Integer', 'real': 'Float', 'text': 'String', 'blob': 'LargeBinary', 'boolean': 'Boolean', 'date': 'Date', 'datetime': 'DateTime', 'timestamp': 'DateTime', 'char': 'String', 'varchar': 'String'}

DTYPE_WITHOUT_LENGTH = {
        "INTEGER",
        "REAL",
        "BLOB",
        "BOOLEAN",
        "DATE",
        "DATETIME",
        "TIMESTAMP",
    }
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


# SYNC
SYNC_ENV = 'pythonanywhere'


# UTILS

MAIN_DB = set(("postgresql", "mysql", "oracle"))
NOT_DELETE_TABLE = set(
    (
        "alembic_version",
        "daily_data_delete",
        "internal_users",
        "task_status",
        "bg_task_response",
        "bg_tasks",
    )
)

POSTGRESQL = "postgresql"

DECORATE_METHODS = set(("get", "post", "delete", "patch", "put", "head"))


# VALIDATOR 
API_PREFIX = "api/v1/"

FILE_SERVICE_CLOUDNARY = "Cloudnary"
