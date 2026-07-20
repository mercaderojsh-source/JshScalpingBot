def trend_strength(
    ema9,
    ema21,
    ema50,
    price
):
    """
    Returns a trend strength score (0-20)
    tuned for 1-minute crypto scalping.
    """

    gap1 = abs(ema9 - ema21)
    gap2 = abs(ema21 - ema50)

    total_gap = gap1 + gap2

    percent = (total_gap / price) * 100

    if percent >= 0.30:
        return 20

    if percent >= 0.20:
        return 16

    if percent >= 0.15:
        return 12

    if percent >= 0.10:
        return 8

    if percent >= 0.05:
        return 4

    return 0