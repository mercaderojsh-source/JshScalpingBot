def final_score(
    confidence,
    volatility,
    trend_strength,
    market_state,
    setup
):
    """
    Intelligent weighted score (0-100)
    """

    score = confidence * 0.45

    # -------------------------
    # Volatility (0-15)
    # -------------------------

    score += min(volatility, 15) * 0.8

    # -------------------------
    # Trend Strength (0-20)
    # -------------------------

    score += min(trend_strength, 20)

    # -------------------------
    # Market State
    # -------------------------

    if "EXPLOSIVE" in market_state:
        score += 15

    elif "TRENDING" in market_state:
        score += 10

    elif "RANGING" in market_state:
        score -= 8

    # -------------------------
    # Setup Quality
    # -------------------------

    if "STRONG" in setup:
        score += 15

    elif "BUY" in setup or "SELL" in setup:
        score += 8

    if "WATCHLIST" in setup:
        score -= 30

    return round(max(0, min(score, 100)), 1)