from fastapi import APIRouter, Query, Depends
from typing import Annotated

router = APIRouter()

@router.get("/health")
def get_status():
    return {
        "status": "ok"
    }