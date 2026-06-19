from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from app.config import team_id, user_id_1, user_name_1, PROJECT_ROOT
from ..db.store import db
from typing import Annotated
from ..dependencies.headers import validate_accept_header_team_photo
from ..enums.http import AcceptTeamPhotoFormats


router = APIRouter()

@router.get("/api/team")
def get_team_info():

    return {
        "sessionId": db["session_id"],
        "teamId": f"{team_id}",
        "participants": [
            {
                "id": f"{user_id_1}",
                "name": f"{user_name_1}"
            }
        ]
    }


@router.get("/api/team/photo")
def get_team_photo():
    return FileResponse(PROJECT_ROOT / "static" / "team-photo.jpg", media_type="image/jpeg")


@router.get("/api/team/photo/after")
def get_team_photo_after(
    accept: Annotated[str|None, Depends(validate_accept_header_team_photo)]
):
    match accept:
        case AcceptTeamPhotoFormats.jpg:
            return FileResponse(PROJECT_ROOT / "static" / "team-photo-after.jpg", media_type=AcceptTeamPhotoFormats.jpg)
        
        case _:
            return FileResponse(PROJECT_ROOT / "static" / "team-photo-after.png", media_type=AcceptTeamPhotoFormats.png)