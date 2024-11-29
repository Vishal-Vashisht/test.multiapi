from .middelware import ApplyAuthentication
from flask import request


def _url_rule_to_authenticate(app):

    api_config = app.config.get("API_CONFIG")
    if not api_config:
        return "Not Found", 404

    method = request.method
    url_rule = str(request.url_rule)

    print("url", url_rule, method, "method")
    if url_rule not in api_config:
        return "Resource Not found", 404

    url_in_api_config = api_config.get(url_rule, {})

    supported_methods = url_in_api_config.get("methods", set())

    if method not in supported_methods:
        return {
            "Invalid Method": "HTTP Method Not supported"
        }, 404

    is_authenticated = url_in_api_config.get("is_authenticated", True)

    if is_authenticated:
        return True, None

    return False, None


def before_request_middelware(app):

    atuh_middelware_inst = ApplyAuthentication(app, request)
    auth_middelware_list = set((atuh_middelware_inst._validate_auth,))
    simple_middelware_list = set()

    response, status = _url_rule_to_authenticate(app)

    if response and status:
        return response, status

    if response is True and not status:
        for middelware in auth_middelware_list:

            response, status = middelware()

            if response:
                return response, status

    for middelware in simple_middelware_list:

        response, status = middelware()

        if response:
            return response, status


def register_middelware(app):

    @app.before_request
    def apply_before_request():
        return before_request_middelware(app)
