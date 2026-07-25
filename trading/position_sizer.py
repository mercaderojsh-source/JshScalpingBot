import math
from config import LEVERAGE


def calculate_position_size(
    balance,
    risk_percent,
    entry_price,
    stop_loss,
    symbol_rules=None,
    min_notional=5.0  # Bitget minimum order size in USDT
):
    """
    Calculates a futures position size based on account risk while ensuring
    it respects exchange minimum order value and buying power limits.
    """

    risk_amount = balance * (risk_percent / 100)
    stop_distance = abs(entry_price - stop_loss)

    if stop_distance <= 0 or entry_price <= 0:
        return 0

    # 1. Risk-based position size (in asset contracts/coins)
    risk_size = risk_amount / stop_distance

    # 2. Maximum size allowed by available balance & leverage (10% safety buffer)
    max_size = (balance * LEVERAGE * 0.90) / entry_price

    # 3. Take the safer/smaller size
    raw_size = min(risk_size, max_size)

    # 4. Check Bitget Minimum Order Notional ($5.00 USDT minimum order value)
    notional_value = raw_size * entry_price
    if notional_value < min_notional:
        print(f"⚠️ Trade skipped: Position value (${notional_value:.2f}) < Bitget Min Order (${min_notional:.2f})")
        return 0

    # Paper trading format
    if symbol_rules is None:
        return round(raw_size, 6)

    # Live trading step alignment
    min_size = symbol_rules.get("min_size", 0.001)
    step = symbol_rules.get("size_step", 0.001)
    decimals = symbol_rules.get("size_decimals", 4)

    if raw_size < min_size:
        return 0

    # Round down to exact valid contract precision
    size = math.floor(raw_size / step) * step

    return round(size, decimals)
