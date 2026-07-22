def intelligence_score(data):
    """
    Brain V2

    Weighted score out of 100.
    """

    score = 0

    # -----------------------
    # Trend Alignment (30)
    # -----------------------

    if data["higher_timeframe"] == "BUY":

        if "BUY" in data["setup"]:
            score += 30

    elif data["higher_timeframe"] == "SELL":

        if "SELL" in data["setup"]:
            score += 30

    # -----------------------
    # Momentum (25)
    # -----------------------

    momentum = data["momentum"]

    score += momentum * 0.25

    # -----------------------
    # Quality (20)
    # -----------------------

    quality = data["quality"]

    score += quality * 0.20

    # -----------------------
    # Market Condition (15)
    # -----------------------

    state = data["market_state"]

    if "EXPLOSIVE" in state:
        score += 15

    elif "TRENDING" in state:
        score += 10

    elif "QUIET" in state:
        score += 3

    # -----------------------
    # Volatility (10)
    # -----------------------

    vol = data["volatility_score"]

    score += min(vol, 10)

    return round(min(score, 100), 1)