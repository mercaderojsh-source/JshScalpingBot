from trading.live_trader import LiveTrader
from exchange.bitget import get_symbol_rules


def main():
    live = LiveTrader()

    print("\n===== ACCOUNT =====")
    live.get_account_info()

    print("\n===== POSITIONS =====")
    live.get_open_positions()

    print("\n===== BTC RULES =====")
    rules = get_symbol_rules("BTCUSDT")
    print(rules)


if __name__ == "__main__":
    main()