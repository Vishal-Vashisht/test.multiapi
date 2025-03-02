from app.constants import logger
import time


class ApplyAuthentication:

    def __init__(self, app, request):

        self.__api_key = app.config.get("API_KEY")
        self.__request = request

    def _validate_auth(self):

        auth_header = self.__request.headers.get("authorization")

        if not auth_header:
            auth_header = self.__request.cookies.get("access_token")

        if not self.__api_key or not auth_header or auth_header[:6] != "Bearer":
            return {"Unauthorized": "Provide the valid authorization headers"}, 401

        token = auth_header[7:]
        if not token or token != self.__api_key:
            return {"Unauthorized": "Provide the valid authorization headers"}, 401

        return None, None

    def test_function(self):
        logger.info("I'm a test function"),
        return None, None


class BlockRequest:

    def __init__(self, app):

        self._block_request = app.block_requests
        self._restart_time = app.restart_time
        self._restarts_in = app.restarts_in

    def _block_inc_request(self):
        if self._block_request:
            print(self._restart_time)
            current_time = time.localtime()
            time_diff = time.mktime(self._restart_time) - time.mktime(current_time)

            hours = int(time_diff // 3600)
            minutes = int((time_diff % 3600) // 60)
            seconds = int(time_diff % 60)
            return {
                "msg": "Application is preparing for sync, further calls, are restricted till then, will let you once application is available.",
                "time_left_to_restart": f"Application will restart in {hours} hours, {minutes} minutes, and {seconds} seconds"
            }, 503

        return None, None
