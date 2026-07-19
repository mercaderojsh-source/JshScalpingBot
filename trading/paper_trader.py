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
            "entry": price
        }

        print(f"📈 OPEN {direction} {pair} @ {price}")

        return True

    def close_trade(self, price):

        if self.position is None:
            return None

        entry = self.position["entry"]
        direction = self.position["direction"]

        if direction == "BUY":
            pnl = price - entry
        else:
            pnl = entry - price

        self.balance += pnl

        self.trade_count += 1

        if pnl > 0:
            self.wins += 1
        else:
            self.losses += 1

        print(f"💰 CLOSE Trade")
        print(f"PnL: {round(pnl,2)}")
        print(f"Balance: {round(self.balance,2)}")

        self.position = None

        return pnl

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