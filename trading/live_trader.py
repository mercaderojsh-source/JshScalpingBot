import time

from config import (
    LEVERAGE,
    RISK_PER_TRADE,
)

from exchange.bitget import (
    get_futures_account,
    get_positions,
    get_symbol_rules,
    set_leverage,
    place_market_order,
    place_stop_loss,
    place_take_profit,
)

from trading.position_sizer import calculate_position_size
from trading.risk_manager import calculate_levels


def format_precision(value, precision_places):
    """Formats float value according to Bitget symbol decimal place rule."""
    try:
        places = int(precision_places)
        return float(f"{value:.{places}f}")
    except Exception:
        return round(float(value), 4)


class LiveTrader:

    def __init__(self):
        self.position = None

    def get_balance(self):
        response = get_futures_account()

        if response.get("code") != "00000":
            print("❌ Failed to fetch futures account.")
            print(response)
            return None

        account = response["data"][0]

        balance = float(account["available"])

        print(f"💰 Live Balance: {balance:.2f} USDT")

        return balance

    def get_account_info(self):
        response = get_futures_account()

        if response.get("code") != "00000":
            print(response)
            return

        account = response["data"][0]

        print("\n========== LIVE ACCOUNT ==========")
        print(f"Available : {account['available']} USDT")
        print(f"Equity    : {account['accountEquity']} USDT")
        print(f"Locked    : {account['locked']} USDT")
        print(f"Margin    : {account['crossedMaxAvailable']} USDT")
        print("==================================")

    def get_open_positions(self):
        response = get_positions()

        if response.get("code") != "00000":
            print(response)
            return []

        positions = response.get("data", [])

        open_positions = []

        print("\n========== OPEN POSITIONS ==========")

        for pos in positions:
            size = float(pos.get("total", 0))

            if size == 0:
                continue

            symbol = pos["symbol"]
            side = pos["holdSide"]
            entry = pos["openPriceAvg"]
            pnl = pos["unrealizedPL"]

            print(
                f"{symbol} | {side.upper()} | "
                f"Entry: {entry} | "
                f"PnL: {pnl} USDT | "
                f"Size: {size}"
            )

            open_positions.append(pos)

        if not open_positions:
            print("No open positions.")

        print("====================================")

        return open_positions

    def execute_trade(
        self,
        pair,
        direction,
        entry_price,
        atr,
        context=None,
        **kwargs
    ):
        """
        Executes a complete live trade with exact Bitget price precision formatting
        and immediate SL/TP order attachment.
        """

        print("\n========== EXECUTE LIVE TRADE ==========")

        # Prevent duplicate trades
        if self.get_open_positions():
            print("⚠️ Existing live position detected.")
            return False

        # Calculate SL / TP
        levels = calculate_levels(
            entry_price=entry_price,
            atr=atr,
            direction=direction
        )

        raw_stop_loss = levels["stop_loss"]
        raw_take_profit = levels["take_profit"]

        balance = self.get_balance()

        if balance is None:
            return False

        rules = get_symbol_rules(pair)

        if rules is None:
            print("❌ Failed to fetch symbol rules.")
            return False

        price_precision = rules.get("pricePlace", 4)
        stop_loss = format_precision(raw_stop_loss, price_precision)
        take_profit = format_precision(raw_take_profit, price_precision)

        size = calculate_position_size(
            balance=balance,
            risk_percent=RISK_PER_TRADE,
            entry_price=entry_price,
            stop_loss=stop_loss,
            symbol_rules=rules
        )

        if size <= 0:
            print("❌ Invalid position size.")
            return False

        # Market order side
        side = "buy" if direction == "BUY" else "sell"

        # Required by Bitget leverage endpoint
        leverage_hold_side = "long" if direction == "BUY" else "short"

        # Reuse the Hedge Mode holdSide for TP/SL
        tpsl_hold_side = leverage_hold_side

        print(f"\n📈 Opening {direction} {pair}")
        print(f"Entry : {entry_price}")
        print(f"Size  : {size}")
        print(f"SL    : {stop_loss} (Precision: {price_precision})")
        print(f"TP    : {take_profit} (Precision: {price_precision})")

        # --------------------------------------------------
        # Set Leverage
        # --------------------------------------------------

        print("\n===== SET LEVERAGE =====")

        response = set_leverage(
            pair,
            LEVERAGE,
            leverage_hold_side
        )

        print(response)

        if response.get("code") != "00000":
            print("❌ Failed to set leverage.")
            return False

        # --------------------------------------------------
        # Place Market Order
        # --------------------------------------------------

        print("\n===== PLACE MARKET ORDER =====")

        response = place_market_order(
            symbol=pair,
            side=side,
            size=size
        )

        print(response)

        if response.get("code") != "00000":
            print("❌ Failed to place market order.")
            return False

        # Brief 0.5s pause to ensure exchange state syncs before attaching SL/TP
        time.sleep(0.5)

        # --------------------------------------------------
        # Attach Stop Loss
        # --------------------------------------------------

        print("\n===== ATTACH STOP LOSS =====")

        response = place_stop_loss(
            symbol=pair,
            hold_side=tpsl_hold_side,
            stop_loss=stop_loss
        )

        print("Stop Loss Response:")
        print(response)

        if response.get("code") == "00000":
            print("✅ Stop Loss attached successfully.")
        else:
            print(f"❌ Stop Loss attachment failed: {response.get('msg', 'Unknown Error')}")

        # --------------------------------------------------
        # Attach Take Profit
        # --------------------------------------------------

        print("\n===== ATTACH TAKE PROFIT =====")

        response = place_take_profit(
            symbol=pair,
            hold_side=tpsl_hold_side,
            take_profit=take_profit
        )

        print("Take Profit Response:")
        print(response)

        if response.get("code") == "00000":
            print("✅ Take Profit attached successfully.")
        else:
            print(f"❌ Take Profit attachment failed: {response.get('msg', 'Unknown Error')}")

        print("✅ Live trade execution completed.")

        return {
            "pair": pair,
            "direction": direction,
            "entry": entry_price,
            "atr": atr,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "size": size,
            "context": context or {}
        }
