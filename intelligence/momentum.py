def momentum_score(trend_strength, atr_percent):
    """
    Momentum Score (0-100)

    Trend Strength : 80 points
    ATR            : 20 points
    """

    # -----------------------
    # Trend (0-80)
    # -----------------------
    trend_points = (trend_strength / 20) * 80

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

    return round(trend_points + atr_points, 1)