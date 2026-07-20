import time

from config import LEVERAGE

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


class LiveTrader:

    def __init__(self):
        self.position = None

    def get_balance(self):
        response = get_futures_account()

        if response.get("code") != "00000":
            print("❌ Failed to fetch futures account.")
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
        symbol,
        side,
        entry_price,
        stop_loss,
        take_profit,
        risk_percent
    ):
        """
        Executes a complete live trade.
        """

        print("\n========== EXECUTE LIVE TRADE ==========")

        balance = self.get_balance()

        if balance is None:
            return {
                "success": False,
                "step": "balance"
            }

        rules = get_symbol_rules(symbol)

        if rules is None:
            return {
                "success": False,
                "step": "symbol_rules"
            }

        size = calculate_position_size(
            balance=balance,
            risk_percent=risk_percent,
            entry_price=entry_price,
            stop_loss=stop_loss,
            symbol_rules=rules
        )

        if size <= 0:
            return {
                "success": False,
                "step": "position_size"
            }

        hold_side = "long" if side == "buy" else "short"

        response = set_leverage(
            symbol,
            LEVERAGE,
            hold_side
        )

        if response.get("code") != "00000":
            return {
                "success": False,
                "step": "set_leverage",
                "response": response
            }

        response = place_market_order(
            symbol=symbol,
            side=side,
            size=size
        )

        if response.get("code") != "00000":
            return {
                "success": False,
                "step": "market_order",
                "response": response
            }

        time.sleep(3)

        response = place_stop_loss(
            symbol=symbol,
            hold_side=hold_side,
            stop_loss=stop_loss
        )

        if response.get("code") != "00000":
            return {
                "success": False,
                "step": "stop_loss",
                "response": response
            }

        response = place_take_profit(
            symbol=symbol,
            hold_side=hold_side,
            take_profit=take_profit
        )

        if response.get("code") != "00000":
            return {
                "success": False,
                "step": "take_profit",
                "response": response
            }

        print("✅ Live trade executed successfully.")

        return {
            "success": True,
            "symbol": symbol,
            "side": side,
            "size": size,
            "entry": entry_price,
            "stop_loss": stop_loss,
            "take_profit": take_profit
        }