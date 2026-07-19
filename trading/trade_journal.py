import csv
import os
from datetime import datetime


class TradeJournal:

    def __init__(self, filename="trade_history.csv"):
        self.filename = filename

        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="") as file:
                writer = csv.writer(file)

                writer.writerow([
                    "Time",
                    "Pair",
                    "Direction",
                    "Entry",
                    "Exit",
                    "PnL",
                    "Reason",
                    "Balance"
                ])

    def log_trade(
        self,
        pair,
        direction,
        entry,
        exit_price,
        pnl,
        reason,
        balance
    ):

        with open(self.filename, "a", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                pair,
                direction,
                round(entry, 4),
                round(exit_price, 4),
                round(pnl, 4),
                reason,
                round(balance, 2)
            ])