def prepare_api_documentation(app):
    api_config = app.config.get("API_CONFIG", {})
    api_docs = app.config.get("API_DOC")
    deprecated_endpoints = app.config.get("DEPRECATED_ENDPOINTS")
    for api_url, api_data in api_config.items():
        if "paths" not in api_docs:
            api_docs["paths"] = {}

        if (api_data.get("feroute")) or (api_url in deprecated_endpoints):
            continue
        paths = api_docs.get("paths")
        paths[api_url] = {}
        # loop for methods
        methods = api_data.get("methods")
        current_url = paths[api_url]
        end_of_endpoint = api_url.split("/")[-2]
        for method in methods:
            current_url.update({method.lower(): {}})
            api_method = current_url.get(method.lower())
            api_method.update(
                {
                    "summary": f"{method} api for {end_of_endpoint}",
                    "operationId": f"{method}{end_of_endpoint}",
                    "responses": {},
                }
            )
            if api_data.get("is_authenticated"):
                api_method.update({"security": [{"BearerAuth": []}]})

    return api_docs
