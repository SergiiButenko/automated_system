from web.errors.general_error import GeneralError


class UnableToRefresh(GeneralError):
    def_status_code = 403
    def_message = "Unable to refresh token"

    def __init__(
        self, message=def_message, status_code=def_status_code, description=""
    ):
        super().__init__(message, status_code, description)
