def confirm_entry(
    setup,
    market_state,
    score,
    rsi,
    atr_percent
):
    """
    Intelligent trade confirmation with fee & noise filters.
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
    minimum_score = 60

    if "TRENDING" in market_state:
        minimum_score = 55
    elif "QUIET" in market_state:
        minimum_score = 50

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
    # RSI Extreme Filter
    # -----------------------
    if rsi > 75 or rsi < 25:
        print(f"❌ Rejected: Extreme RSI ({rsi:.1f})")
        return False

    # -----------------------
    # ATR Fee-Coverage Filter
    # Requires min 0.08% move potential to exceed Bitget roundtrip fees (~0.12%)
    # -----------------------
    if atr_percent < 0.08:
        print(
            f"❌ Rejected: ATR too low ({atr_percent:.2f}% < 0.08% fee barrier)"
        )
        return False

    print(f"✅ Passed confirmation (Threshold={minimum_score})")

    return True
