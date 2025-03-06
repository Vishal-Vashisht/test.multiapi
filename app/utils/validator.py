from .exceptions import ValidationError


def none_validator(entity, fields_exclude: set = set()):

    errors = []
    for key, value in entity._asdict().items():
        if key == "pk":
            key = "id"
        if key in fields_exclude:
            continue
        if not value:
            errors.append({"error": f"{key} is required", "name": key})

    if errors:
        raise ValidationError(errors)


def customize_route(api_route):
    if api_route.startswith("/"):
        api_route = api_route[1:]

    if "api/v1/" in api_route:
        api_route = api_route.replace("api/v1/", " ")

    if not api_route.endswith("/"):
        api_route += "/"
    return api_route.strip()
