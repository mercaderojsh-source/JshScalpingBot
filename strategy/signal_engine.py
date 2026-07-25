def generate_signal(ema9, ema21, ema50, atr, rsi, current_price):
    score = 0
    reasons = []

    # -------------------------
    # 1. Trend Alignment (40 Points Max)
    # -------------------------
    if ema9 > ema21 > ema50:
        score += 40
        reasons.append("✅ Strong Bull Trend")
    elif ema9 < ema21 < ema50:
        score += 40
        reasons.append("✅ Strong Bear Trend")
    elif ema9 > ema50 or ema9 < ema50:
        score += 20
        reasons.append("⚠ Moderate Trend")
    else:
        reasons.append("❌ Sideways Market")

    # -------------------------
    # 2. Relative EMA Gap (20 Points Max)
    # Normalized as percentage of EMA50 (0.05% to 0.3% is normal on 1m)
    # -------------------------
    ema_gap_pct = (abs(ema9 - ema50) / ema50) * 100

    if 0.10 <= ema_gap_pct <= 0.40:
        score += 20
        reasons.append("✅ Ideal Scalp Expansion")
    elif ema_gap_pct > 0.40:
        score += 5
        reasons.append("⚠ Overextended Trend (Reversal Risk)")
    else:
        reasons.append("❌ Tight Consolidation")

    # -------------------------
    # 3. Percentage ATR / Volatility (20 Points Max)
    # Scaled to asset price so it works on XRP, DOGE, SOL, and BTC
    # -------------------------
    atr_pct = (atr / current_price) * 100

    if atr_pct >= 0.15:
        score += 20
        reasons.append(f"✅ High Volatility ({atr_pct:.2f}%)")
    elif atr_pct >= 0.08:
        score += 12
        reasons.append(f"✅ Medium Volatility ({atr_pct:.2f}%)")
    else:
        reasons.append(f"❌ Low Volatility ({atr_pct:.2f}%)")

    # -------------------------
    # 4. Pullback RSI Momentum (20 Points Max)
    # Rewards healthy pullbacks instead of overbought peaks
    # -------------------------
    if 40 <= rsi <= 58:
        score += 20
        reasons.append("✅ Prime Pullback Zone")
    elif 35 <= rsi <= 65:
        score += 10
        reasons.append("⚠ Acceptable Momentum")
    else:
        reasons.append("❌ Overbought/Oversold Extreme")

    return round(min(score, 100), 1), reasons
