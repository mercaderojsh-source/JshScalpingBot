class PaperTrader:

    def __init__(self):
        self.balance = 15.00
        self.position = None
        self.trade_count = 0
        self.wins = 0
        self.losses = 0

    def open_trade(self, pair, direction, price):

        if self.position is not None:
            return False

        self.position = {
            "pair": pair,
            "direction": direction,
            "entry": price,
            "opened_at": price
        }

        print(f"📈 OPEN {direction} {pair} @ {price}")

        return True

    def check_exit(self, current_price):

        if self.position is None:
            return None

        entry = self.position["entry"]
        direction = self.position["direction"]

        if direction == "BUY":

            if current_price >= entry * 1.01:
                return "TP"

            if current_price <= entry * 0.995:
                return "SL"

        else:

            if current_price <= entry * 0.99:
                return "TP"

            if current_price >= entry * 1.005:
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
            "balance": self.balance
        }

        self.position = None

        return trade

    def stats(self):

        if self.trade_count == 0:
            win_rate = 0
        else:
            win_rate = round(
                self.wins / self.trade_count * 100,
                2
            )

        return {
            "balance": round(self.balance, 2),
            "trades": self.trade_count,
            "wins": self.wins,
            "losses": self.losses,
            "win_rate": win_rate
        }