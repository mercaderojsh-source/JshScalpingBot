import csv
import os
from datetime import datetime

from utils.github_backup import upload_file


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
                    "Setup",
                    "Market State",
                    "HTF",
                    "Brain Score",
                    "Confidence",
                    "Momentum",
                    "Quality",
                    "Trend Strength",
                    "Volatility",
                    "RSI",
                    "ATR %",
                    "Entry",
                    "Stop Loss",
                    "Take Profit",
                    "Exit",
                    "Exit Reason",
                    "PnL",
                    "Balance"
                ])

    def log_trade(self, trade, context=None, exit_reason=""):

        context = context or {}

        with open(self.filename, "a", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

                trade["pair"],
                trade["direction"],

                context.get("setup", ""),
                context.get("market_state", ""),
                context.get("higher_timeframe", ""),
                round(context.get("brain_score", 0), 2),
                context.get("confidence", ""),
                context.get("momentum", ""),
                context.get("quality", ""),
                context.get("trend_strength", ""),
                context.get("volatility_score", ""),
                round(context.get("rsi", 0), 2),
                round(context.get("atr_percent", 0), 2),

                round(trade["entry"], 4),
                round(trade["stop_loss"], 4),
                round(trade["take_profit"], 4),
                round(trade["exit"], 4),

                exit_reason,

                round(trade["pnl"], 4),
                round(trade["balance"], 2)
            ])

        upload_file(self.filename, "trade_history.csv")