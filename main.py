import time

from scanner.scanner import scan_market
from telegram.telegram_bot import send_message


def main():

    print("=" * 40)
    print("🚀 JshScalpingBot Started")
    print("=" * 40)

    send_message("🚀 JshScalpingBot Scanner Started")

    while True:

        market = scan_market()

        for pair, info in market.items():

            print(
                f"{pair} | "
                f"Price: {info['price']} | "
                f"24h: {info['change']:.2%} | "
                f"Volume: {info['volume']:.0f}"
            )

        print("-" * 60)

        time.sleep(5)


if __name__ == "__main__":
    main()