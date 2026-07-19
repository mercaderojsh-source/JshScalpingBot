def calculate_position_size(
    balance,
    risk_percent,
    entry_price,
    stop_loss
):
    """
    Calculates position size based on account risk.

    Returns:
        float
    """

    risk_amount = balance * (risk_percent / 100)

    stop_distance = abs(entry_price - stop_loss)

    if stop_distance == 0:
        return 0

    size = risk_amount / stop_distance

    return round(size, 6)