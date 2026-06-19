from ..errors.error_codes import Codes
from ..errors.exception_handlers import _err


def validate_country_code_util(val: str):

    if not val.strip():
        raise _err(Codes.MISSING_REQUIRED_FIELDS, "Empty country code value!")

    if len(val) != 2 or not all(c.isalpha() for c in val):
        raise _err(Codes.INVALID_FORMAT, "Country code length must have a length of 2!")
    
    return val
