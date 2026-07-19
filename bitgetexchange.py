import requests

BASE_URL = "https://api.bitget.com"


def get_ticker(symbol):
    url = f"{BASE_URL}/api/v2/mix/market/ticker?symbol={symbol}&productType=USDT-FUTURES"

    response = requests.get(url)

    return response.json()