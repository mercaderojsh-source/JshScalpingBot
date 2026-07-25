from exchange.bitget import get_candles
from indicators.ema import calculate_ema


def higher_timeframe_trend(pair):
    # Fetch 15m candles for a true Higher Timeframe trend anchor
    response = get_candles(
        pair,
        granularity="15m"
    )

    if response.get("code") != "00000" or not response.get("data"):
        return {
            "trend": "NEUTRAL",
            "ema9": 0,
            "ema21": 0,
            "ema50": 0
        }

    candles = response["data"]
    closes = [float(c[4]) for c in candles]

    if len(closes) < 50:
        return {
            "trend": "NEUTRAL",
            "ema9": 0,
            "ema21": 0,
            "ema50": 0
        }

    ema9 = calculate_ema(closes, 9)
    ema21 = calculate_ema(closes, 21)
    ema50 = calculate_ema(closes, 50)
    price = closes[-1]

    # Standardized output to "BULLISH", "BEARISH", or "NEUTRAL"
    if ema9 > ema21 > ema50 and price > ema50:
        trend = "BULLISH"
    elif ema9 < ema21 < ema50 and price < ema50:
        trend = "BEARISH"
    else:
        trend = "NEUTRAL"

    return {
        "trend": trend,
        "ema9": ema9,
        "ema21": ema21,
        "ema50": ema50
    }
