def momentum_score(
    ema_gap,
    trend_strength,
    atr_percent
):
    """
    Score momentum from 0-100
    """

    score = 0

    # EMA expansion
    if ema_gap > 0.30:
        score += 40
    elif ema_gap > 0.20:
        score += 30
    elif ema_gap > 0.10:
        score += 20
    elif ema_gap > 0.05:
        score += 10

    # Trend strength
    score += min(trend_strength * 3, 30)

    # Volatility
    if atr_percent > 0.50:
        score += 30
    elif atr_percent > 0.30:
        score += 20
    elif atr_percent > 0.15:
        score += 10

    return min(score, 100)