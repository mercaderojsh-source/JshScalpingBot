import time
from exchange.bitget import get_ticker

PAIRS = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "XRPUSDT",
    "BGBUSDT"
]


def main():
    print("=" * 40)
    print("🚀 JshScalpingBot Started")
    print("=" * 40)

    while True:
        for pair in PAIRS:
            data = get_ticker(pair)

            if data["code"] == "00000":
                price = data["data"][0]["lastPr"]
                print(f"{pair}: {price}")
            else:
                print(f"{pair}: ERROR")

        print("-" * 40)
        time.sleep(1)


if __name__ == "__main__":
    main()