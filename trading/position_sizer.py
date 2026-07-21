import math

from config import LEVERAGE


def calculate_position_size(
    balance,
    risk_percent,
    entry_price,
    stop_loss,
    symbol_rules=None
):
    """
    Calculates a futures position size based on account risk
    while ensuring it does not exceed available buying power.
    """

    risk_amount = balance * (risk_percent / 100)

    stop_distance = abs(entry_price - stop_loss)

    if stop_distance <= 0:
        return 0

    # Risk-based size
    risk_size = risk_amount / stop_distance

    # Maximum size allowed by balance & leverage
    max_size = (balance * LEVERAGE) / entry_price

    # Use whichever is smaller
    raw_size = min(risk_size, max_size)

    # Paper trading
    if symbol_rules is None:
        return round(raw_size, 6)

    min_size = symbol_rules["min_size"]
    step = symbol_rules["size_step"]
    decimals = symbol_rules["size_decimals"]

    if raw_size < min_size:
        return 0

    size = math.floor(raw_size / step) * step

    return round(size, decimals)