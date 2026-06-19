from enum import StrEnum


class SortBy(StrEnum):
    BUY_PRICE = "buyPrice"
    SELL_PRICE = "sellPrice"
    TICKER = "ticker"
    COUNTRY_CODE = "countryCode"


class SortOrder(StrEnum):
    ASC = "asc"
    DESC = "desc"