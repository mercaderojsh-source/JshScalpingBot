from exchange.bitget import get_candles

from indicators.ema import calculate_ema


def higher_timeframe_trend(pair):

    response = get_candles(
        pair,
        granularity="5m"
    )

    if response.get("code") != "00000":
        return {
            "trend": "NEUTRAL",
            "ema9": 0,
            "ema21": 0,
            "ema50": 0
        }

    candles = response["data"]

    closes = [float(c[4]) for c in candles]

    ema9 = calculate_ema(closes, 9)
    ema21 = calculate_ema(closes, 21)
    ema50 = calculate_ema(closes, 50)

    if ema9 > ema21 > ema50:
        trend = "BUY"

    elif ema9 < ema21 < ema50:
        trend = "SELL"

    else:
        trend = "NEUTRAL"

    return {
        "trend": trend,
        "ema9": ema9,
        "ema21": ema21,
        "ema50": ema50
    }