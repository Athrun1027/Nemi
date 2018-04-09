from flask import request, current_app, g
from datetime import datetime
from functools import wraps
import jwt

from models import User

from .response_init import ProfileError


def login_require(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get("Nemi-Api-Key", "")
        if not token.startswith("Nemi "):
            raise ProfileError(code=400, message="Please add the token in header and startwith 'Nemi '!")
        try:
            data = jwt.decode(token[5:], current_app.config["SECRET_KEY"])
        except jwt.DecodeError:
            data = None
        if data is None:
            raise ProfileError(code=400, message="Your token is wrong, Please authenticate again!")
        if data["expire"] - datetime.now().timestamp() < 0:
            raise ProfileError(code=400, message="Your token has been expired, Please authenticate again!")
        user = User.query.filter_by(id=data["user_id"]).first()
        if not user:
            raise ProfileError(code=400, message="User not exist!")
        g.login_user = user
        return func(*args, **kwargs)
    return decorated
