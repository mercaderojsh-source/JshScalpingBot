def detect_setup(
    ema9,
    ema21,
    ema50,
    rsi,
    atr
):
    """
    Returns:
        🟢 STRONG BUY
        🟢 BUY
        🔴 STRONG SELL
        🔴 SELL
        👀 WATCHLIST
    """

    # -----------------------------
    # Strong Buy
    # -----------------------------
    if (
        ema9 > ema21 > ema50
        and 45 <= rsi <= 70
    ):
        return "🟢 STRONG BUY"

    # -----------------------------
    # Buy
    # -----------------------------
    if (
        ema9 > ema21
        and ema21 >= ema50
        and rsi < 70
    ):
        return "🟢 BUY"

    # -----------------------------
    # Strong Sell
    # -----------------------------
    if (
        ema9 < ema21 < ema50
        and 30 <= rsi <= 55
    ):
        return "🔴 STRONG SELL"

    # -----------------------------
    # Sell
    # -----------------------------
    if (
        ema9 < ema21
        and ema21 <= ema50
        and rsi > 30
    ):
        return "🔴 SELL"

    return "👀 WATCHLIST"