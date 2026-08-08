import os
import csv
from datetime import datetime

try:
    from config import LOG_FILE
except ImportError:
    LOG_FILE = "trade_history_gold_1m.csv"


def analyze_past_performance(lookback=30):
    """
    Analyzes the last `lookback` trades from the CSV log to compute
    rolling win rates per trade setup type.
    """
    if not os.path.isfile(LOG_FILE):
        return {}

    trades = []
    try:
        with open(LOG_FILE, mode="r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                trades.append(row)
    except Exception as e:
        print(f"⚠️ Self-Learning Engine Error reading logs: {e}")
        return {}

    # Slice the last N trades
    recent_trades = trades[-lookback:]
    setup_stats = {}

    for trade in recent_trades:
        # Infer direction/setup from logged trade
        direction = str(trade.get("direction", "")).upper()
        result = str(trade.get("result", "")).upper()

        if not direction:
            continue

        if direction not in setup_stats:
            setup_stats[direction] = {"wins": 0, "total": 0}

        setup_stats[direction]["total"] += 1
        if "WIN" in result:
            setup_stats[direction]["wins"] += 1

    # Calculate win rates per direction
    win_rates = {}
    for key, data in setup_stats.items():
        if data["total"] > 0:
            win_rates[key] = data["wins"] / data["total"]

    return win_rates


def apply_self_learning_adjustment(base_score, direction, context=None):
    """
    Dynamically adjusts the base entry score based on recent win-rate feedback.
    """
    win_rates = analyze_past_performance(lookback=20)
    adjusted_score = base_score
    dir_key = str(direction).upper()

    if dir_key in win_rates:
        win_rate = win_rates[dir_key]

        # Cold Streak Penalty: Severe loss rate on this direction -> Penalize score
        if win_rate < 0.40:
            penalty = 15.0
            adjusted_score -= penalty
            print(f"🧠 Self-Learning: {dir_key} win rate is low ({win_rate*100:.1f}%). Score penalized by -{penalty}")

        # Hot Streak Reward: Strong win rate -> Boost score
        elif win_rate >= 0.65:
            boost = 10.0
            adjusted_score += boost
            print(f"🧠 Self-Learning: {dir_key} win rate is high ({win_rate*100:.1f}%). Score boosted by +{boost}")

    return max(0.0, min(100.0, adjusted_score))
