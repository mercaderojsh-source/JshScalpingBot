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

    print("\n📝 ENTRY FILTER")

    # Ignore weak setups
    if "WATCHLIST" in setup:
        print("❌ Rejected: WATCHLIST setup")
        return False

    # Ignore ranging/quiet markets
    if market_state in ["🌊 RANGING", "😴 QUIET"]:
        print(f"❌ Rejected: Market State = {market_state}")
        return False

    # Require minimum strategy score
    if score < MIN_SCORE:
        print(f"❌ Rejected: Score = {score:.1f} (Minimum = {MIN_SCORE})")
        return False

    # Avoid chasing overextended moves
    if rsi > 72 or rsi < 28:
        print(f"❌ Rejected: RSI = {rsi:.2f}")
        return False

    # Require sufficient volatility
    if atr_percent < 0.05:
        print(f"❌ Rejected: ATR % = {atr_percent:.2f}%")
        return False

    print("✅ ENTRY APPROVED")

    return True