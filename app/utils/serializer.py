from jsonschema import Draft7Validator
from .exceptions import ValidationError
from copy import deepcopy


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

    copy_config = config.copy()
    schema = {
        "type": "object",
        "required": [],
        "properties": config
    }

    cleaned_payload = _cleand_payload(copy_config, payload)

    for key, value in config.items():
        if value.get("required"):
            schema["required"].append(key)
        elif not payload.get(key):
            schema["properties"].pop(key, None)
    _valid_args(schema, cleaned_payload)
    return cleaned_payload


def _valid_args(schema, payload):

    validator = Draft7Validator(schema)

    errors = []
    for e in validator.iter_errors(payload):
        errors.append({"name": e.path[0], "error": e.message})

    if errors:
        raise ValidationError(errors)


def _cleand_payload(config, payload):

    cleaned_payload = {}
    for key, value in config.items():
        if key in payload:
            cleaned_payload[key] = payload.get(key)

    return cleaned_payload


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