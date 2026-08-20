from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import current_app, request

from ..models.user import User


def create_token(user):
    expires = datetime.now(timezone.utc) + timedelta(hours=current_app.config["JWT_EXPIRY_HOURS"])
    payload = {"sub": str(user.id), "email": user.email, "exp": expires}
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")


def optional_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        request.current_user = None
        header = request.headers.get("Authorization", "")
        if header.startswith("Bearer "):
            token = header.removeprefix("Bearer ").strip()
            try:
                payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
                request.current_user = User.query.get(int(payload["sub"]))
            except jwt.PyJWTError:
                request.current_user = None
        return fn(*args, **kwargs)

    return wrapper
