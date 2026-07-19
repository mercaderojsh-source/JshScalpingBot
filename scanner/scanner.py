from exchange.bitget import get_ticker


PAIRS = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "XRPUSDT",
    "BGBUSDT"
]


def scan_market():
    market = {}

    for pair in PAIRS:
        data = get_ticker(pair)

        if data["code"] == "00000":
            ticker = data["data"][0]

            market[pair] = {
                "price": float(ticker["lastPr"]),
                "bid": float(ticker["bidPr"]),
                "ask": float(ticker["askPr"]),
                "high": float(ticker["high24h"]),
                "low": float(ticker["low24h"]),
                "change": float(ticker["change24h"]),
                "volume": float(ticker["baseVolume"])
            }

    return market