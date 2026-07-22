def quality_score(
    confidence,
    setup,
    htf
):
    score = confidence

    if "STRONG" in setup:
        score += 20

    if htf == "BUY" and "BUY" in setup:
        score += 15

    elif htf == "SELL" and "SELL" in setup:
        score += 15

    elif htf == "NEUTRAL":
        score += 5

    return min(score, 100)