from fastapi import APIRouter, Response, Depends
from ..models.user import User, UpdateCredentials
from ..services.users_handling import register_user
from typing import Annotated
from ..dependencies.cookies import get_user_id
from ..services.users_handling import change_password, change_email, change_country_code
from ..db.store import db

router = APIRouter()

@router.post("/api/users", status_code=201)
def post_register_user(user: User):
    user_id = register_user(user)
    
    return {
        "message": "Потребителят е регистриран успешно",
        "email": f"{user.email}",
        "userId": f"{user_id}"
    }


@router.patch("/api/users/me")
def patch_me(
    response: Response,
    credentials: UpdateCredentials,
    user_id: Annotated[str, Depends(get_user_id)]
    ):

        
    if credentials.newPassword is not None:
        change_password(user_id, credentials)

    if credentials.email is not None:
        change_email(user_id, credentials)

    if credentials.countryCode is not None:
        change_country_code(user_id, credentials)

    user = db["users"].get(user_id)

    db["sessions"] = {cookie: u_id for cookie, u_id in db["sessions"].items() if u_id != user_id}
    
    response.delete_cookie(
        "authToken",
        path="/"
    )

    return {
        "message": "Промените са записани успешно",
        "email": user.email,
        "countryCode": user.country_code
    }

