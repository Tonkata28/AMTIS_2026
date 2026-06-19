import requests
from ..config import team_id, API_TOKEN, MARKET_BASE_URL
from ..db.store import db


class MarketClient():

    def __init__(self, base_url: str = MARKET_BASE_URL):
        self.base_url = base_url.rstrip("/")


    def authenticate_session(self) -> dict:
        """
        Interacts with the outside server, from which it gets a session id. The id is stored in the internal DB, where it is used for future requests.
        Returns the session id.
        """
        body = {
            "API_KEY": team_id,
            "API_SECRET": API_TOKEN
        }

        response = requests.post(f"{self.base_url}/auth", json=body)
        response.raise_for_status()
        db["session_id"] = response.json()["sessionId"]

        print(db["session_id"])

        return response.json()


    def _get(self, path: str):
        headers = {
            "Authorization": db["session_id"]
        }

        response = requests.get(f"{self.base_url}{path}", headers=headers)
        response.raise_for_status()

        return response.json()

    def get_stocks_prices(self) -> list[dict]:
        
        return self._get("/prices")

    def get_stocks_v2(self):

        return self._get(f"/v2/stocks")

    def get_prices_v2(self) -> list[dict]:
        
        return self._get("/v2/prices")
    
    def get_fx_rates(self) -> list[dict]:

        return self._get("/rates")
    
    def get_market_regulations(self) -> dict:

        return self._get("/v2/regulations")
    

market = MarketClient()