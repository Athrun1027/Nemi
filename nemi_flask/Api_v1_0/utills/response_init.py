from werkzeug.exceptions import BadRequest


def success_response(code=200, data=None):
    return {
        "code": code,
        "success": True,
        "data": data
    }


class ProfileError(BadRequest):

    def __init__(self, code=None, message=None):
        super(ProfileError).__init__()
        self.message = message
        self.code = code
