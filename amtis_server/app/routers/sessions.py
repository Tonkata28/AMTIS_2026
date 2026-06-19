from fastapi import APIRouter, Response
from ..db.store import db
from ..models.user import User, UserLogin
import secrets

from ..services.users_handling import authorize

router = APIRouter()

@router.post("/api/sessions", status_code=201)
def login_user(response: Response, login_info: UserLogin):

    user_id = authorize(login_info)
    cookie = secrets.token_urlsafe(32)
    db["sessions"][cookie] = user_id

    response.set_cookie(
        "authToken",
        cookie,
        httponly=True,
        secure=True,
        samesite="lax",
        path="/",
        max_age=3600,
    )

    return {
        "message": "Успешен вход",
        "email": login_info.email,
        "userId": user_id
    }