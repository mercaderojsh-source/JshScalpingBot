import math


def calculate_position_size(
    balance,
    risk_percent,
    entry_price,
    stop_loss,
    symbol_rules=None
):
    """
    Calculates a futures position size based on account risk.

    Args:
        balance (float): Available account balance.
        risk_percent (float): Percent of balance to risk.
        entry_price (float): Planned entry price.
        stop_loss (float): Stop-loss price.
        symbol_rules (dict, optional): Exchange trading rules.

    Returns:
        float: Position size.
    """

    risk_amount = balance * (risk_percent / 100)

    stop_distance = abs(entry_price - stop_loss)

    if stop_distance <= 0:
        return 0

    raw_size = risk_amount / stop_distance

    # -----------------------------
    # Paper Trading
    # -----------------------------
    if symbol_rules is None:
        return round(raw_size, 6)

    # -----------------------------
    # Live Trading
    # -----------------------------
    min_size = symbol_rules["min_size"]
    step = symbol_rules["size_step"]
    decimals = symbol_rules["size_decimals"]

    if raw_size < min_size:
        return 0

    # Round DOWN to the nearest valid contract step
    size = math.floor(raw_size / step) * step

    return round(size, decimals)