from config import TAKE_PROFIT_RR


def calculate_levels(entry_price, atr, direction, rr_ratio=TAKE_PROFIT_RR):
    """
    ATR-based Stop Loss & Take Profit.

    rr_ratio:
        2.0 = Risk 1 to make 2
    """

    stop_distance = atr

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