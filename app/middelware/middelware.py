from app.constants import logger


class ApplyAuthentication():

    def __init__(self, app, request):

        self.__api_key = app.config.get("API_KEY")
        self.__request = request

    def _validate_auth(self):

        auth_header = self.__request.headers.get("authorization")

        if not auth_header:
            auth_header = self.__request.cookies.get('access_token')

        if not self.__api_key or not auth_header or \
                auth_header[:6] != "Bearer":
            return {
                "Unauthorized": "Provide the valid authorization headers"
            }, 401

        token = auth_header[7:]
        if not token or token != self.__api_key:
            return {
                "Unauthorized": "Provide the valid authorization headers"
            }, 401

        return None, None

    def test_function(self):
        logger.info("I'm a test function"),
        return None, None
