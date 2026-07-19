def confidence_score(
    ema9,
    ema21,
    ema50,
    rsi,
    atr
):
    score = 0

    # Trend
    if ema9 > ema21 > ema50:
        score += 30

    elif ema9 < ema21 < ema50:
        score += 30

    # RSI
    if 40 <= rsi <= 60:
        score += 20
    elif rsi < 35 or rsi > 65:
        score += 10

    # ATR
    if atr > 50:
        score += 20
    elif atr > 30:
        score += 10

    # EMA Separation
    distance = abs(ema9 - ema21)

    if distance > 20:
        score += 15
    elif distance > 10:
        score += 10

    # Bonus
    if atr > 70:
        score += 15

    return min(score, 100)