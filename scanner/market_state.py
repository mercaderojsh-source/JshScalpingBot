def market_state(ema9, ema21, ema50, atr, rsi):

    # Strong trend + high volatility
    if (
        (ema9 > ema21 > ema50 or ema9 < ema21 < ema50)
        and atr > 50
    ):
        return "🔥 EXPLOSIVE"

    # Trend present
    if ema9 > ema21 > ema50:
        return "⚡ TRENDING UP"

    if ema9 < ema21 < ema50:
        return "⚡ TRENDING DOWN"

    # Sideways
    if 45 <= rsi <= 55:
        return "🌊 RANGING"

    # Low-volatility market
    if atr < 30:
        return "😴 QUIET"

    # Mixed / transition market
    return "🌤 TRANSITION"