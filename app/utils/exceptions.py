class ValidationError(Exception):

    def __init__(self, msg, code=None, *args, **kwargs):
        super().__init__(*args)

        self._msg = msg
        self._code = code or 400
        self._FORMAT_EXCEPTION = ValidationError.__FORMAT_EXCEPTION(self._msg, self._code)

    @staticmethod
    def __FORMAT_EXCEPTION(msg, code):
        if isinstance(msg, list):
            return {"errors": msg}

        return {"errors": [{"error": msg, "code": code}]}, code
