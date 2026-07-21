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
        atr
    ):
        """
        Executes a complete live trade using the same
        interface as PaperTrader.
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

        stop_loss = levels["stop_loss"]
        take_profit = levels["take_profit"]

        balance = self.get_balance()

        if balance is None:
            return False

        rules = get_symbol_rules(pair)

        if rules is None:
            print("❌ Failed to fetch symbol rules.")
            return False

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

        side = "buy" if direction == "BUY" else "sell"

        # Bitget One-way Position Mode
        hold_side = side

        print(f"\n📈 Opening {direction} {pair}")
        print(f"Entry : {entry_price}")
        print(f"Size  : {size}")
        print(f"SL    : {stop_loss}")
        print(f"TP    : {take_profit}")

        print("\n===== SET LEVERAGE =====")

        response = set_leverage(
            pair,
            LEVERAGE,
            hold_side
        )

        print(response)

        if response.get("code") != "00000":
            print("❌ Failed to set leverage.")
            return False

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

        print("⏳ Waiting 3 seconds for Bitget to register the position...")
        time.sleep(3)

        # ---------------- STOP LOSS ----------------

        print("\n===== ATTACH STOP LOSS =====")

        response = place_stop_loss(
            symbol=pair,
            hold_side=hold_side,
            stop_loss=stop_loss
        )

        print("Stop Loss Response:")
        print(response)

        if response.get("code") == "00000":
            print("✅ Stop Loss attached.")
        else:
            print("❌ Stop Loss attachment failed.")

        # ---------------- TAKE PROFIT ----------------

        print("\n===== ATTACH TAKE PROFIT =====")

        response = place_take_profit(
            symbol=pair,
            hold_side=hold_side,
            take_profit=take_profit
        )

        print("Take Profit Response:")
        print(response)

        if response.get("code") == "00000":
            print("✅ Take Profit attached.")
        else:
            print("❌ Take Profit attachment failed.")

        print("✅ Live trade execution completed.")

        return {
            "pair": pair,
            "direction": direction,
            "entry": entry_price,
            "atr": atr,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "size": size
        }