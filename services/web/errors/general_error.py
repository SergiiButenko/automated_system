class GeneralError(Exception):
    def_code = 400
    def_message = "Invalid request"

    def __init__(self, message=def_message, code=def_code, description=""):
        Exception.__init__(self)
        self.message = message
        self.code = code
        self.description = description

    def to_dict(self):
        return dict(message=self.message, code=self.code, description=self.description)
