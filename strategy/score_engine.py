def final_score(confidence, volatility, market_state, setup):
    """
    Returns a score out of 100.
    Higher is better.
    """

    score = confidence

    # Reward volatility
    score += min(volatility, 15)

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

    return round(min(score, 100), 1)