"""
All messages mus be defined HERE
"""

# Controller -> Field -> purpose

# Api config

API_CONF_ENTITY_NOT_EXISTS = "Entity not exists"
API_CONF_NAME_EXISTS = "Name already exists"
API_CONF_ROUTE_EXISTS = "Route already exists"

API_CONF_DEFAULT_DESCRIPTION = "Entitys attributes will be used as default payload if no payload defined.\n\t"
API_CONF_FIELD_ARG_NOT_MATCH = "field name or arg_name did not match attribute defined for field."
# DYNAMIC APIS
DYNAMIC_PK_REQUIRED = "pk is required field"
DYNAMIC_API_CONF_NOT_EXIST = "Api config not exists"
DYNAMIC_MODEL_DEF_NOT_EXIST = "Model defination not found"


# ENTITY
ENTITY_COLUMN_NOT_EXIST = "Column not exist, in refrence table remove this relation for proceeding further."
ENTITY_COLUMN_NOT_EXIST_IN_CONFIG = "Column not found in column config"
ENTITY_TABLE_NOT_EXIST = "Table not ex ist, remove this relation for proceeding further"
ENTITY_ALIAS_REQUIRED = "entity alias is required"
ENTITY_NAME_REQUIRED = "entity name is required"
ENTITY_COL_CONFIG_REQUIRED = "column config is reuired"
ENTITY_CONFIG_NOT_VALID = "Config is not valid"
ENTITY_ALREADY_EXISTS = "Entity already exists"

# SYNC

SYNC_PROCESS_START = "sync process will start in"


# UTILS
GENERAL_ERROR = "Something went wrong we are try to fix this."
SERIALIZER_KEY_CONTAIN_SPACES = "contain spaces, a key must not contain keys"


# MIDDELWARE
NOT_FOUND = "Not Found"
RES_NOT_FOUND = "Resource Not found"
METHOD_NOT_SUPPORTED = "HTTP Method Not supported"
UNAUTHORIZED_HEADER = "Provide the valid authorization headers"
SYNC_PREPARE = "Application is preparing for sync, further calls, are restricted till then, will let you once application is available."