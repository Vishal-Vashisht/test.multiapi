import os
import sys
import threading
import time
from flask import current_app


def restart_app(app):
    restarts_in = app.config.get("RESTART_TIME")
    thread = threading.Thread(target=sync, args=(restarts_in,app))
    thread.start()
    return {"msg": f"sync process will start in {restarts_in}"}


def sync(restarts_in, app):
    with app.app_context():
        app.block_requests = True
        app.restart_time = time.localtime(time.mktime(time.localtime()) + int(restarts_in))
        app.restarts_in = int(restarts_in)
    time.sleep(int(restarts_in))
    os.execv(sys.executable, ['python'] + sys.argv)
