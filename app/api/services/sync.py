import os
import sys
import threading
import time
from app.initial_tasks.pythonanywhere_restart import restart_script
from app import messages as msg, constants as const

logger = const.logger


def restart_app(app):
    restarts_in = app.config.get("RESTART_TIME")
    thread = threading.Thread(target=sync, args=(restarts_in, app))
    thread.start()
    return {"msg": f"{msg.SYNC_PROCESS_START} {restarts_in}"}


def sync(restarts_in, app):
    with app.app_context():
        app.block_requests = True
        app.restart_time = time.localtime(
            time.mktime(time.localtime()) + int(restarts_in)
        )
        app.restarts_in = int(restarts_in)
        ENV = app.config.get("DEPLOYED_ENV")

    time.sleep(int(restarts_in))
    if ENV == const.SYNC_ENV:
        logger.info("Restart Initiated for pythonanywhere")
        restart_script()
    else:
        os.execv(sys.executable, ["python"] + sys.argv)
