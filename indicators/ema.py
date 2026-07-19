def calculate_ema(closes, period):
    if len(closes) < period:
        return None

    multiplier = 2 / (period + 1)

    ema = sum(closes[:period]) / period

    for price in closes[period:]:
        ema = (price - ema) * multiplier + ema

    return ema