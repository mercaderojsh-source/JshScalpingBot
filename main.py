from exchange.bitget import get_candles
from indicators.ema import calculate_ema
from indicators.atr import calculate_atr
from indicators.rsi import calculate_rsi
from strategy.signal_engine import generate_signal

print("=" * 40)
print("🚀 SIGNAL ENGINE")
print("=" * 40)

candles = get_candles("BTCUSDT")

if candles["code"] == "00000":

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
    print("Signal Score:", score, "/3")
    print()

    for reason in reasons:
        print(reason)

    print()

    if score == 3:
        print("🚀 STRONG TRADE SETUP")
    elif score == 2:
        print("👀 WATCHLIST")
    else:
        print("⛔ NO TRADE")