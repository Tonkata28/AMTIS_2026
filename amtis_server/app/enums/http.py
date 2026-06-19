from enum import StrEnum


class AcceptStocksFormats(StrEnum):
    JSON = "application/json"
    CSV = "text/csv"
    HTML = "text/html"
    ALL_FILES = "*/*"


class AcceptTeamPhotoFormats(StrEnum):
    png = "image/png"
    jpg = "image/jpeg"
    ALL_FILES = "*/*"