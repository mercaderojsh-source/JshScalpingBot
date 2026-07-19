def detect_setup(
    ema9,
    ema21,
    ema50,
    rsi,
    atr
):
    """
    Returns:
    STRONG BUY
    BUY
    SELL
    STRONG SELL
    WATCHLIST
    """

    # Strong Buy
    if (
        ema9 > ema21 > ema50
        and 40 < rsi < 65
        and atr > 40
    ):
        return "🟢 STRONG BUY"

    # Buy Pullback
    if (
        ema9 > ema21
        and rsi < 40
        and atr > 40
    ):
        return "🟢 BUY"

    # Strong Sell
    if (
        ema9 < ema21 < ema50
        and 35 < rsi < 60
        and atr > 40
    ):
        return "🔴 STRONG SELL"

    # Sell Bounce
    if (
        ema9 < ema21
        and rsi > 60
        and atr > 40
    ):
        return "🔴 SELL"

    return "👀 WATCHLIST"