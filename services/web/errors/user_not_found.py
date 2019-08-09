from web.errors.general_error import GeneralError


class UserNotFound(GeneralError):
    def_status_code = 401
    def_message = "User not found"

    def __init__(
        self, message=def_message, status_code=def_status_code, description=""
    ):
        super().__init__(message, status_code, description)
