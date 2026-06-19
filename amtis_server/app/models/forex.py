from pydantic import BaseModel, Field, model_validator, field_validator
from decimal import Decimal
from ..errors.exception_handlers import _err
from ..errors.error_codes import Codes


class ForexQueryBase(BaseModel):
    amount: Decimal
    source: str = Field(alias="from")
    to: str

    @field_validator("amount")
    @classmethod
    def validate_amout_positive(cls, v: int):
        if v <= 0:
            raise _err(Codes.INVALID_VALUE, "Amount must be a positive number")
        
        return v

    @model_validator(mode="after")
    def validate_from_to_exist_when_amount(self):
        if self.amount is None:
            return self
        
        if self.to is None and self.source is None:
            raise _err(Codes.MISSING_REQUIRED_FIELDS, "From/to must exist when amount does")
        
        return self


class ForexQuery(ForexQueryBase):
    source: str|None = Field(alias="from", default=None)
    to: str|None = None
    amount: Decimal|None = None
    

class ForexPurchaseQuery(ForexQueryBase):
    pass