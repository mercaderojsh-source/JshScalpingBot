from config import MIN_SCORE


def confirm_entry(
    setup,
    market_state,
    score,
    rsi,
    atr_percent
):
    """
    Final filter before opening a trade.

    Returns:
        True / False
    """

    # Ignore weak setups
    if "WATCHLIST" in setup:
        return False

    # Ignore ranging/quiet markets
    if market_state in ["🌊 RANGING", "😴 QUIET"]:
        return False

    # Require minimum strategy score
    if score < MIN_SCORE:
        return False

    # Avoid chasing overextended moves
    if rsi > 72 or rsi < 28:
        return False

    # Require sufficient volatility
    if atr_percent < 0.30:
        return False

    return True