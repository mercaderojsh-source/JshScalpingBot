from exchange.bitget import get_candles
from indicators.ema import calculate_ema


def higher_timeframe_trend(pair):
    """
    Determines the higher timeframe trend (5-minute)
    using EMA 9, EMA 21 and EMA 50.
    """

    response = get_candles(pair, granularity="5m")

    if response.get("code") != "00000":
        return "NEUTRAL"

    candles = response["data"]

    closes = [float(c[4]) for c in candles]

    ema9 = calculate_ema(closes, 9)
    ema21 = calculate_ema(closes, 21)
    ema50 = calculate_ema(closes, 50)

    if ema9 > ema21 > ema50:
        return "BUY"

    if ema9 < ema21 < ema50:
        return "SELL"

    return "NEUTRAL"