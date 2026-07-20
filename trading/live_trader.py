from exchange.bitget import get_futures_account, get_positions


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