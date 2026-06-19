from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.errors.error_codes import ERRORS
from app.errors.exceptions import AppError

from pydantic_core import PydanticCustomError
from typing import LiteralString


def _err(error_type: LiteralString, additional_info: LiteralString):
    return PydanticCustomError(error_type, additional_info)


def _response(code: str) -> JSONResponse:
    """Single source of truth for what an error response looks like."""
    spec = ERRORS[code]
    return JSONResponse(
        status_code=spec.status,
        content={"error_code": spec.code, "message": spec.message},
    )


async def app_error_handler(request: Request, exc: Exception):
    assert isinstance(exc, AppError)
    return _response(exc.spec.code)


def _classify_pydantic_error(err_type: str) -> str:
    # 1. If a validator raised PydanticCustomError with one of our codes, use it.
    if err_type in ERRORS:
        return err_type

    # 2. The one case validators can't intercept: a required field was absent.
    if err_type == "missing":
        return "MISSING_REQUIRED_FIELDS"
    
    # 3. If there is a format exception -> Convert to INVALID_FORMAT
    if err_type.endswith("_type") or err_type.endswith("_parsing") or err_type == "value_error":
        return "INVALID_FORMAT"
    
    # 4. Anything else means Pydantic's built-in machinery rejected it
    #    (wrong type, bad JSON, etc.) — we didn't write a custom validator
    #    for that case, so it falls into a generic bucket.
    return "INVALID_REQUEST"


async def validation_exception_handler(request: Request, exc: Exception):
    assert isinstance(exc, RequestValidationError)
    errors = exc.errors()
    code = (
        _classify_pydantic_error(errors[0].get("type", ""))
        if errors
        else "INVALID_REQUEST"
    )
    return _response(code)


# ── Handler 3: anything we forgot to catch (defensive) ─────────
async def unhandled_exception_handler(request: Request, exc: Exception):
    # Log the real exception here for debugging — but never leak it to the client
    return _response("INTERNAL_ERROR")


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)