def calculate_bollinger_bands(closes, period=20, std_dev=2.0):
    """Calculates Upper, Middle (SMA), and Lower Bollinger Bands."""
    if len(closes) < period:
        return None, None, None
    slice_closes = closes[-period:]
    sma = sum(slice_closes) / period
    variance = sum((x - sma) ** 2 for x in slice_closes) / period
    std = variance ** 0.5
    upper_band = sma + (std_dev * std)
    lower_band = sma - (std_dev * std)
    return upper_band, sma, lower_band
