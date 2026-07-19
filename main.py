import time

from exchange.bitget import get_candles
from indicators.ema import calculate_ema
from indicators.atr import calculate_atr
from indicators.rsi import calculate_rsi

from strategy.signal_engine import generate_signal
from strategy.setup_detector import detect_setup
from strategy.confidence import confidence_score

from telegram.telegram_bot import send_message


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

send_message("🤖 JshScalpingBot Scanner Started")


while True:

    print("\n" + "=" * 50)
    print("🔍 New Market Scan")
    print("=" * 50)

    for pair in PAIRS:

        candles = get_candles(pair)["data"]

        closes = [float(c[4]) for c in candles]
        highs = [float(c[2]) for c in candles]
        lows = [float(c[3]) for c in candles]

        # Indicators
        ema9 = calculate_ema(closes, 9)
        ema21 = calculate_ema(closes, 21)
        ema50 = calculate_ema(closes, 50)

        atr = calculate_atr(highs, lows, closes)
        rsi = calculate_rsi(closes)

        # Current signal
        signal = generate_signal(
            ema9,
            ema21,
            ema50,
            atr,
            rsi
        )

        # Setup detector
        setup = detect_setup(
            ema9,
            ema21,
            ema50,
            rsi,
            atr
        )

        # Confidence score
        score = confidence_score(
            ema9,
            ema21,
            ema50,
            rsi,
            atr
        )

        print(f"\n{'=' * 50}")
        print(pair)
        print(f"{'=' * 50}")

        print(signal)
        print(f"Setup      : {setup}")
        print(f"Confidence : {score}%")

        # Telegram alert
        if score >= 80:
            message = (
                f"🚨 {pair}\n\n"
                f"{setup}\n\n"
                f"{signal}\n\n"
                f"Confidence: {score}%"
            )

            send_message(message)

    print("\n⏳ Waiting 30 seconds...\n")

    time.sleep(30)