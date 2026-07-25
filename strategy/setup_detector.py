def detect_setup(ema9, ema21, ema50, rsi, price):
    """
    Detects Pullbacks & Trend Continuations for 1m Scalping.
    """
    is_bullish_trend = ema21 > ema50
    is_bearish_trend = ema21 < ema50

    # Distance from EMA21 to price (detecting dip/pullback)
    price_to_ema21 = abs(price - ema21) / ema21

    # -----------------------------
    # Long Setups (Buy the Dip in Uptrend)
    # -----------------------------
    if is_bullish_trend:
        # Pullback into EMA21/EMA50 with RSI reset (Prime Scalp)
        if 40 <= rsi <= 52 and price_to_ema21 <= 0.002:
            return "🟢 STRONG BUY"
        # Standard Momentum Breakout
        elif 52 < rsi <= 65 and ema9 > ema21:
            return "🟢 BUY"

    # -----------------------------
    # Short Setups (Sell the Rally in Downtrend)
    # -----------------------------
    if is_bearish_trend:
        # Rally back to EMA21/EMA50 with RSI reset (Prime Scalp)
        if 48 <= rsi <= 60 and price_to_ema21 <= 0.002:
            return "🔴 STRONG SELL"
        # Standard Momentum Breakdown
        elif 35 <= rsi < 48 and ema9 < ema21:
            return "🔴 SELL"

    return "👀 WATCHLIST"
