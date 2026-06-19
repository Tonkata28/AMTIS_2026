from dotenv import load_dotenv
from pathlib import Path
from currency_converter import CurrencyConverter
import os

load_dotenv("credentials.env")

team_id = os.getenv("API_KEY")

if not team_id:
    raise ValueError("API_KEY must not be empty or None")

API_TOKEN = os.getenv("API_TOKEN")

if not API_TOKEN:
    raise ValueError("API_TOKEN must not be empty or None")

user_id_1 = "273556"
user_name_1 = "Antonio Simeonov"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MARKET_BASE_URL = "https://it.az-moga.bg/market"

STOCK_FIELDS_V1 = ["ticker", "name", "countryCode", "buyPrice", "sellPrice"]
STOCK_FIELDS_V2 = ["ticker", "name", "countryCode", "currency", "buyPrice", "sellPrice"]

VALID_CARD_EXPIRATION_DATE_FORMATS = ["%m/%Y", "%m/%y"]
VALID_CARD_CVV_LENGTHS = [3,4]

converter = CurrencyConverter()
SUPPORTED_CURRENCIES = converter.currencies
SUPPORTED_REGULATION_TYPES = ["full-ban", "amount-based"]
VALID_TRANSACTION_TYPES = ["stock", "currency"]
VALID_STOCK_TRANSACTION_TYPES = ["purchase", "sale"]