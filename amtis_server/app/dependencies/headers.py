from typing import Annotated
from fastapi import Header

from ..errors.error_codes import Codes
from ..errors.exceptions import AppError

from ..enums.http import AcceptStocksFormats, AcceptTeamPhotoFormats


def validate_accept_header_format_stocks(
        accept: Annotated[str|None, Header()] = None
) -> str|None:
    
    if accept not in AcceptStocksFormats and accept is not None:
        raise AppError(Codes.UNSUPPORTED_FORMAT)
    
    return accept


def validate_accept_header_team_photo(
        accept: Annotated[str|None, Header()] = None
) -> str|None:
    
    if accept not in AcceptTeamPhotoFormats and accept is not None:
        raise AppError(Codes.UNSUPPORTED_FORMAT)
    
    return accept