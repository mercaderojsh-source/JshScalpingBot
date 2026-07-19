import requests

BASE_URL = "https://api.bitget.com"


def get_ticker(symbol):
    url = f"{BASE_URL}/api/v2/mix/market/ticker?symbol={symbol}&productType=USDT-FUTURES"

    response = requests.get(url)

    return response.json()


def get_candles(symbol, granularity="1m", limit="100"):
    url = f"{BASE_URL}/api/v2/mix/market/candles"

    params = {
        "symbol": symbol,
        "granularity": granularity,
        "limit": limit,
        "productType": "USDT-FUTURES"
    }

    response = requests.get(url, params=params)

    return response.json()