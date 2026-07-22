def analyze_market(ema9, ema21, ema50, atr):

    # -------------------------
    # Trend
    # -------------------------

    if ema9 > ema21 > ema50:
        trend = "BULLISH"
    elif ema9 < ema21 < ema50:
        trend = "BEARISH"
    else:
        trend = "SIDEWAYS"

    # -------------------------
    # EMA Alignment Strength
    # -------------------------

    ema_gap = abs(ema9 - ema50)

    if ema_gap > ema50 * 0.015:
        trend_strength = "VERY_STRONG"
    elif ema_gap > ema50 * 0.008:
        trend_strength = "STRONG"
    elif ema_gap > ema50 * 0.004:
        trend_strength = "MEDIUM"
    else:
        trend_strength = "WEAK"

    # -------------------------
    # ATR Quality
    # -------------------------

    if atr > 100:
        volatility = "HIGH"
    elif atr > 50:
        volatility = "MEDIUM"
    else:
        volatility = "LOW"

    # -------------------------
    # Market Quality Score
    # -------------------------

    quality = 0

    if trend != "SIDEWAYS":
        quality += 40

    if trend_strength == "VERY_STRONG":
        quality += 35
    elif trend_strength == "STRONG":
        quality += 25
    elif trend_strength == "MEDIUM":
        quality += 15

    if volatility == "HIGH":
        quality += 25
    elif volatility == "MEDIUM":
        quality += 15

    return {
        "trend": trend,
        "trend_strength": trend_strength,
        "volatility": volatility,
        "quality": quality
    }