import os
import time
import hmac
import base64
import hashlib
import requests

BASE_URL = "https://api.bitget.com"

API_KEY = os.getenv("BITGET_API_KEY")
API_SECRET = os.getenv("BITGET_API_SECRET")
API_PASSPHRASE = os.getenv("BITGET_API_PASSPHRASE")


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


def _sign(timestamp, method, request_path, query_string="", body=""):
    if query_string:
        message = f"{timestamp}{method.upper()}{request_path}?{query_string}{body}"
    else:
        message = f"{timestamp}{method.upper()}{request_path}{body}"

    signature = hmac.new(
        API_SECRET.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256
    ).digest()

    return base64.b64encode(signature).decode()


def _private_get(request_path, params=None):
    params = params or {}

    query_string = "&".join(f"{k}={v}" for k, v in params.items())

    timestamp = str(int(time.time() * 1000))

    headers = {
        "ACCESS-KEY": API_KEY,
        "ACCESS-SIGN": _sign(timestamp, "GET", request_path, query_string),
        "ACCESS-TIMESTAMP": timestamp,
        "ACCESS-PASSPHRASE": API_PASSPHRASE,
        "locale": "en-US"
    }

    url = BASE_URL + request_path

    response = requests.get(url, headers=headers, params=params)

    return response.json()


def get_futures_account():
    return _private_get(
        "/api/v2/mix/account/accounts",
        {
            "productType": "USDT-FUTURES"
        }
    )


def get_positions():
    """
    Returns all open USDT perpetual futures positions.
    """
    return _private_get(
        "/api/v2/mix/position/all-position",
        {
            "productType": "USDT-FUTURES",
            "marginCoin": "USDT"
        }
    )