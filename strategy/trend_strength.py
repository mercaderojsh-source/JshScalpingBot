def trend_strength(
    ema9,
    ema21,
    ema50,
    price
):
    """
    Returns a trend strength score (0-20).
    """

    gap1 = abs(ema9 - ema21)
    gap2 = abs(ema21 - ema50)

    total_gap = gap1 + gap2

    percent = (total_gap / price) * 100

    if percent >= 1.0:
        return 20

    if percent >= 0.80:
        return 18

    if percent >= 0.60:
        return 15

    if percent >= 0.40:
        return 12

    if percent >= 0.20:
        return 8

    if percent >= 0.10:
        return 5

    return 0