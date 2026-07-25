import os
import time
from trading.performance import performance_summary

from config import (
    PAIRS,
    SCAN_INTERVAL,
    LIVE_TRADING,
)

from intelligence.momentum import momentum_score
from intelligence.quality import quality_score
from intelligence.opportunity import opportunity_score
from intelligence.memory import remember
from intelligence.brain import intelligence_score

from exchange.bitget import get_candles

from indicators.ema import calculate_ema
from indicators.atr import calculate_atr
from indicators.rsi import calculate_rsi

from strategy.signal_engine import generate_signal
from strategy.setup_detector import detect_setup
from strategy.confidence import confidence_score
from strategy.trend_strength import trend_strength
from strategy.score_engine import final_score
from strategy.confirmation import confirm_entry
from strategy.timeframe_filter import higher_timeframe_trend

from scanner.volatility_ranker import volatility_score
from scanner.market_state import market_state

from trading.paper_trader import PaperTrader
from trading.live_trader import LiveTrader
from trading.trade_journal import TradeJournal

from telegram.telegram_bot import send_message


if LIVE_TRADING:
    trader = LiveTrader()
    print("🟢 LIVE TRADING ENABLED")
else:
    trader = PaperTrader()
    print("🟡 PAPER TRADING ENABLED")

journal = TradeJournal()

stats = performance_summary()

print("\n📊 Historical Performance")
print(f"Trades   : {stats['trades']}")
print(f"Wins     : {stats['wins']}")
print(f"Losses   : {stats['losses']}")
print(f"Win Rate : {stats['win_rate']}%")
print(f"Net PnL  : ${stats['net_profit']}")
print("-" * 60)

print("Journal File :", os.path.abspath(journal.filename))
print("Journal Exists :", os.path.exists(journal.filename))

print("=" * 60)
print("🚀 JshScalpingBot Intelligent Scanner")
print("=" * 60)

if os.path.exists(journal.filename):
    print("\n===== trade_history.csv =====")

    with open(journal.filename, "r") as f:
        for i, line in enumerate(f):
            print(line.strip())

            if i >= 10:
                break

    print("=============================\n")

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

        # Updated to pass price for percentage-based normalized metrics
        signal = generate_signal(
            ema9,
            ema21,
            ema50,
            atr,
            rsi,
            price
        )

        setup = detect_setup(
            ema9,
            ema21,
            ema50,
            rsi,
            price
        )

        confidence = confidence_score(
            ema9,
            ema21,
            ema50,
            rsi,
            atr
        )

        trend = trend_strength(
            ema9,
            ema21,
            ema50,
            price
        )

        print(
            f"{pair} | EMA Gap %: "
            f"{((abs(ema9-ema21)+abs(ema21-ema50))/price)*100:.4f}% "
            f"| Trend Score: {trend}"
        )

        state = market_state(
            ema9,
            ema21,
            ema50,
            atr,
            rsi
        )

        htf = higher_timeframe_trend(pair)

        vol = volatility_score(
            atr,
            price
        )

        atr_percent = (atr / price) * 100

        momentum = momentum_score(
            trend,
            atr_percent,
            ema9,
            ema21,
            ema50,
            price
        )

        previous_momentum, momentum_change = remember(pair, momentum)

        print(
             f"{pair} | "
             f"Trend={trend}/20 | "
             f"ATR={atr_percent:.2f}% | "
             f"Momentum={momentum} | "
             f"ΔMomentum={momentum_change:+.1f}"
        )

        quality = quality_score(
            confidence,
            setup,
            htf["trend"]
        )

        score = opportunity_score(
            momentum,
            quality,
            vol
        )

        results.append({
            "pair": pair,
            "price": price,
            "atr": atr,
            "atr_percent": atr_percent,
            "rsi": rsi,
            "signal": signal,
            "setup": setup,
            "confidence": confidence,
            "trend_strength": trend,
            "volatility_score": vol,
            "market_state": state,
            "higher_timeframe": htf["trend"],
            "momentum": momentum,
            "quality": quality,
            "opportunity": score,
            "score": score
        })

        results[-1]["brain_score"] = intelligence_score(results[-1])
        results[-1]["score"] = results[-1]["brain_score"]

    if not results:
        print("⚠️ No market data received.")
        time.sleep(SCAN_INTERVAL)
        continue

    ranked = sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )

    # -----------------------------
    # Check active trade
    # -----------------------------
    if (
        not LIVE_TRADING
        and trader.position is not None
    ):

        active_pair = trader.position["pair"]

        for item in ranked:

            if item["pair"] != active_pair:
                continue

            # -----------------------------
            # Manage trade
            # -----------------------------
            event = trader.manage_trade(item["price"])

            # Break-even
            if event == "BREAK_EVEN":

                print(f"🛡 Break-even activated for {trader.position['pair']}")

                send_message(
                    f"🛡 BREAK-EVEN ACTIVATED\n\n"
                    f"Pair : {trader.position['pair']}\n"
                    f"New Stop : {trader.position['stop_loss']:.4f}"
                )

            # Partial TP / Trailing Stop
            elif isinstance(event, dict):

                if event.get("event") == "PARTIAL_TP":

                    print(f"💵 Partial Take Profit for {event['pair']}")

                    send_message(
                        f"💵 PARTIAL TAKE PROFIT\n\n"
                        f"Pair : {event['pair']}\n"
                        f"Realized PnL : ${event['pnl']:.2f}\n"
                        f"Remaining Size : {event['remaining_size']:.6f}\n"
                        f"Balance : ${event['balance']:.2f}"
                    )

                elif event.get("event") == "TRAILING_STOP":

                    print(f"📈 Trailing Stop Updated for {event['pair']}")

                    send_message(
                        f"📈 TRAILING STOP UPDATED\n\n"
                        f"Pair : {event['pair']}\n"
                        f"New Stop : {event['stop_loss']:.4f}"
                    )

            # -----------------------------
            # Exit Check
            # -----------------------------
            exit_signal = trader.check_exit(item["price"])

            print(f"Exit Signal: {exit_signal}")

            if exit_signal:

                trade = trader.close_trade(item["price"])

                journal.log_trade(
                    trade=trade,
                    context=trade.get("context", {}),
                    exit_reason=exit_signal
                )

                send_message(
                    f"💰 PAPER TRADE CLOSED\n\n"
                    f"{trade['pair']}\n"
                    f"Exit : {exit_signal}\n"
                    f"PnL  : {round(trade['pnl'], 2)}\n"
                    f"Balance : ${trade['balance']:.2f}"
                )

            break

    # -----------------------------
    # Print rankings
    # -----------------------------
    print("\n🔥 TOP OPPORTUNITIES\n")

    for index, item in enumerate(ranked, start=1):

        print(f"{index}. {item['pair']}")
        print(f"   State      : {item['market_state']}")
        print(f"   HTF        : {item['higher_timeframe']}")
        print(f"   Setup      : {item['setup']}")
        print(f"   Confidence : {item['confidence']}%")
        print(f"   Trend      : {item['trend_strength']}")
        print(f"   Momentum   : {item['momentum']}")
        print(f"   Quality    : {item['quality']}")
        print(f"   Volatility : {item['volatility_score']}")
        print(f"   Brain      : {item['brain_score']:.1f}")
        print()

    # -----------------------------
    # Open new trade
    # -----------------------------
    if (
        (not LIVE_TRADING and trader.position is None)
        or LIVE_TRADING
    ):

        trade_found = False

        for best in ranked:

            # Skip pairs in cooldown (PaperTrader only)
            if not LIVE_TRADING:

                if trader.in_cooldown(best["pair"]):

                    print(
                        f"⏳ {best['pair']} still in cooldown..."
                    )

                    continue

            # Skip WATCHLIST setups
            if "WATCHLIST" in best["setup"]:
                continue

            # ----------------------------------------------------
            # HARD FILTER: Never trade against Higher Timeframe
            # ----------------------------------------------------
            htf_trend = str(best["higher_timeframe"]).upper()

            if "BUY" in best["setup"] and "BULL" not in htf_trend:
                print(f"🚫 Skipped BUY on {best['pair']}: HTF Trend is {htf_trend}")
                continue

            if "SELL" in best["setup"] and "BEAR" not in htf_trend:
                print(f"🚫 Skipped SELL on {best['pair']}: HTF Trend is {htf_trend}")
                continue

            print("\n🎯 CHECKING SETUP")
            print(f"Pair        : {best['pair']}")
            print(f"State       : {best['market_state']}")
            print(f"HTF         : {best['higher_timeframe']}")
            print(f"Setup       : {best['setup']}")
            print(f"Momentum    : {best['momentum']}")
            print(f"Quality     : {best['quality']}")
            print(f"Brain Score : {best['brain_score']:.1f}")
            print(f"RSI         : {best['rsi']:.2f}")
            print(f"ATR %       : {best['atr_percent']:.2f}%")

            if not confirm_entry(
                setup=best["setup"],
                market_state=best["market_state"],
                score=best["score"],
                rsi=best["rsi"],
                atr_percent=best["atr_percent"]
            ):
                continue

            direction = "BUY"

            if "SELL" in best["setup"]:
                direction = "SELL"

            trade = trader.execute_trade(
                best["pair"],
                direction,
                best["price"],
                best["atr"],
                context=best
            )

            if not trade:
                continue

            print(
                f"\n✅ OPENED {trade['direction']} "
                f"{trade['pair']} @ {trade['entry']:.4f}"
            )

            mode = "LIVE" if LIVE_TRADING else "PAPER"

            send_message(
                f"📈 {mode} TRADE OPEN\n\n"
                f"Pair : {trade['pair']}\n"
                f"Side : {trade['direction']}\n"
                f"HTF  : {best['higher_timeframe']}\n"
                f"Entry : {trade['entry']:.4f}\n"
                f"ATR   : {trade['atr']:.4f}\n"
                f"SL    : {trade['stop_loss']:.4f}\n"
                f"TP    : {trade['take_profit']:.4f}\n"
                f"Size  : {trade['size']:.6f}\n"
                f"Score : {best['score']}"
            )

            trade_found = True
            break

        if not trade_found:
            print("\n❌ No valid trade found this scan.")

    # -----------------------------
    # Account Statistics
    # -----------------------------
    if not LIVE_TRADING:

        stats = trader.stats()

        print("\n📊 PAPER ACCOUNT")
        print(f"Balance : ${stats['balance']:.2f}")
        print(f"Trades  : {stats['trades']}")
        print(f"Wins    : {stats['wins']}")
        print(f"Losses  : {stats['losses']}")
        print(f"WinRate : {stats['win_rate']}%")

        # Show active cooldowns
        if stats.get("cooldowns"):

            print("\n⏳ ACTIVE COOLDOWNS")

            for pair, seconds in stats["cooldowns"].items():

                mins = seconds // 60
                secs = seconds % 60

                print(f"{pair} : {mins}m {secs}s")

        if trader.position is not None:

            print("\n📌 ACTIVE POSITION")
            print(f"Pair      : {trader.position['pair']}")
            print(f"Side      : {trader.position['direction']}")
            print(f"Entry     : {trader.position['entry']:.4f}")
            print(f"Stop Loss : {trader.position['stop_loss']:.4f}")
            print(f"TakeProfit: {trader.position['take_profit']:.4f}")

            if trader.position["break_even"]:
                print("Mode      : BREAK-EVEN")

            if trader.position["partial_taken"]:
                print("Mode      : TRAILING")

        else:
            print("\n📌 No Active Position")

    else:

        print("\n📊 LIVE TRADING MODE")

        positions = trader.get_open_positions()

        if positions:
            print(f"Open Positions : {len(positions)}")
        else:
            print("No Active Positions")

    print(f"\n⏳ Waiting {SCAN_INTERVAL} seconds...\n")

    time.sleep(SCAN_INTERVAL)
