def generate_signal(ema9, ema21, ema50, atr, rsi):

    score = 0
    reasons = []

    # -------------------------
    # Trend
    # -------------------------

    if ema9 > ema21 > ema50:
        score += 40
        reasons.append("✅ Strong Bull Trend")

    elif ema9 < ema21 < ema50:
        score += 40
        reasons.append("✅ Strong Bear Trend")

    else:
        reasons.append("❌ Sideways")

    # -------------------------
    # EMA Separation
    # -------------------------

    ema_gap = abs(ema9 - ema50)

    if ema_gap > ema50 * 0.015:
        score += 20
        reasons.append("✅ Strong EMA Separation")

    elif ema_gap > ema50 * 0.008:
        score += 10
        reasons.append("✅ Moderate EMA Separation")

    else:
        reasons.append("❌ Weak Trend")

    # -------------------------
    # ATR
    # -------------------------

    if atr > 100:
        score += 20
        reasons.append("✅ Excellent Volatility")

    elif atr > 70:
        score += 15
        reasons.append("✅ Good Volatility")

    elif atr > 50:
        score += 10
        reasons.append("⚠ Average Volatility")

    else:
        reasons.append("❌ Low Volatility")

    # -------------------------
    # RSI
    # -------------------------

    if 45 <= rsi <= 60:
        score += 20
        reasons.append("✅ Healthy Momentum")

    elif 40 <= rsi <= 65:
        score += 10
        reasons.append("⚠ Acceptable Momentum")

    else:
        reasons.append("❌ Weak Momentum")

    return round(min(score, 100), 1), reasons