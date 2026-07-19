from exchange.bitget import get_candles
from indicators.ema import calculate_ema
from indicators.atr import calculate_atr
from indicators.rsi import calculate_rsi
from strategy.signal_engine import generate_signal

PAIRS = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "XRPUSDT",
    "BGBUSDT"
]

print("=" * 50)
print("🚀 JshScalpingBot Multi-Pair Scanner")
print("=" * 50)

for pair in PAIRS:

    candles = get_candles(pair)

    if candles["code"] != "00000":
        print(pair, "ERROR")
        continue

    closes = [float(c[4]) for c in candles["data"]]
    highs = [float(c[2]) for c in candles["data"]]
    lows = [float(c[3]) for c in candles["data"]]

    ema9 = calculate_ema(closes, 9)
    ema21 = calculate_ema(closes, 21)
    ema50 = calculate_ema(closes, 50)

    atr = calculate_atr(highs, lows, closes)
    rsi = calculate_rsi(closes)

    score, reasons = generate_signal(
        ema9,
        ema21,
        ema50,
        atr,
        rsi
    )

    print()
    print("=" * 40)
    print(pair)
    print("=" * 40)

    print(f"Score : {score}/3")

    for reason in reasons:
        print(reason)

    if score == 3:
        print("🚀 STRONG SETUP")

    elif score == 2:
        print("👀 WATCHLIST")

    else:
        print("⛔ NO TRADE")