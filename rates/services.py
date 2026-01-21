import requests
from decimal import Decimal
from environs import Env


env = Env()
env.read_env()

cbr_url = env.str("CBR_URL")

class RateFetchError(Exception):
    pass


def fetch_usd_rate():
    try:
        response = requests.get(cbr_url, timeout=5)
        response.raise_for_status()
        data = response.json()
        usd_data = data["Valute"]["USD"]
        return Decimal(str(usd_data["Value"]))
    except Exception as e:
        raise RateFetchError(f"Failed to fetch USD rate: {e}")
