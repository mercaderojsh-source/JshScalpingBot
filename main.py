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

    for pair in PAIRS:
        data = get_ticker(pair)
        print(pair)
        print(data)
        print("-" * 40)


if __name__ == "__main__":
    main()