from pydantic import BaseModel, field_validator, model_validator
from datetime import date
from ..errors.error_codes import Codes
from ..errors.exception_handlers import _err
from ..config import VALID_TRANSACTION_TYPES, VALID_STOCK_TRANSACTION_TYPES



class ReportQuery(BaseModel):
    startDate: date|None = None
    endDate: date|None = None
    stock_type: str|None = None


    @field_validator("stock_type")
    @classmethod
    def validate_stock_type(cls, v: str):
        stripped = v.strip()
        if stripped == "": # is this check required??
            raise _err(Codes.MISSING_REQUIRED_FIELDS, "Stock type must not be empty when given") # return None??
        
        if stripped not in VALID_STOCK_TRANSACTION_TYPES:
            raise _err(Codes.INVALID_VALUE, "Stock type must be a valid type")
        
        return stripped

    @model_validator(mode='after')
    def validate_dates(self):
        if self.endDate is None or self.startDate is None:
            return self
        
        if self.endDate < self.startDate:
            raise _err(Codes.INVALID_VALUE, "End date must be greater or equal to start date")
        
        return self

class ReportTransactionsQuery(ReportQuery):
    item_type: str|None = None

    @field_validator("item_type")
    @classmethod
    def validate_item_type(cls, v: str):
        stripped = v.strip()
        if stripped == "": # is this check required??
            raise _err(Codes.MISSING_REQUIRED_FIELDS, "Stock type must not be empty when given") # return None??
        
        if stripped not in VALID_TRANSACTION_TYPES:
            raise _err(Codes.INVALID_VALUE, "Stock type must be either purchase or sale")
        
        return stripped
    
class ReportStockTransactionsQuery(ReportQuery):
    pass