from config import TAKE_PROFIT_RR, ATR_STOP_MULTIPLIER, RISK_PER_TRADE, LEVERAGE


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

    # Apply the configured ATR multiplier (e.g. 1.2x ATR)
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


def calculate_position_size(
    account_balance,
    entry_price,
    stop_loss,
    risk_pct=RISK_PER_TRADE,
    leverage=LEVERAGE
):
    """
    Calculates exact position size in base currency based on risk percentage
    and stop loss distance, bounded by maximum account leverage limits.
    """
    if account_balance <= 0 or entry_price <= 0:
        return 0.0

    risk_amount = account_balance * (risk_pct / 100.0)
    stop_distance = abs(entry_price - stop_loss)

    if stop_distance == 0:
        return 0.0

    # Calculate quantity needed to risk exactly `risk_pct` of account
    raw_size = risk_amount / stop_distance

    # Bounded by total available margin * leverage cap
    max_notional = account_balance * leverage
    position_notional = raw_size * entry_price

    if position_notional > max_notional:
        raw_size = max_notional / entry_price

    return raw_size
