schema_columns = {
    "type": "object",
    "additionalProperties": {
        "type": "object",
        "properties": {
            "type": {
                "type": "string",
                "enum": ["string", "date", "integer"],
            },
            "length": {"type": "number", "minimum": 0},
            "constraint": {
                "type": "string",
                "enum": ["default", "unique", "PRIMARY KEY"],
            },
        },
        "required": ["type"],
    },
}


realtion_schema = {
    "type": "object",
    "additionalProperties": {
        "type": "object",
        "properties": {
            "entity": {
                "type": "integer",
            },
            "column": {"type": "string"},
            "ref_column": {"type": "string"},
        },
        "required": ["column", "entity", "ref_column"],
    },
}


# APi Config VALidator

API_CONFIG_BODY_VALIDATOR = {
    "type": "object",
    "additionalProperties": {
        "type": "object",
        "properties": {
            "required": {
                "type": "integer",
            },
            "type": {"type": "string"},
        },
        "required": ["required", "type"],
    },
}

API_CONFIG_QUERY_PARAMS_VALIDATOR = {
    "type": "object",
    "additionalProperties": {
        "type": "object",
        "properties": {
            "required": {
                "type": "integer",
            },
            "type": {"type": "string"},
        },
        "required": ["required", "type"],
    },
}
