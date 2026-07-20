from exchange.bitget import get_futures_account


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