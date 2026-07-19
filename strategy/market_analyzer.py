def analyze_market(ema9, ema21, ema50, atr):

    trend = "SIDEWAYS"

    if ema9 > ema21 > ema50:
        trend = "BULLISH"

    elif ema9 < ema21 < ema50:
        trend = "BEARISH"

    volatility = "LOW"

    if atr > 100:
        volatility = "HIGH"

    elif atr > 50:
        volatility = "MEDIUM"

    return {
        "trend": trend,
        "volatility": volatility
    }