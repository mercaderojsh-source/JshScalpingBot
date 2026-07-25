from config import TAKE_PROFIT_RR, ATR_STOP_MULTIPLIER


def calculate_levels(
    entry_price,
    atr,
    direction,
    rr_ratio=TAKE_PROFIT_RR,
    atr_multiplier=ATR_STOP_MULTIPLIER
):
    """
    ATR-based Stop Loss & Take Profit incorporating configured ATR multiplier.
    """

    # Apply the configured ATR multiplier (e.g. 1.8x ATR)
    stop_distance = atr * atr_multiplier

    if direction == "BUY":
        stop_loss = entry_price - stop_distance
        take_profit = entry_price + (stop_distance * rr_ratio)
    else:
        stop_loss = entry_price + stop_distance
        take_profit = entry_price - (stop_distance * rr_ratio)

    return {
        "stop_loss": round(stop_loss, 4),
        "take_profit": round(take_profit, 4)
    }
