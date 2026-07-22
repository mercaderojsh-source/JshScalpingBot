def intelligence_score(candidate):
    """
    Calculates a weighted intelligence score.

    Returns 0-100.
    """

    score = 0

    # ----------------------------
    # Confidence (40%)
    # ----------------------------
    score += candidate["confidence"] * 0.40

    # ----------------------------
    # Existing Score (20%)
    # ----------------------------
    score += candidate["score"] * 0.20

    # ----------------------------
    # Trend Strength (15%)
    # ----------------------------
    score += candidate["trend_strength"] * 0.15

    # ----------------------------
    # Volatility (15%)
    # ----------------------------
    score += min(candidate["volatility_score"], 15)

    # ----------------------------
    # Market State (10%)
    # ----------------------------
    state = candidate["market_state"]

    if "EXPLOSIVE" in state:
        score += 10

    elif "TRENDING" in state:
        score += 7

    elif "SIDEWAYS" in state:
        score -= 10

    return round(score, 2)