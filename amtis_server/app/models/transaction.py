from pydantic import BaseModel, field_validator
from ..errors.error_codes import Codes
from ..errors.exception_handlers import _err
from ..config import VALID_CARD_EXPIRATION_DATE_FORMATS, VALID_CARD_CVV_LENGTHS, SUPPORTED_CURRENCIES

from decimal import Decimal
from datetime import datetime

class TransactionInfo(BaseModel):
    amount: Decimal
    cardNumber: str
    cardHolderName: str
    expirationDate: str
    cvv: str

    @field_validator("amount")
    @classmethod
    def validate_amount_greater_than_zero(cls, v: float):
        if v <= 0:
            raise _err(Codes.INVALID_VALUE, "Amount field takes only positive values!")
        
        return v


    @field_validator("cardNumber", "cardHolderName", "expirationDate", "cvv")
    @classmethod
    def validate_required_not_empty(cls, v):
        if v.strip() == "":
            raise _err(Codes.MISSING_REQUIRED_FIELDS, "Required fields must not be empty!")
        
        return v

    @field_validator("cardNumber")
    @classmethod
    def validate_card_number_format(cls, v: str):
        
        if not v.isdigit() or len(v) != 16:
            raise _err(Codes.INVALID_FORMAT, "Card number must be 16 digits!")
        
    
    @field_validator("expirationDate")
    @classmethod
    def validate_expiration_date_format_and_value(cls, v: str):

        for f in VALID_CARD_EXPIRATION_DATE_FORMATS:
            try:
                dt = datetime.strptime(v, f)
            except ValueError:
                pass
            else:

                if dt.year >= 2050:
                    dt = dt.replace(year=dt.year - 100)

                if datetime.now() > dt:
                    raise _err(Codes.INVALID_VALUE, "Card is expired!")

                return dt
            
        else:
            raise _err(Codes.INVALID_FORMAT, "Date must be in valid format!")
        

    @field_validator("cvv")
    @classmethod
    def validate_cvv_format(cls, v: str):
        
        if len(v) not in VALID_CARD_CVV_LENGTHS or not v.isdigit():
            raise _err(Codes.INVALID_FORMAT, "Card CVV code length must be 3 or 4!")
        
        return v
    

class TransactionInfoMultiCurr(TransactionInfo):
    currency: str

    @field_validator("currency")
    @classmethod
    def validate_currency_in_market(cls, v: str):
        
        if v not in SUPPORTED_CURRENCIES:
            raise _err(Codes.INVALID_VALUE, "Invalid market currency!")
        
        return v