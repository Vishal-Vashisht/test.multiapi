class ValidationError(Exception):

    def __init__(self, msg, code=None, *args, **kwargs):
        super().__init__(*args)

        self._msg = msg
        self._code = code or 400
