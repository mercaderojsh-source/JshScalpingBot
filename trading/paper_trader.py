from config import (
    START_BALANCE,
    RISK_PER_TRADE,
)

from trading.risk_manager import calculate_levels
from trading.position_sizer import calculate_position_size


class PaperTrader:

    def __init__(self):
        self.balance = START_BALANCE
        self.position = None
        self.trade_count = 0
        self.wins = 0
        self.losses = 0

    def open_trade(self, pair, direction, price, atr):

        if self.position is not None:
            return False

        levels = calculate_levels(
            entry_price=price,
            atr=atr,
            direction=direction
        )

        position_size = calculate_position_size(
            balance=self.balance,
            risk_percent=RISK_PER_TRADE,
            entry_price=price,
            stop_loss=levels["stop_loss"]
        )

        self.position = {
            "pair": pair,
            "direction": direction,
            "entry": price,
            "opened_at": price,
            "atr": atr,

            # Original risk level
            "initial_stop": levels["stop_loss"],

            # Active levels
            "stop_loss": levels["stop_loss"],
            "take_profit": levels["take_profit"],

            # Position sizing
            "size": position_size,

            # Trade management flags
            "break_even": False,
            "partial_taken": False
        }

        print(f"📈 OPEN {direction} {pair} @ {price}")
        print(f"📦 Position Size : {position_size}")
        print(f"🛑 Stop Loss : {levels['stop_loss']}")
        print(f"🎯 Take Profit : {levels['take_profit']}")

        return self.position

    def check_exit(self, current_price):

        if self.position is None:
            return None

        direction = self.position["direction"]
        stop_loss = self.position["stop_loss"]
        take_profit = self.position["take_profit"]

        if direction == "BUY":

            if current_price >= take_profit:
                return "TP"

            if current_price <= stop_loss:
                return "SL"

        else:

            if current_price <= take_profit:
                return "TP"

            if current_price >= stop_loss:
                return "SL"

        return None

    def manage_trade(self, current_price):

        if self.position is None:
            return None

        # Already protected
        if self.position["break_even"]:
            return None

        entry = self.position["entry"]
        initial_stop = self.position["initial_stop"]
        direction = self.position["direction"]

        # Initial risk (1R)
        risk = abs(entry - initial_stop)

        if risk == 0:
            return None

        if direction == "BUY":
            profit = current_price - entry
        else:
            profit = entry - current_price

        r_multiple = profit / risk

        # Move stop to break-even after +1R
        if r_multiple >= 1:

            self.position["stop_loss"] = entry
            self.position["break_even"] = True

            print(f"🛡 Break-even activated for {self.position['pair']}")

            return "BREAK_EVEN"

        return None

    def close_trade(self, current_price):

        if self.position is None:
            return None

        entry = self.position["entry"]
        direction = self.position["direction"]
        size = self.position["size"]

        if direction == "BUY":
            pnl = (current_price - entry) * size
        else:
            pnl = (entry - current_price) * size

        self.balance += pnl
        self.trade_count += 1

        if pnl > 0:
            self.wins += 1
        else:
            self.losses += 1

        print(f"💰 CLOSE {self.position['pair']}")
        print(f"PnL : {round(pnl, 2)}")
        print(f"Balance : {round(self.balance, 2)}")

        trade = {
            "pair": self.position["pair"],
            "direction": self.position["direction"],
            "entry": entry,
            "exit": current_price,
            "pnl": pnl,
            "balance": self.balance,
            "stop_loss": self.position["stop_loss"],
            "take_profit": self.position["take_profit"],
            "size": self.position["size"]
        }

        self.position = None

        return trade

    def stats(self):

        if self.trade_count == 0:
            win_rate = 0
        else:
            win_rate = round(
                (self.wins / self.trade_count) * 100,
                2
            )

        return {
            "balance": round(self.balance, 2),
            "trades": self.trade_count,
            "wins": self.wins,
            "losses": self.losses,
            "win_rate": win_rate
        }