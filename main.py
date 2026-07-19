import time

from exchange.bitget import get_candles

from indicators.ema import calculate_ema
from indicators.atr import calculate_atr
from indicators.rsi import calculate_rsi

from strategy.signal_engine import generate_signal
from strategy.setup_detector import detect_setup
from strategy.confidence import confidence_score

from scanner.volatility_ranker import (
    volatility_score,
    rank_pairs,
)

from trading.paper_trader import PaperTrader

from telegram.telegram_bot import send_message


PAIRS = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "XRPUSDT",
    "BGBUSDT"
]

# Create the paper trader
trader = PaperTrader()

print("=" * 60)
print("🚀 JshScalpingBot Intelligent Scanner")
print("=" * 60)

send_message("🤖 JshScalpingBot Intelligent Scanner Started")

while True:

    print("\n" + "=" * 60)
    print("🔍 New Market Scan")
    print("=" * 60)

    results = []

    for pair in PAIRS:

        response = get_candles(pair)

        if response["code"] != "00000":
            continue

        candles = response["data"]

        closes = [float(c[4]) for c in candles]
        highs = [float(c[2]) for c in candles]
        lows = [float(c[3]) for c in candles]

        price = closes[-1]

        ema9 = calculate_ema(closes, 9)
        ema21 = calculate_ema(closes, 21)
        ema50 = calculate_ema(closes, 50)

        atr = calculate_atr(highs, lows, closes)
        rsi = calculate_rsi(closes)

        signal = generate_signal(
            ema9,
            ema21,
            ema50,
            atr,
            rsi
        )

        setup = detect_setup(
            ema9,
            ema21,
            ema50,
            rsi,
            atr
        )

        confidence = confidence_score(
            ema9,
            ema21,
            ema50,
            rsi,
            atr
        )

        vol_score = volatility_score(
            atr,
            price
        )

        results.append({
            "pair": pair,
            "price": price,
            "signal": signal,
            "setup": setup,
            "confidence": confidence,
            "volatility_score": vol_score
        })

    ranked = rank_pairs(results)

    print("\n🔥 TOP OPPORTUNITIES\n")

    for index, item in enumerate(ranked, start=1):

        print(f"{index}. {item['pair']}")
        print(f"   Setup       : {item['setup']}")
        print(f"   Confidence  : {item['confidence']}%")
        print(f"   Volatility  : {item['volatility_score']}")
        print()

        if (
            trader.position is None
            and item["confidence"] >= 80
        ):

            direction = "BUY"

            if "SELL" in item["setup"]:
                direction = "SELL"

            trader.open_trade(
                item["pair"],
                direction,
                item["price"]
            )

            send_message(
                f"📈 PAPER TRADE OPEN\n\n"
                f"{item['pair']}\n"
                f"{direction}\n"
                f"Entry: {item['price']}"
            )

        elif (
            item["confidence"] >= 80
            and item["volatility_score"] >= 5
        ):

            send_message(
                f"🔥 TOP SCALPING SETUP\n\n"
                f"{item['pair']}\n\n"
                f"{item['setup']}\n"
                f"Confidence: {item['confidence']}%\n"
                f"Volatility: {item['volatility_score']}"
            )

    stats = trader.stats()

    print("=" * 60)
    print("📊 PAPER ACCOUNT")
    print("=" * 60)
    print(f"Balance : ${stats['balance']}")
    print(f"Trades  : {stats['trades']}")
    print(f"Wins    : {stats['wins']}")
    print(f"Losses  : {stats['losses']}")
    print(f"WinRate : {stats['win_rate']}%")

    print("\n⏳ Waiting 30 seconds...\n")

    time.sleep(30)