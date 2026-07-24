def momentum_score(
    trend_strength,
    atr_percent,
    ema9,
    ema21,
    ema50,
    price
):
    """
    Momentum Score (0-100)

    Trend Strength : 60 points
    ATR            : 20 points
    Entry Timing   : 20 points
    """

    # -----------------------
    # Trend (0-60)
    # -----------------------
    trend_points = (trend_strength / 20) * 60

    # -----------------------
    # ATR (0-20)
    # Tuned from your Railway logs
    # -----------------------
    if atr_percent >= 0.10:
        atr_points = 20
    elif atr_percent >= 0.08:
        atr_points = 16
    elif atr_percent >= 0.06:
        atr_points = 12
    elif atr_percent >= 0.04:
        atr_points = 8
    elif atr_percent >= 0.02:
        atr_points = 4
    else:
        atr_points = 0

    # --------------------------
    # Entry Timing (0-20)
    # --------------------------
    distance = abs(price - ema9) / price * 100

    if distance <= 0.05:
        entry_points = 20
    elif distance <= 0.10:
        entry_points = 16
    elif distance <= 0.20:
        entry_points = 12
    elif distance <= 0.30:
        entry_points = 8
    elif distance <= 0.50:
        entry_points = 4
    else:
        entry_points = 0

    return round(
        trend_points +
        atr_points +
        entry_points,
        1
    )