from web.errors.general_error import GeneralError


class JsonMalformed(GeneralError):
    def_status_code = 400
    def_message = "Check json format"

    def __init__(
        self, message=def_message, status_code=def_status_code, description=""
    ):
        super().__init__(message, status_code, description)
