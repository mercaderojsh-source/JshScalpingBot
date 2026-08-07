def detect_liquidity_impulse(atr, atr_ma, price, rsi):
    """Detects immediate institutional liquidity surges for fast scalping."""
    
    # Ensure volatility expansion is active (ATR surge)
    if atr < (atr_ma * 1.3):
        return "NO_IMPULSE"
        
    # Bullish Impulse Burst
    if rsi >= 60 and rsi <= 75:
        return "BUY_IMPULSE"
        
    # Bearish Impulse Burst
    if rsi <= 40 and rsi >= 25:
        return "SELL_IMPULSE"
        
    return "NO_IMPULSE"
