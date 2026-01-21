import requests
from decimal import Decimal


CBR_URL = "https://www.cbr-xml-daily.ru/daily_json.js"


def fetch_usd_rate():
    response = requests.get(CBR_URL, timeout=5)
    response.raise_for_status()
    response_json = response.json()
    usd_data = response_json["Valute"]["USD"]
    
    return Decimal(str(usd_data["Value"]))
