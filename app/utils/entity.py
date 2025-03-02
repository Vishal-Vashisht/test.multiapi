from collections import namedtuple

Requests = namedtuple(
    "Requests", [
        "method",
        "query_params",
        "body",
        "path"
    ])
