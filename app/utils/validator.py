from .exceptions import ValidationError


def none_validator(entity, fields_exclude: set = set()):

    errors = []
    for key, value in entity._asdict().items():
        if key in fields_exclude:
            continue
        if not value:
            errors.append({"error": f"{key} is required", "name": key})

    if errors:
        raise ValidationError(errors)
