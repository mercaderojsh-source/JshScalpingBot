def generate_signal(ema9, ema21, ema50, atr, rsi):
    score = 0
    reasons = []

    # Trend
    if ema9 > ema21 > ema50:
        score += 1
        reasons.append("✅ Bullish Trend")
    elif ema9 < ema21 < ema50:
        score += 1
        reasons.append("✅ Bearish Trend")
    else:
        reasons.append("❌ Sideways Market")

    # RSI
    if rsi < 30:
        score += 1
        reasons.append("✅ RSI Oversold")
    elif rsi > 70:
        score += 1
        reasons.append("✅ RSI Overbought")
    else:
        reasons.append("❌ RSI Neutral")

    # ATR
    if atr > 30:
        score += 1
        reasons.append("✅ Good Volatility")
    else:
        reasons.append("❌ Low Volatility")

    return score, reasons