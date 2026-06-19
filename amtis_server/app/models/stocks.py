from pydantic import BaseModel, field_validator, model_validator, Field
from typing import Optional
from ..utils.validation import validate_country_code_util
from ..errors.exception_handlers import _err
from ..errors.error_codes import Codes
from decimal import Decimal

from ..enums.stocks import SortBy, SortOrder

class StocksFilter(BaseModel):
    ticker: Optional[str] = None
    countryCode: Optional[str] = None
    minBuyPrice: Optional[float] = None
    maxBuyPrice: Optional[float] = None
    minSellPrice: Optional[float] = None
    maxSellPrice: Optional[float] = None
    sortBy: Optional[str] = None
    sortOrder: Optional[str] = None

    @field_validator("countryCode")
    @classmethod
    def validate_country_code(cls, val: str):

        return validate_country_code_util(val)
    
    # CAN REMOVE FIELD VALIDATORS IN FUTURE AND CHECK IF ERROR TYPE = enum
    @field_validator("sortBy")
    @classmethod
    def validate_sort_by(cls, val: str):

        if val not in SortBy:
            raise _err(Codes.INVALID_VALUE, "Invalid sortBy value!")
        
        return val
    

    @field_validator("sortOrder")
    @classmethod
    def validate_sort_order(cls, val: str):

        if val not in SortOrder:
            raise _err(Codes.INVALID_VALUE, "Invalid sortOrder value!")
        
        return val


    @model_validator(mode="after")
    def validate_filter_model(self):

        if self.minBuyPrice and self.maxBuyPrice and self.minBuyPrice > self.maxBuyPrice:
            raise _err(Codes.INVALID_VALUE, "Minimum buy price must be less than or equal to maximum buy price!")

        if self.minSellPrice and self.maxSellPrice and self.minSellPrice > self.maxSellPrice:
            raise _err(Codes.INVALID_VALUE, "Minimum sell price must be less than or equal to maximum sell price!")
        
        if self.sortBy is None and self.sortOrder is not None:
            raise _err(Codes.MISSING_REQUIRED_FIELDS, "Sort order can not exist when no sorting criteria is provided!")

        return self
    

class StockTransactionBase(BaseModel):
    ticker: str
    quantity: int = Field(strict=True)

    @field_validator("ticker")
    @classmethod
    def validate_ticker_not_empty(cls, v: str):
        if v.strip() == "":
            raise _err(Codes.MISSING_REQUIRED_FIELDS, "Required field ticker is empty!")
        
        return v
    
    @field_validator("quantity")
    @classmethod
    def validate_quantity_positive(cls, v: int):
        if v <= 0:
            raise _err(Codes.INVALID_VALUE, "Quantity must be a positive number!")
        return v
    


class BuyStockRequest(StockTransactionBase):
    pass


class SellStockRequest(StockTransactionBase):
    pass


class StockTransactionResponseProperties(BaseModel):
    ticker: str
    countryCode: str
    buyPrice: float   
    sellPrice: float


class StockTransactionResponseBase(BaseModel):
    stock: StockTransactionResponseProperties


class SellStockResponse(StockTransactionResponseBase):
    pass


class BuyStockResponse(StockTransactionResponseBase):
    pass


class StockTransactionMultiCurrencyResponseProperties(StockTransactionResponseProperties):
    currency: str
    name: str


class StockTransactionResponseMultiCurrencyBase(BaseModel):
    stock: StockTransactionMultiCurrencyResponseProperties


class SellStockMultiCurrencyResponse(StockTransactionResponseMultiCurrencyBase):
    pass


class BuyStockMultiCurrencyResponse(StockTransactionResponseMultiCurrencyBase):
    pass


class TransactionStocksResult(BaseModel):
    ticker: str
    countryCode: str
    buyPrice: float
    sellPrice: float


class BuyStocksResult(TransactionStocksResult):
    pass


class SellStocksResult(TransactionStocksResult):
    pass


class TransactionMultiCurrResult(TransactionStocksResult):
    currency: str
    name: str


class BuyStockMultiCurrencyResult(TransactionMultiCurrResult):
    pass


class SellStockMultiCurrencyResult(TransactionMultiCurrResult):
    pass


class StockTransactionMultiCurrencyRequest(StockTransactionBase):
    price: Decimal


    @field_validator("price")
    @classmethod
    def validate_price_positive(cls, v):

        if v <= Decimal('0'):
            raise _err(Codes.INVALID_VALUE, "Price must be a positive floating point number")
        
        return v


class BuyStockMaxPriceRequest(StockTransactionMultiCurrencyRequest):
    pass


class SellStockMinPriceRequest(StockTransactionMultiCurrencyRequest):
    pass