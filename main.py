import time

from exchange.bitget import get_candles

from indicators.ema import calculate_ema
from indicators.atr import calculate_atr
from indicators.rsi import calculate_rsi

from strategy.signal_engine import generate_signal
from strategy.setup_detector import detect_setup
from strategy.confidence import confidence_score

from scanner.volatility_ranker import volatility_score, rank_pairs

from trading.paper_trader import PaperTrader

from telegram.telegram_bot import send_message


PAIRS = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "XRPUSDT",
    "BGBUSDT"
]

SCAN_INTERVAL = 30

trader = PaperTrader()

print("=" * 60)
print("🚀 JshScalpingBot Intelligent Scanner")
print("=" * 60)

send_message("🤖 JshScalpingBot Started")


while True:

    print("\n" + "=" * 60)
    print("🔍 New Market Scan")
    print("=" * 60)

    results = []

    # -----------------------------
    # Scan all pairs
    # -----------------------------
    for pair in PAIRS:

        response = get_candles(pair)

        if response.get("code") != "00000":
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

        vol = volatility_score(
            atr,
            price
        )

        results.append({
            "pair": pair,
            "price": price,
            "signal": signal,
            "setup": setup,
            "confidence": confidence,
            "volatility_score": vol
        })

    # Safety check
    if not results:
        print("⚠️ No market data received.")
        time.sleep(SCAN_INTERVAL)
        continue

    ranked = rank_pairs(results)

    # -----------------------------
    # Check active paper trade
    # -----------------------------
    if trader.position is not None:

        active_pair = trader.position["pair"]

        for item in ranked:

            if item["pair"] == active_pair:

                exit_signal = trader.check_exit(item["price"])

                if exit_signal:

                    pnl = trader.close_trade(item["price"])

                    send_message(
                        f"💰 PAPER TRADE CLOSED\n\n"
                        f"{active_pair}\n"
                        f"Exit: {exit_signal}\n"
                        f"PnL: {round(pnl,2)}\n"
                        f"Balance: ${trader.balance:.2f}"
                    )

                break

    # -----------------------------
    # Print rankings
    # -----------------------------
    print("\n🔥 TOP OPPORTUNITIES\n")

    for index, item in enumerate(ranked, start=1):

        print(
            f"{index}. {item['pair']} | "
            f"{item['setup']} | "
            f"Conf: {item['confidence']}% | "
            f"Vol: {item['volatility_score']}"
        )

    # -----------------------------
    # Open new paper trade
    # -----------------------------
    if trader.position is None:

        best = ranked[0]

        if best["confidence"] >= 40:

            direction = "BUY"

            if "SELL" in best["setup"]:
                direction = "SELL"

            trader.open_trade(
                best["pair"],
                direction,
                best["price"]
            )

            send_message(
                f"📈 PAPER TRADE OPEN\n\n"
                f"{best['pair']}\n"
                f"{direction}\n"
                f"Entry: {best['price']}"
            )

    # -----------------------------
    # Account Stats
    # -----------------------------
    stats = trader.stats()

    print("\n📊 PAPER ACCOUNT")
    print(f"Balance : ${stats['balance']}")
    print(f"Trades  : {stats['trades']}")
    print(f"Wins    : {stats['wins']}")
    print(f"Losses  : {stats['losses']}")
    print(f"WinRate : {stats['win_rate']}%")

    print(f"\n⏳ Waiting {SCAN_INTERVAL} seconds...\n")

    time.sleep(SCAN_INTERVAL)