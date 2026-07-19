import time

from config import (
    PAIRS,
    SCAN_INTERVAL,
    MIN_SCORE,
)

from exchange.bitget import get_candles

from indicators.ema import calculate_ema
from indicators.atr import calculate_atr
from indicators.rsi import calculate_rsi

from strategy.signal_engine import generate_signal
from strategy.setup_detector import detect_setup
from strategy.confidence import confidence_score
from strategy.score_engine import final_score

from scanner.volatility_ranker import volatility_score
from scanner.market_state import market_state

from trading.paper_trader import PaperTrader
from trading.trade_journal import TradeJournal

from telegram.telegram_bot import send_message


trader = PaperTrader()
journal = TradeJournal()

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

        state = market_state(
            ema9,
            ema21,
            ema50,
            atr,
            rsi
        )

        vol = volatility_score(
            atr,
            price
        )

        score = final_score(
            confidence,
            vol,
            state,
            setup
        )

        results.append({
            "pair": pair,
            "price": price,
            "atr": atr,
            "signal": signal,
            "setup": setup,
            "confidence": confidence,
            "volatility_score": vol,
            "market_state": state,
            "score": score
        })

    if not results:
        print("⚠️ No market data received.")
        time.sleep(SCAN_INTERVAL)
        continue

    # -----------------------------
    # Rank by overall score
    # -----------------------------
    ranked = sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )

    # -----------------------------
    # Check active paper trade
    # -----------------------------
    if trader.position is not None:

        active_pair = trader.position["pair"]

        for item in ranked:

            if item["pair"] == active_pair:

                exit_signal = trader.check_exit(item["price"])

                if exit_signal:

                    trade = trader.close_trade(item["price"])

                    journal.log_trade(
                        pair=trade["pair"],
                        direction=trade["direction"],
                        entry=trade["entry"],
                        exit_price=trade["exit"],
                        pnl=trade["pnl"],
                        reason=exit_signal,
                        balance=trade["balance"]
                    )

                    send_message(
                        f"💰 PAPER TRADE CLOSED\n\n"
                        f"{trade['pair']}\n"
                        f"Exit: {exit_signal}\n"
                        f"PnL: {round(trade['pnl'], 2)}\n"
                        f"Balance: ${trade['balance']:.2f}"
                    )

                break

    # -----------------------------
    # Print rankings
    # -----------------------------
    print("\n🔥 TOP OPPORTUNITIES\n")

    for index, item in enumerate(ranked, start=1):

        print(f"{index}. {item['pair']}")
        print(f"   State : {item['market_state']}")
        print(f"   Setup : {item['setup']}")
        print(f"   Conf  : {item['confidence']}%")
        print(f"   Vol   : {item['volatility_score']}")
        print(f"   Score : {item['score']}")
        print()

    # -----------------------------
    # Open new paper trade
    # -----------------------------
    if trader.position is None:

        best = ranked[0]

        if (
            best["score"] >= MIN_SCORE
            and "WATCHLIST" not in best["setup"]
            and best["market_state"] not in ["🌊 RANGING", "😴 QUIET"]
        ):

            direction = "BUY"

            if "SELL" in best["setup"]:
                direction = "SELL"

            trade = trader.open_trade(
                best["pair"],
                direction,
                best["price"],
                best["atr"]
            )

            send_message(
                f"📈 PAPER TRADE OPEN\n\n"
                f"Pair : {trade['pair']}\n"
                f"Side : {trade['direction']}\n"
                f"Entry: {trade['entry']:.4f}\n"
                f"ATR  : {trade['atr']:.4f}\n"
                f"SL   : {trade['stop_loss']:.4f}\n"
                f"TP   : {trade['take_profit']:.4f}\n"
                f"Size : {trade['size']:.6f}\n"
                f"Score: {best['score']}"
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