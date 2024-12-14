from .middelware import ApplyAuthentication
from flask import request
from app.constants import logger


def _url_rule_to_authenticate(app):

    static_config = app.config.get("STATIC_CONFIG", {})
    api_config = app.config.get("API_CONFIG", {})

    static_folders = static_config.get("folders", set(("static",)))
    method = request.method
    url_rule = str(request.url_rule)

    split_url_rule = url_rule.split("/", maxsplit=2)
    static_path = None
    if split_url_rule and len(split_url_rule) >= 2:
        static_path = split_url_rule[1]

    if static_folders and static_path in static_folders:
        return False, None

    if not api_config:
        return "Not Found", 404

    logger.info("url %s method %s", url_rule, method)
    if url_rule not in api_config:
        logger.info("url rule not found")
        return "Resource Not found", 404

    url_in_api_config = api_config.get(url_rule, {})

    supported_methods = url_in_api_config.get("methods", set())

    if method not in supported_methods:
        logger.info("Supported method not found")
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
