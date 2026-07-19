def calculate_atr(highs, lows, closes, period=14):
    if len(highs) < period + 1:
        return None

    true_ranges = []

    for i in range(1, len(highs)):
        tr = max(
            highs[i] - lows[i],
            abs(highs[i] - closes[i - 1]),
            abs(lows[i] - closes[i - 1])
        )
        true_ranges.append(tr)

    atr = sum(true_ranges[-period:]) / period

    return atr