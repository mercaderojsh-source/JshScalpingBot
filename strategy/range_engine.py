from indicators.bollinger import calculate_bollinger_bands

def detect_range_setup(closes, price, rsi, trend_score, min_trend_score=6):
    """
    Detects single-entry mean-reversion setups when trend score indicates range consolidation.
    Returns: 'STRONG RANGE BUY', 'STRONG RANGE SELL', or 'NO_SETUP'
    """
    # Range mode only activates when market is flat (Trend Score < Threshold)
    if trend_score >= min_trend_score:
        return "NO_SETUP"

    upper, middle, lower = calculate_bollinger_bands(closes, period=20, std_dev=2.0)
    if not upper or not lower:
        return "NO_SETUP"

    # Support Bounce: Price near/below Lower Band + Oversold RSI
    if price <= lower * 1.001 and rsi <= 35:
        return "STRONG RANGE BUY"

    # Resistance Drop: Price near/above Upper Band + Overbought RSI
    if price >= upper * 0.999 and rsi >= 65:
        return "STRONG RANGE SELL"

    return "NO_SETUP"
