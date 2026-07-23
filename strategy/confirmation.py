def confirm_entry(
    setup,
    market_state,
    score,
    rsi,
    atr_percent
):
    """
    Intelligent trade confirmation.
    Returns True if the setup passes all filters.
    """

    # -----------------------
    # Ignore watchlist setups
    # -----------------------
    if "WATCHLIST" in setup:
        print("❌ Rejected: Watchlist setup")
        return False

    # -----------------------
    # Adaptive minimum score
    # -----------------------
    minimum_score = 75

    if "TRENDING" in market_state:
        minimum_score = 70

    elif "QUIET" in market_state:
        minimum_score = 60

    # -----------------------
    # Score filter
    # -----------------------
    if score < minimum_score:
        print(
            f"❌ Rejected: "
            f"Score={score:.1f} "
            f"(Need {minimum_score}, "
            f"Missing {minimum_score-score:.1f})"
        )
        return False

    # -----------------------
    # RSI filter
    # -----------------------
    if rsi > 80 or rsi < 20:
        print(
            f"❌ Rejected: Extreme RSI ({rsi:.1f})"
        )
        return False

    # -----------------------
    # ATR filter
    # -----------------------
    if atr_percent < 0.02:
        print(
            f"❌ Rejected: ATR too low ({atr_percent:.2f}%)"
        )
        return False

    print(
        f"✅ Passed confirmation "
        f"(Threshold={minimum_score})"
    )

    return True