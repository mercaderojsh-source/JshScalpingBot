import time

from trading.live_trader import LiveTrader
from exchange.bitget import (
    get_symbol_rules,
    set_leverage,
    place_market_order,
    place_stop_loss,
    place_take_profit,
)
from config import LEVERAGE


def main():
    live = LiveTrader()

    print("********** TEST FILE IS RUNNING **********")

    print("\n===== ACCOUNT =====")
    live.get_account_info()

    print("\n===== POSITIONS =====")
    live.get_open_positions()

    print("\n===== BTC RULES =====")
    rules = get_symbol_rules("BTCUSDT")
    print(rules)

    print("\n===== SET LEVERAGE =====")
    response = set_leverage("BTCUSDT", LEVERAGE)
    print(response)

    print("\n===== TEST MARKET ORDER =====")

    try:
        response = place_market_order(
            symbol="BTCUSDT",
            side="buy",
            size=0.0001
        )
        print(response)

        # Give Bitget time to register the new position
        time.sleep(3)

        print("\n===== VERIFY POSITION =====")
        live.get_open_positions()

        print("\n===== ATTACH STOP LOSS =====")

        # Test stop loss (below current BTC price for a long)
        stop_loss_price = 50000

        response = place_stop_loss(
            symbol="BTCUSDT",
            hold_side="long",
            stop_loss=stop_loss_price
        )

        print(response)

        print("\n===== ATTACH TAKE PROFIT =====")

        # Test take profit (above current BTC price for a long)
        take_profit_price = 70000

        response = place_take_profit(
            symbol="BTCUSDT",
            hold_side="long",
            take_profit=take_profit_price
        )

        print(response)

        print("\n===== FINAL POSITION =====")
        live.get_open_positions()

    except Exception as e:
        print("EXCEPTION:", e)


if __name__ == "__main__":
    main()