import dotenv
import os

dotenv.load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")
SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
API_KEY = os.getenv("API_KEY")
ADMIN_MAIL = os.getenv("ADMIN_MAIL")
PASS = os.getenv("PASS")
USERNAME = os.getenv("USERNAME")

API_CONFIG = {
    "/api/v1/convert/": {
        "methods": set(("POST",)),
        "is_authenticated": False
    },
    "/api/v1/trvlr/": {
        "methods": set(("GET",)),
        "is_authenticated": False
    },
    "/api/v1/auth/register/usercart/": {
        "methods": set(("POST",)),
        "is_authenticated": True,
    },
    "/api/v1/auth/register/userapp/": {
        "methods": set(("POST",)),
        "is_authenticated": True,
    },
    "/api/v1/auth/insert/user-app-post/": {
        "methods": set(("POST",)),
        "is_authenticated": True,
    },
    "/api/v1/auth/parallel/": {
        "methods": set(("POST",)),
        "is_authenticated": True,
    },
    "/api/v1/sample/": {
        "methods": set(("GET",)),
        "is_authenticated": False,
    },
    "/api/v1/auth/user/login/": {
        "methods": set(("POST",)),
        "is_authenticated": False,
    },
    "/api/v1/tables/delete/": {
        "methods": set(("POST",)),
        "is_authenticated": True,
    },
    "/api/v1/tables/task/info/": {
        "methods": set(("GET",)),
        "is_authenticated": True,
    },
    "/api/v1/data/": {
        "methods": set(("GET",)),
        "is_authenticated": True,
        "query_params": {
            "page": {
                "type": "integer"
            },
            "size": {
                "type": "integer"
            }
        }
    },
}
