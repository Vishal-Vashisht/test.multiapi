import dotenv
import os

dotenv.load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")
SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
API_KEY = os.getenv("API_KEY")

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
    }
}
