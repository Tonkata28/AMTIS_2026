from ..db.store import db
from ..errors.exceptions import AppError
from ..errors.error_codes import Codes
from typing import Annotated
from fastapi import Cookie


def get_user_id(
        cookie: Annotated[str|None, Cookie(alias="authToken")] = None
) -> str:

    if cookie is None:
        raise AppError(Codes.AUTH_REQUIRED)

    if cookie.startswith("authToken="):  # just in case the user which sends it type authToken="token" instead of just token
        cookie = cookie.replace("authToken=", "", 1)

    user_id = db["sessions"].get(cookie)
    if user_id is None:
        raise AppError(Codes.AUTH_REQUIRED)
    
    return user_id