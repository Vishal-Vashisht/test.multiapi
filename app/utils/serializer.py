from copy import deepcopy

from jsonschema import Draft7Validator

from app import messages as msg

from .exceptions import ValidationError


def serialize_response(dataset, response_fields, model):
    resp = {}
    if isinstance(dataset, list):
        results = []
        for res in dataset:
            temp_data = {}
            _dataset = res.serialize()
            if response_fields[0] == "*":
                temp_data = _dataset
            else:
                for field in response_fields:
                    temp_data[field] = _dataset.get(field)
            results.append(temp_data)

        resp["results"] = results

    if isinstance(dataset, dict):
        if response_fields[0] == "*":
            return dataset

        for field in response_fields:
            resp[field] = dataset.get(field)

    if isinstance(dataset, model):
        dataset = dataset.serialize()
        if response_fields[0] == "*":
            return dataset
        for field in response_fields:
            resp[field] = dataset.get(field)
    return resp


def deserialize(config, payload):

    copy_config = deepcopy(config)
    local_config = deepcopy(config)
    schema = {"type": "object", "required": [], "properties": copy_config}

    cleaned_payload = _cleand_payload(local_config, payload)
    validate_spaces(cleaned_payload)

    for key, value in local_config.items():
        key = key.lower()
        if value.get("required"):
            schema["required"].append(key)
        elif not payload.get(key):
            schema["properties"].pop(key, None)
    _valid_args(schema, cleaned_payload)
    return cleaned_payload


def _valid_args(schema, payload):

    bool_to_string(schema)
    validator = Draft7Validator(schema)
    errors = []
    for e in validator.iter_errors(payload):
        path = e.message.split(" ")[0][1:-1]
        if e.path:
            path = e.path[0]
        errors.append({"name": path, "error": e.message})

    if errors:  
        raise ValidationError(errors)


def _cleand_payload(config, payload):

    cleaned_payload = {}
    for key, value in config.items():
        key = key.lower()
        # Process only those keys which are defined in config.
        if key in payload:
            cleaned_payload[key] = payload.get(key)
        if value.get("arg_name") and key in payload:
            # if arg_name which is actuall column name in config
            # and payload contain the key of that arg replace it with orginal key
            _val = cleaned_payload.pop(key, "")
            cleaned_payload.update({value.get("arg_name"): _val})

    if "id" in payload:
        cleaned_payload["id"] = payload.get("id")
    if "pk" in payload:
        cleaned_payload["pk"] = payload.get("pk")

    return cleaned_payload


def validate_spaces(cleaned_payload):

    for key, values in cleaned_payload.items():

        if " " in key:
            raise ValidationError(msg=f"'{key}'{msg.SERIALIZER_KEY_CONTAIN_SPACES}")
        if isinstance(values, dict):
            validate_spaces(values)


def bool_to_string(schema):

    for key, val in schema.items():

        if isinstance(val, bool):
            schema[key] = str(val).lower()
        elif isinstance(val, dict):
            bool_to_string(val)

# method for refrence
# def serialize_response(dataset, response_fields, model):
#     resp = {}
#     if isinstance(dataset, list):
#         results = []
#         for res in dataset:
#             temp_data = {}
#             for column in res.__table__.columns:
#                 column_name = str(column).split(".")[-1]
#                 if response_fields[0] == "*":
#                     temp_data
#                 elif column_name in response_fields:
#                     temp_data[column_name] = getattr(res, column_name)
#             results.append(temp_data)
#         resp["results"] = results
