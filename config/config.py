import os

import dotenv

dotenv.load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")
SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
API_KEY = os.getenv("API_KEY")
ADMIN_MAIL = os.getenv("ADMIN_MAIL")
PASS = os.getenv("PASS")
USERNAME = os.getenv("USERNAME")
RESTART_TIME = os.getenv("restart_time")
DEPLOYED_ENV = os.getenv("DEPLOYED_ENV")
API_CONFIG = {
    "/api/v1/echo/": {
        "methods": set(("POST",)),
        "is_authenticated": False,
        "POST_data": {"body": {"data": {"required": True, "type": "object"}}},
    },
    "/api/v1/trvlr/": {"methods": set(("GET",)), "is_authenticated": False},
    "/api/v1/auth/register/usercart/": {
        "methods": set(("POST",)),
        "is_authenticated": True,
        "POST_data": {
            "body": {
                "name": {"type": "string", "required": True},
                "email": {"type": "string", "required": True},
                "gender": {"type": "string", "required": True},
                "refrence_id": {"type": "integer", "required": False},
            }
        },
    },
    "/api/v1/auth/register/userapp/": {
        "methods": set(("POST",)),
        "is_authenticated": True,
        "POST_data": {
            "body": {
                "name": {"type": "string", "required": True},
                "email": {"type": "string", "required": True},
                "gender": {"type": "string", "required": True},
                "refrence_id": {"type": "integer", "required": False},
            }
        },
    },
    "/api/v1/auth/insert/user-app-post/": {
        "methods": set(("POST",)),
        "is_authenticated": True,
        "POST_data": {
            "body": {
                "name": {"type": "string", "required": True},
                "email": {"type": "string", "required": True},
                "gender": {"type": "string", "required": True},
                "refrence_id": {"type": "integer", "required": False},
            }
        },
    },
    "/api/v1/auth/parallel/": {
        "methods": set(("POST",)),
        "is_authenticated": True,
        "POST_data": {
            "body": {
                "name": {"type": "string", "required": True},
                "email": {"type": "string", "required": True},
                "gender": {"type": "string", "required": True},
                "refrence_id": {"type": "integer", "required": False},
            }
        },
    },
    "/api/v1/sample/": {
        "methods": set(("GET",)),
        "is_authenticated": False,
    },
    "/api/v1/auth/user/login/": {
        "methods": set(("POST",)),
        "is_authenticated": False,
        "POST_data": {
            "body": {
                "username": {"required": True, "type": "string"},
                "password": {"required": True, "type": "string"},
            }
        },
    },
    "/api/v1/tables/async/delete/": {
        "methods": set(("POST",)),
        "is_authenticated": True,
    },
    "/api/v1/tables/sync/delete/": {
        "methods": set(("POST",)),
        "is_authenticated": True,
    },
    "/api/v1/tables/task/info/": {
        "methods": set(("GET",)),
        "is_authenticated": True,
        "GET_data": {
            "query_params": {"process_id": {"type": "string", "required": True}}
        },
    },
    "/api/v1/data/": {
        "methods": set(("GET", "POST")),
        "is_authenticated": True,
        "GET_data": {
            "query_params": {
                "page": {"type": "integer", "required": False},
                "size": {"type": "integer", "required": False},
            }
        },
        "POST_data": {
            "query_params": {
                "page": {"type": "integer", "required": False},
                "size": {"type": "integer", "required": False},
            }
        },
    },
    "/api/v1/entity/": {
        "methods": set(("POST", "GET")),
        "is_authenticated": True,
        "POST_data": {
            "body": {
                "entity_name": {"type": "string", "required": True},
                "entity_alias": {"type": "string", "required": True},
                "columns_config": {
                    "type": "object"
                },
                "relations_config": {
                    "type": "object",
                    "required": False
                },
            }
        },
    },
    "/api/v1/datatypes/": {
        "methods": set(("GET",)),
        "is_authenticated": True,
        "POST_data": {
        },
    },
    "/api/v1/entity/<int:pk>/": {
        "methods": set(("GET",)),
        "is_authenticated": True,
        "GET_data": {}
    },
    "/api/v1/api-config/": {
        "methods": set(("POST",)),
        "is_authenticated": True,
        "POST_data": {
            "body": {
                "name": {
                    "type": "string",
                    "description": "The name of the API configuration",
                    "minLength": 1,
                    "required": True,
                },
                "entity": {
                    "type": "integer",
                    "description": "The entity ID related to the API",
                    "required": True,
                },
                "route": {
                    "type": "string",
                    "description": "The route for the API",
                    "minLength": 1,
                    "required": True,
                    "example": "product-getitems/"
                },
                "method": {
                    "type": "string",
                    "enum": ["get", "post", "put", "delete"],
                    "description": "The HTTP method for the API",
                    "required": True,
                },
                "description": {
                    "type": "string",
                    "description": "A description of the API",
                    "minLength": 1,
                    "required": True,
                },
                "response": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of response fields",
                    "required": True,
                },
                "body": {
                    "type": "object",
                    "description": "The request body for the API",
                    "required": False,
                    "properties": {
                        "payload_key": {
                            "type": "object",
                            "properties": {
                                "type": {
                                    "type": "string",
                                    "required": True
                                },
                                "required": {
                                    "type": "boolean"
                                }
                            }
                        }
                    }
                },
                "query_params": {
                    "type": "object",
                    "description": "Query parameters for the API",
                    "required": False,
                    "properties": {
                        "param": {
                            "type": "object",
                            "properties": {
                                "type": {
                                    "type": "string",
                                    "required": True
                                },
                                "required": {
                                    "type": "boolean"
                                }
                            }
                        }
                    }
                },
                "is_authenticated": {
                    "type": "boolean",
                    "description": "Whether the API requires authentication",
                    "required": True,
                },
            }
        },
    },
    "/api/v1/sync/": {
        "methods": set(("POST",)),
        "is_authenticated": True,
        "POST_data": {},
    },
    # Frontend
    "/home/": {"methods": set(("GET",)), "is_authenticated": True, "feroute": True},
    "/home/data/": {
        "methods": set(("GET",)),
        "is_authenticated": True,
        "feroute": True,
    },
    # login screen
    "/": {"methods": set(("GET",)), "is_authenticated": False, "feroute": True},
    "/documentation/": {
        "methods": set(("GET",)),
        "is_authenticated": False,
        "feroute": True,
    },
    "/doc/": {"methods": set(("GET",)), "is_authenticated": True},
}

# if static folder changes define it in this list
# STATIC_CONFIG = {
#     "folders": set((
#         "static",
#     ))
# }

API_DOC = {
    "openapi": "3.0.0",
    "info": {
        "title": "API Documentation",
        "description": "API documentation for developers.",
        "version": "1.0.0",
    },
    "components": {
        "securitySchemes": {
            "BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
        }
    },
}


DEPRECATED_ENDPOINTS = set(("/api/v1/trvlr/",))
