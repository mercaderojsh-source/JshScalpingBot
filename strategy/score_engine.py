def final_score(
    confidence,
    volatility,
    trend_strength,
    market_state,
    setup
):
    """
    Returns a score out of 100.
    Higher is better.
    """

    score = confidence

    # Reward volatility
    score += min(volatility, 15)

    # Reward trend strength
    score += trend_strength

    # Reward market state
    if "EXPLOSIVE" in market_state:
        score += 20
    elif "TRENDING" in market_state:
        score += 10

    # Reward setup quality
    if "STRONG" in setup:
        score += 15
    elif "BUY" in setup or "SELL" in setup:
        score += 8

    # Penalize watchlist setups
    if "WATCHLIST" in setup:
        score -= 35

    score = max(0, min(score, 100))

    return round(score, 1)