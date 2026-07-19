from config import START_BALANCE
from trading.risk_manager import calculate_levels


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

        self.position = {
            "pair": pair,
            "direction": direction,
            "entry": price,
            "opened_at": price,
            "atr": atr,
            "stop_loss": levels["stop_loss"],
            "take_profit": levels["take_profit"]
        }

        print(f"📈 OPEN {direction} {pair} @ {price}")
        print(f"🛑 Stop Loss : {levels['stop_loss']}")
        print(f"🎯 Take Profit : {levels['take_profit']}")

        return True

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

    def close_trade(self, current_price):

        if self.position is None:
            return None

        entry = self.position["entry"]
        direction = self.position["direction"]

        if direction == "BUY":
            pnl = current_price - entry
        else:
            pnl = entry - current_price

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
            "take_profit": self.position["take_profit"]
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