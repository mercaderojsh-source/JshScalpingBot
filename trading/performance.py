import os
import csv
from datetime import datetime

try:
    from config import LOG_FILE
except ImportError:
    LOG_FILE = "trade_history.csv"


def log_trade_result(pair, direction, entry, exit_price, win, pnl=0.0):
    """
    Logs a completed trade result to the configured CSV file.
    """
    file_exists = os.path.isfile(LOG_FILE)
    fieldnames = ["timestamp", "pair", "direction", "entry", "exit", "result", "pnl"]
    result_str = "WIN" if win else "LOSS"

    try:
        with open(LOG_FILE, mode="a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "pair": pair,
                "direction": direction,
                "entry": entry,
                "exit": exit_price,
                "result": result_str,
                "pnl": round(pnl, 4)
            })
    except Exception as e:
        print(f"⚠️ Error logging trade result: {e}")


def performance_summary():
    """
    Reads performance logs and calculates overall metrics.
    """
    if not os.path.isfile(LOG_FILE):
        return {
            "trades": 0,
            "wins": 0,
            "losses": 0,
            "win_rate": 0.0,
            "net_profit": 0.0
        }

    trades = 0
    wins = 0
    losses = 0
    net_profit = 0.0

    try:
        with open(LOG_FILE, mode="r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                trades += 1
                res = str(row.get("result", "")).upper()
                if "WIN" in res:
                    wins += 1
                elif "LOSS" in res:
                    losses += 1

                try:
                    net_profit += float(row.get("pnl", 0.0))
                except (ValueError, TypeError):
                    pass
    except Exception as e:
        print(f"⚠️ Error reading performance log: {e}")

    win_rate = round((wins / trades * 100), 1) if trades > 0 else 0.0

    return {
        "trades": trades,
        "wins": wins,
        "losses": losses,
        "win_rate": win_rate,
        "net_profit": round(net_profit, 2)
    }
