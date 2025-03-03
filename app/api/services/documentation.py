from copy import deepcopy
import re

body = {
    "requestBody": {
        "required": "true",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {},
                }
            }
        },
    }
}

path_types = {"int": "integer", "str": "string"}
bool_map = {"true": True, "false": False}


def prepare_api_documentation(app):
    api_config = app.config.get("API_CONFIG", {})
    api_docs = app.config.get("API_DOC")
    deprecated_endpoints = app.config.get("DEPRECATED_ENDPOINTS")
    for api_url, api_data in api_config.items():
        if "paths" not in api_docs:
            api_docs["paths"] = {}

        if (api_data.get("feroute")) or (api_url in deprecated_endpoints):
            continue

        # Search path params
        pattern = r"<(\w+):(\w+)>"
        path_matches = re.findall(pattern, api_url)

        api_data.setdefault("path_params", {})
        path_params = api_data.get("path_params")
        if path_matches:
            for match in path_matches:
                type_part, name_part = match
                path_params[name_part] = type_part
                api_url = api_url.replace(f"<{type_part}:{name_part}>", f"{{{name_part}}}")

        paths = api_docs.get("paths")
        paths[api_url] = {}
        # loop for methods
        methods = api_data.get("methods")
        current_url = paths[api_url]
        end_of_endpoint = api_url.split("/")[-2]
        group = api_data.get("group", "Default")

        for method in methods:
            current_url.update({method.lower(): {}})
            api_method = current_url.get(method.lower())
            api_method.update(
                {
                    "tags": [group],
                    "operationId": f"{method}{end_of_endpoint}",
                    "responses": {},
                }
            )
            if method not in set(("GET", "HEAD")):
                api_method.update(deepcopy(body))

            api_method.update({"parameters": []})
            doc_params = api_method.get("parameters", [])
            default_summary = f"{method} api for {end_of_endpoint}"
            summary = default_summary

            if path_params:
                for name, value in path_params.items():
                    doc_params.append(
                        {
                            "name": name,
                            "in": "path",
                            "required": True,
                            "schema": {"type": path_types.get(value, value)},
                        }
                    )

            if api_data.get("is_authenticated"):
                api_method.update({"security": [{"BearerAuth": []}]})

            if f"{method}_data" in api_data:
                method_data = api_data.get(f"{method}_data", {})
                summary = method_data.get("summary", default_summary)
                if "body" in method_data and method_data.get("body"):
                    props = (
                        api_method.get("requestBody", {})
                        .get("content", {})
                        .get("application/json", {})
                        .get("schema", {})
                        .get("properties", {})
                    )
                    props.update(method_data.get("body", {}))

                if "query_params" in method_data and method_data.get("query_params"):
                    method_params = method_data.get("query_params", {})
                    for param_name, param_value in method_params.items():

                        doc_params.append(
                            {
                                "name": param_name,
                                "in": "query",
                                "required": bool_map.get(param_value.get("required",""), False),
                                "schema": {"type": param_value.get("type", "string")},
                            }
                        )

            api_method.update({"summary": summary})
    return api_docs
