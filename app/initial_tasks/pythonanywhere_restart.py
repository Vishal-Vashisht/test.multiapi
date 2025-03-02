import os

import dotenv
import requests

from app.constants import logger

dotenv.load_dotenv()

username = "vashisht"
token = os.getenv("PY_TOKEN")
domain = os.getenv("DOMAIN")


def restart_script():
    try:
        url = f"https://www.pythonanywhere.com//api/v0/user/{username}/webapps/{domain}/reload/"
        headers = {"Authorization": "Token {token}".format(token=token)}
        res = requests.request(method="POST", url=url, headers=headers)
        logger.info("response %s", res.json())
    except Exception as e:
        logger.info("py exception:- %s", str(e))
