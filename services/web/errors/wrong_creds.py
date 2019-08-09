from web.errors.general_error import GeneralError


class WrongCreds(GeneralError):
    def_status_code = 401
    def_message = "username or password is not correct"

    def __init__(
        self, message=def_message, status_code=def_status_code, description=""
    ):
        super().__init__(message, status_code, description)
