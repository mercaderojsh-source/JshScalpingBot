def opportunity_score(
    momentum,
    quality,
    volatility
):
    score = (
        momentum * 0.40
        + quality * 0.45
        + volatility * 0.15
    )

    return round(score, 1)