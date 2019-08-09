from web.errors.general_error import GeneralError


class UnexpectedRole(GeneralError):
    def_status_code = 403
    def_message = "User is not allowed to perform this operation"

    def __init__(
        self, message=def_message, status_code=def_status_code, description=""
    ):
        super().__init__(message, status_code, description)
