import requests
from decimal import Decimal


CBR_URL = "https://www.cbr-xml-daily.ru/daily_json.js"


class RateFetchError(Exception):
    pass


def fetch_usd_rate():
    try:
        response = requests.get(CBR_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        usd_data = data["Valute"]["USD"]
        return Decimal(str(usd_data["Value"]))
    except Exception as e:
        raise RateFetchError(f"Failed to fetch USD rate: {e}")
