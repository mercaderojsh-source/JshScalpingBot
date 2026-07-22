def momentum_score(ema_gap, trend_strength, atr_percent):
    """
    Momentum Score (0-100)

    Components:
      EMA Gap        : 40%
      Trend Strength : 40%
      ATR %          : 20%
    """

    # -----------------------
    # EMA Gap (0-40)
    # -----------------------
    if ema_gap >= 0.50:
        ema_points = 40
    elif ema_gap >= 0.35:
        ema_points = 32
    elif ema_gap >= 0.20:
        ema_points = 24
    elif ema_gap >= 0.10:
        ema_points = 16
    elif ema_gap >= 0.05:
        ema_points = 8
    else:
        ema_points = 0

    # -----------------------
    # Trend Strength (0-40)
    # -----------------------
    trend_points = max(0, min(trend_strength, 10)) * 4

    # -----------------------
    # ATR % (0-20)
    # -----------------------
    if atr_percent >= 2.0:
        atr_points = 20
    elif atr_percent >= 1.5:
        atr_points = 16
    elif atr_percent >= 1.0:
        atr_points = 12
    elif atr_percent >= 0.7:
        atr_points = 8
    elif atr_percent >= 0.4:
        atr_points = 4
    else:
        atr_points = 0

    score = ema_points + trend_points + atr_points

    return round(min(score, 100), 1)