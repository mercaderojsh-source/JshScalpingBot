def confidence_score(
    ema9,
    ema21,
    ema50,
    rsi,
    atr
):
    score = 0

    # -------------------------
    # Trend (0-35)
    # -------------------------

    if ema9 > ema21 > ema50:
        score += 35
    elif ema9 < ema21 < ema50:
        score += 35

    # -------------------------
    # EMA Alignment Strength (0-20)
    # -------------------------

    ema_gap = abs(ema9 - ema50)

    if ema_gap > ema50 * 0.015:
        score += 20
    elif ema_gap > ema50 * 0.010:
        score += 15
    elif ema_gap > ema50 * 0.005:
        score += 10

    # -------------------------
    # RSI (0-20)
    # -------------------------

    if 45 <= rsi <= 55:
        score += 20

    elif 40 <= rsi <= 60:
        score += 15

    elif 35 <= rsi <= 65:
        score += 10

    # -------------------------
    # ATR (0-25)
    # -------------------------

    if atr > 100:
        score += 25

    elif atr > 70:
        score += 20

    elif atr > 50:
        score += 15

    elif atr > 30:
        score += 10

    return min(score, 100)