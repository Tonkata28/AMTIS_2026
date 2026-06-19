from pydantic import BaseModel, field_validator, Field
from ..errors.exception_handlers import _err
from ..errors.error_codes import Codes
from ..config import SUPPORTED_REGULATION_TYPES


class RegulationFilterQuery(BaseModel):
    type:str|None = None
    is_applicable_to_me: bool|None = None

    @field_validator("is_applicable_to_me", mode="before")
    @classmethod
    def validate_is_applicable_to_me_valid_bool(cls, v: str):

        if not isinstance(v, str):
            raise _err(Codes.INVALID_FORMAT, "Is_applicable_to_me must be a string from json")

        if not v.lower() in ["true", "false"]:
            raise _err(Codes.INVALID_VALUE, "Is applicable to me must be a valid boolean")
        
        return v.lower() == "true"

    @field_validator("type")
    @classmethod
    def validate_type_value(cls, v: str):

        if v.strip() == "":
            raise _err(Codes.MISSING_REQUIRED_FIELDS, "Type field must not be empty!") # maybe just return None??
        
        if v not in SUPPORTED_REGULATION_TYPES:
            raise _err(Codes.INVALID_VALUE, "Regulation type is not supported!")
        
        return v