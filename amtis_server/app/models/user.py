from pydantic import BaseModel, field_validator, EmailStr, model_validator
from ..errors.error_codes import Codes
from ..db.store import db
from ..utils.validation import validate_country_code_util
from ..errors.exception_handlers import _err
from decimal import Decimal
from dataclasses import dataclass

def validate_password_rules(v: str) -> str:

    if not v.strip():
        raise _err(Codes.MISSING_REQUIRED_FIELDS, "Empty password value!")
            
    if any([
        len(v) < 6,
        not any(e.isupper() for e in v),
        not any(e.islower() for e in v),
        not any(e.isdigit() for e in v),
        all(e.isalnum() for e in v)
    ]):
        raise _err(Codes.INVALID_VALUE, "Password doesn't match required rules!")
    
    return v


def validate_email_not_empty(v: str) -> str:
    if isinstance(v, str) and not v.strip(): # possible error for expecting invalid_value
            raise _err(Codes.MISSING_REQUIRED_FIELDS, "Empty email value!")
    return v



class User(BaseModel):
    email: EmailStr
    password: str
    countryCode: str


    @field_validator("email", mode="before")
    @classmethod
    def email_not_empty(cls, v):
        return validate_email_not_empty(v)
    

    @field_validator("countryCode")
    @classmethod
    def validate_country_code(cls, val: str):

        return validate_country_code_util(val)


    @field_validator("password")
    @classmethod
    def validate_password(cls, val: str):

        return validate_password_rules(v=val)
        
    
    @model_validator(mode="before")
    @classmethod
    def validate_email_not_in_password(cls, data):
        if not isinstance(data, dict):
            return data

        email = data.get("email")
        password = data.get("password")

        if isinstance(email, str) and isinstance(password, str):
            if email and email.lower() in password.lower():
                raise _err(Codes.VALIDATION_FAILED, "Password must not contain email!")

        return data
    

class UserLogin(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str):

        if not v:
            raise _err(Codes.MISSING_REQUIRED_FIELDS, "Password must not be empty!")
        
        return v

@dataclass
class UserBalance:
    currency: str
    amount: Decimal


@dataclass
class UserStock:
    currency: str
    ticker: str
    countryCode: str
    quantity: int


@dataclass
class UserTransaction:
    type: str
    ticker: str
    countryCode: str
    quantity: int
    price: Decimal
    timestamp: str


@dataclass
class StoredUser:
    id: str
    email: str
    balances: list[UserBalance]
    stocks: list[UserStock]
    transactions: list[UserTransaction]
    country_code: str
    password_hash: str


class UpdateCredentials(BaseModel):
    email: EmailStr|None = None
    countryCode: str|None = None
    currentPassword: str|None = None
    newPassword: str|None = None
    password: str|None = None

    @field_validator("email", mode="before")
    @classmethod
    def email_not_empty(cls, v: str):
        return validate_email_not_empty(v)

    @field_validator("currentPassword")
    @classmethod
    def reject_empty_old_password(cls, val: str):
        if not val.strip():
            raise _err(Codes.MISSING_REQUIRED_FIELDS, "Empty password value!")
            
        return val
    

    @field_validator("countryCode")
    @classmethod
    def validate_country_code(cls, val: str):

        return validate_country_code_util(val)

    @model_validator(mode="after")
    def validate_fields_exist(self):
        if all([
            self.newPassword is None,
            self.email is None,
            self.countryCode is None
        ]):
            raise _err(Codes.INVALID_FORMAT, "At least one field must be provided") # possible wrong error

        return self