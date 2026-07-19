import csv


def performance_summary(filename="trade_history.csv"):

    trades = []

    try:
        with open(filename, "r") as file:

            reader = csv.DictReader(file)

            for row in reader:
                trades.append(row)

    except FileNotFoundError:

        return {
            "trades": 0,
            "wins": 0,
            "losses": 0,
            "win_rate": 0,
            "net_profit": 0
        }

    total = len(trades)

    wins = 0
    losses = 0
    profit = 0

    for trade in trades:

        pnl = float(trade["PnL"])

        profit += pnl

        if pnl > 0:
            wins += 1
        else:
            losses += 1

    win_rate = 0

    if total > 0:
        win_rate = round(wins / total * 100, 2)

    return {
        "trades": total,
        "wins": wins,
        "losses": losses,
        "win_rate": win_rate,
        "net_profit": round(profit, 2)
    }