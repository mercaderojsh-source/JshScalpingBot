import os
import time
import json
import hmac
import base64
import hashlib
import requests

from config import MARGIN_MODE

BASE_URL = "https://api.bitget.com"

API_KEY = os.getenv("BITGET_API_KEY")
API_SECRET = os.getenv("BITGET_API_SECRET")
API_PASSPHRASE = os.getenv("BITGET_API_PASSPHRASE")


# ==========================================================
# Public Endpoints
# ==========================================================

def get_ticker(symbol):
    url = (
        f"{BASE_URL}/api/v2/mix/market/ticker"
        f"?symbol={symbol}&productType=USDT-FUTURES"
    )

    response = requests.get(url)

    return response.json()


def get_contract_info(symbol):

    url = f"{BASE_URL}/api/v2/mix/market/contracts"

    params = {
        "symbol": symbol,
        "productType": "USDT-FUTURES"
    }

    response = requests.get(
        url,
        params=params
    )

    return response.json()


def get_symbol_rules(symbol):

    response = get_contract_info(symbol)

    if response.get("code") != "00000":
        return None

    if not response.get("data"):
        return None

    contract = response["data"][0]

    return {
        "symbol": contract["symbol"],
        "min_size": float(contract["minTradeNum"]),
        "size_step": float(contract["sizeMultiplier"]),
        "price_decimals": int(contract["pricePlace"]),
        "size_decimals": int(contract["volumePlace"]),
        "max_leverage": int(contract["maxLever"]),
    }


def get_candles(
    symbol,
    granularity="1m",
    limit="100"
):
    url = f"{BASE_URL}/api/v2/mix/market/candles"

    params = {
        "symbol": symbol,
        "granularity": granularity,
        "limit": limit,
        "productType": "USDT-FUTURES"
    }

    response = requests.get(
        url,
        params=params
    )

    return response.json()


# ==========================================================
# Authentication
# ==========================================================

def _sign(
    timestamp,
    method,
    request_path,
    query_string="",
    body=""
):
    if query_string:
        message = (
            f"{timestamp}"
            f"{method.upper()}"
            f"{request_path}"
            f"?{query_string}"
            f"{body}"
        )
    else:
        message = (
            f"{timestamp}"
            f"{method.upper()}"
            f"{request_path}"
            f"{body}"
        )

    signature = hmac.new(
        API_SECRET.encode(),
        message.encode(),
        hashlib.sha256
    ).digest()

    return base64.b64encode(signature).decode()


def _private_get(
    request_path,
    params=None
):
    params = params or {}

    query_string = "&".join(
        f"{k}={v}"
        for k, v in params.items()
    )

    timestamp = str(int(time.time() * 1000))

    headers = {
        "ACCESS-KEY": API_KEY,
        "ACCESS-SIGN": _sign(
            timestamp,
            "GET",
            request_path,
            query_string
        ),
        "ACCESS-TIMESTAMP": timestamp,
        "ACCESS-PASSPHRASE": API_PASSPHRASE,
        "locale": "en-US"
    }

    response = requests.get(
        BASE_URL + request_path,
        headers=headers,
        params=params
    )

    return response.json()


def _private_post(
    request_path,
    body=None
):
    body = body or {}

    body_json = json.dumps(
        body,
        separators=(",", ":")
    )

    timestamp = str(int(time.time() * 1000))

    headers = {
        "ACCESS-KEY": API_KEY,
        "ACCESS-SIGN": _sign(
            timestamp,
            "POST",
            request_path,
            body=body_json
        ),
        "ACCESS-TIMESTAMP": timestamp,
        "ACCESS-PASSPHRASE": API_PASSPHRASE,
        "Content-Type": "application/json",
        "locale": "en-US"
    }

    print("\n========== BITGET REQUEST ==========")
    print("Endpoint :", request_path)
    print("Body     :", body)

    response = requests.post(
        BASE_URL + request_path,
        headers=headers,
        data=body_json
    )

    try:
        data = response.json()
    except Exception:
        print(response.text)
        raise

    print("Response :", data)
    print("====================================\n")

    return data


# ==========================================================
# Private Endpoints
# ==========================================================

def get_futures_account():

    return _private_get(
        "/api/v2/mix/account/accounts",
        {
            "productType": "USDT-FUTURES"
        }
    )


def get_positions():

    return _private_get(
        "/api/v2/mix/position/all-position",
        {
            "productType": "USDT-FUTURES",
            "marginCoin": "USDT"
        }
    )


def place_market_order(
    symbol,
    side,
    size,
    trade_side="open"
):

    body = {
        "symbol": symbol,
        "productType": "USDT-FUTURES",
        "marginMode": MARGIN_MODE,
        "marginCoin": "USDT",
        "side": side,
        "tradeSide": trade_side,
        "orderType": "market",
        "size": str(size)
    }

    return _private_post(
        "/api/v2/mix/order/place-order",
        body
    )


def set_leverage(
    symbol,
    leverage,
    hold_side="long"
):

    body = {
        "symbol": symbol,
        "productType": "USDT-FUTURES",
        "marginCoin": "USDT",
        "leverage": str(leverage),
        "holdSide": hold_side
    }

    return _private_post(
        "/api/v2/mix/account/set-leverage",
        body
    )

# ==========================================================
# Position TP / SL
# ==========================================================

def place_position_tpsl(
    symbol,
    hold_side,
    stop_loss=None,
    take_profit=None
):
    """
    Attach Stop Loss and/or Take Profit to an existing futures position.

    hold_side:
        long
        short
    """

    body = {
        "symbol": symbol,
        "productType": "USDT-FUTURES",
        "marginCoin": "USDT",
        "holdSide": hold_side,
    }

    # ---------------- STOP LOSS ----------------

    if stop_loss is not None:
        body["stopLossTriggerPrice"] = str(stop_loss)
        body["stopLossTriggerType"] = "mark_price"

        # Execute at MARKET when triggered
        body["stopLossExecutePrice"] = str(stop_loss)

    # ---------------- TAKE PROFIT ----------------

    if take_profit is not None:
        body["stopSurplusTriggerPrice"] = str(take_profit)
        body["stopSurplusTriggerType"] = "mark_price"

        # Execute at MARKET when triggered
        body["stopSurplusExecutePrice"] = str(take_profit)

    print("\n========== POSITION TP/SL ==========")
    print(body)

    return _private_post(
        "/api/v2/mix/order/place-pos-tpsl",
        body
    )


def place_stop_loss(
    symbol,
    hold_side,
    stop_loss
):
    """
    Attach Stop Loss to an existing position.
    """

    print("\n===== PLACE STOP LOSS =====")

    return place_position_tpsl(
        symbol=symbol,
        hold_side=hold_side,
        stop_loss=stop_loss
    )


def place_take_profit(
    symbol,
    hold_side,
    take_profit
):
    """
    Attach Take Profit to an existing position.
    """

    print("\n===== PLACE TAKE PROFIT =====")

    return place_position_tpsl(
        symbol=symbol,
        hold_side=hold_side,
        take_profit=take_profit
    )