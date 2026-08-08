import os
import time
import traceback
from datetime import datetime, timezone
from trading.performance import performance_summary, log_trade_result

import config
from config import (
    PAIRS,
    SCAN_INTERVAL,
    LIVE_TRADING,
    MIN_SCORE,
    REQUIRE_STRONG_BUY,
    MIN_TREND_SCORE,
    MAX_OPEN_POSITIONS,
    ENABLE_RANGE_MODE,
)

from intelligence.momentum import momentum_score
from intelligence.quality import quality_score
from intelligence.opportunity import opportunity_score
from intelligence.memory import remember
from intelligence.brain import intelligence_score
from intelligence.self_learning import apply_self_learning_adjustment

from exchange.bitget import get_candles, get_positions

from indicators.ema import calculate_ema
from indicators.atr import calculate_atr
from indicators.rsi import calculate_rsi

from strategy.signal_engine import generate_signal
from strategy.setup_detector import detect_setup
from strategy.range_engine import detect_range_setup
from strategy.confidence import confidence_score
from strategy.trend_strength import trend_strength
from strategy.timeframe_filter import higher_timeframe_trend

from scanner.volatility_ranker import volatility_score
from scanner.market_state import market_state

from trading.paper_trader import PaperTrader
from trading.live_trader import LiveTrader
from trading.trade_journal import TradeJournal

from telegram.telegram_bot import send_message

# Dynamic Feature Toggles
ENABLE_SESSION_FILTER = getattr(config, "ENABLE_SESSION_FILTER", False)
ENABLE_PYRAMIDING = getattr(config, "ENABLE_PYRAMIDING", False)
PYRAMID_PROFIT_ATR = getattr(config, "PYRAMID_PROFIT_ATR", 1.0)


def is_liquidity_window_active():
    """Returns True if current UTC time falls within peak liquidity trading hours."""
    now_utc = datetime.now(timezone.utc).time()

    # Session 1: London Open (07:00 - 10:00 UTC)
    london_start = datetime.strptime("07:00", "%H:%M").time()
    london_end = datetime.strptime("10:00", "%H:%M").time()

    # Session 2: London / New York Overlap (13:00 - 17:00 UTC)
    ny_start = datetime.strptime("13:00", "%H:%M").time()
    ny_end = datetime.strptime("17:00", "%H:%M").time()

    is_london = (london_start <= now_utc <= london_end)
    is_ny_overlap = (ny_start <= now_utc <= ny_end)

    return is_london or is_ny_overlap


if LIVE_TRADING:
    trader = LiveTrader()
    print("🟢 LIVE TRADING ENABLED")
else:
    trader = PaperTrader()
    print("🟡 PAPER TRADING ENABLED")

journal = TradeJournal()

# Track active live position in memory for exit detection
active_tracked_trade = None

stats = performance_summary()

print("\n📊 Historical Performance")
print(f"Trades   : {stats.get('trades', 0)}")
print(f"Wins     : {stats.get('wins', 0)}")
print(f"Losses   : {stats.get('losses', 0)}")
print(f"Win Rate : {stats.get('win_rate', 0)}%")
print(f"Net PnL  : ${stats.get('net_profit', 0)}")
print("-" * 60)

mode_label = "LIVE TRADING" if LIVE_TRADING else "PAPER TRADING"
send_message(f"🤖 JshScalpingBot Started [{mode_label}]")

while True:
    try:
        print("\n" + "=" * 60)
        print("🔍 New Market Scan")
        print("=" * 60)

        # ----------------------------------------------------
        # 1. POSITION MONITORING & EXITED TRADE DETECTION
        # ----------------------------------------------------
        current_positions = trader.get_open_positions() if LIVE_TRADING else ([] if trader.position is None else [trader.position])

        # If a trade was active but is no longer open in Bitget, it closed (TP/SL hit)
        if active_tracked_trade and not current_positions:
            print("\n🏁 DETECTED CLOSED TRADE! Processing stats and alert...")

            pair = active_tracked_trade["pair"]
            entry = active_tracked_trade["entry"]
            direction = active_tracked_trade["direction"]
            tp = active_tracked_trade["take_profit"]
            sl = active_tracked_trade["stop_loss"]

            # Fetch current mark price to evaluate exit zone
            ticker_data = get_candles(pair)
            exit_price = entry
            if ticker_data and ticker_data.get("code") == "00000":
                exit_price = float(ticker_data["data"][-1][4])

            # Evaluate Win vs Loss
            is_win = False
            if direction == "BUY":
                is_win = exit_price >= (entry + (tp - entry) * 0.5)
            else:
                is_win = exit_price <= (entry - (entry - tp) * 0.5)

            result_str = "WIN ✅" if is_win else "LOSS ❌"

            # Log result & get updated performance stats
            try:
                log_trade_result(pair=pair, direction=direction, entry=entry, exit_price=exit_price, win=is_win)
            except Exception as log_err:
                print(f"⚠️ Could not update performance log file: {log_err}")

            updated_stats = performance_summary()

            # Telegram Notification
            send_message(
                f"🏁 {mode_label} TRADE CLOSED\n\n"
                f"Pair   : {pair}\n"
                f"Side   : {direction}\n"
                f"Result : {result_str}\n"
                f"Entry  : {entry}\n"
                f"Exit   : {exit_price:.4f}\n"
                f"TP/SL  : {tp} / {sl}\n\n"
                f"📊 UPDATED SCOREBOARD\n"
                f"Total Trades : {updated_stats.get('trades', 0)}\n"
                f"Wins / Losses: {updated_stats.get('wins', 0)} W / {updated_stats.get('losses', 0)} L\n"
                f"Win Rate     : {updated_stats.get('win_rate', 0)}%\n"
                f"Net Profit   : ${updated_stats.get('net_profit', 0)}"
            )

            # Reset active position tracking
            active_tracked_trade = None

        # ----------------------------------------------------
        # 2. SESSION LIQUIDITY CHECK
        # ----------------------------------------------------
        if ENABLE_SESSION_FILTER and not is_liquidity_window_active():
            print("💤 Outside peak liquidity window (London 07:00-10:00 UTC / NY 13:00-17:00 UTC). Skipping entries.")
            time.sleep(SCAN_INTERVAL)
            continue

        # ----------------------------------------------------
        # 3. MARKET SCANNING
        # ----------------------------------------------------
        results = []

        for pair in PAIRS:
            try:
                response = get_candles(pair)

                if not response or response.get("code") != "00000":
                    continue

                candles = response.get("data", [])
                if len(candles) < 50:
                    continue

                closes = [float(c[4]) for c in candles]
                highs = [float(c[2]) for c in candles]
                lows = [float(c[3]) for c in candles]

                price = closes[-1]

                ema9 = calculate_ema(closes, 9)
                ema21 = calculate_ema(closes, 21)
                ema50 = calculate_ema(closes, 50)

                atr = calculate_atr(highs, lows, closes)
                rsi = calculate_rsi(closes)

                signal = generate_signal(ema9, ema21, ema50, atr, rsi, price)
                setup = detect_setup(ema9, ema21, ema50, rsi, price)
                confidence = confidence_score(ema9, ema21, ema50, rsi, atr)
                trend = trend_strength(ema9, ema21, ema50, price)
                state = market_state(ema9, ema21, ema50, atr, rsi)
                htf = higher_timeframe_trend(pair)
                vol = volatility_score(atr, price)

                atr_percent = (atr / price) * 100

                if ENABLE_RANGE_MODE and ("WATCHLIST" in setup or trend < MIN_TREND_SCORE):
                    range_setup = detect_range_setup(
                        closes=closes,
                        price=price,
                        rsi=rsi,
                        trend_score=trend,
                        min_trend_score=MIN_TREND_SCORE
                    )
                    if range_setup != "NO_SETUP":
                        setup = range_setup

                momentum = momentum_score(trend, atr_percent, ema9, ema21, ema50, price)
                previous_momentum, momentum_change = remember(pair, momentum)
                quality = quality_score(confidence, setup, htf["trend"])
                score = opportunity_score(momentum, quality, vol)

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

                base_brain_score = intelligence_score(results[-1])
                direction_label = "BUY" if "BUY" in str(results[-1]["setup"]).upper() else "SELL"

                # Dynamic Self-Learning Reinforcement Adjustment
                results[-1]["brain_score"] = apply_self_learning_adjustment(
                    base_score=base_brain_score,
                    direction=direction_label,
                    context=results[-1]
                )
                results[-1]["score"] = results[-1]["brain_score"]

            except Exception as pair_err:
                print(f"⚠️ Error scanning pair {pair}: {pair_err}")
                continue

        if not results:
            print("⚠️ No market data received.")
            time.sleep(SCAN_INTERVAL)
            continue

        ranked = sorted(results, key=lambda x: x["score"], reverse=True)

        # ----------------------------------------------------
        # 4. ENTRY EXECUTION & PYRAMIDING CHECK
        # ----------------------------------------------------
        can_open_trade = False

        if not LIVE_TRADING:
            can_open_trade = (trader.position is None)
        else:
            num_positions = len(current_positions)

            if num_positions == 0:
                can_open_trade = True
            elif num_positions == 1 and ENABLE_PYRAMIDING:
                pos = current_positions[0]
                entry_p = float(pos.get("openPriceAvg", 0))
                mark_p = float(pos.get("markPrice", entry_p))
                hold_side = str(pos.get("holdSide", "")).upper()

                # Calculate current profit in price distance
                price_gain = (mark_p - entry_p) if hold_side in ["LONG", "BUY"] else (entry_p - mark_p)
                min_required_gain = ranked[0]["atr"] * PYRAMID_PROFIT_ATR

                if price_gain >= min_required_gain:
                    print(f"🔥 Pyramiding Triggered! Position 1 gain (+{price_gain:.2f}) >= required (+{min_required_gain:.2f}). Scanning for follow-up entry...")
                    can_open_trade = True
                else:
                    print(f"📌 Position 1 active (+{price_gain:.2f}). Waiting for +{min_required_gain:.2f} gain before pyramiding.")
            else:
                print(f"📌 Max positions reached ({num_positions}/{MAX_OPEN_POSITIONS}). Skipping entry scan.")

        if can_open_trade:

            trade_found = False

            for best in ranked:

                if "WATCHLIST" in best["setup"]:
                    continue

                if REQUIRE_STRONG_BUY and "STRONG" not in str(best["setup"]).upper():
                    continue

                if best["brain_score"] < MIN_SCORE:
                    continue

                htf_trend = str(best["higher_timeframe"]).upper()

                if "BUY" in str(best["setup"]).upper() and "BEAR" in htf_trend:
                    print(f"🚫 Skipped BUY on {best['pair']}: Contradicts HTF Bearish Trend")
                    continue

                if "SELL" in str(best["setup"]).upper() and "BULL" in htf_trend:
                    print(f"🚫 Skipped SELL on {best['pair']}: Contradicts HTF Bullish Trend")
                    continue

                print("\n🎯 CHECKING SETUP")
                print(f"Pair        : {best['pair']}")
                print(f"Setup       : {best['setup']}")
                print(f"Brain Score : {best['brain_score']:.1f}")

                direction = "BUY" if "BUY" in str(best["setup"]).upper() else "SELL"

                trade = trader.execute_trade(
                    best["pair"],
                    direction,
                    best["price"],
                    best["atr"],
                    context=best
                )

                if not trade:
                    continue

                # Store active trade details in memory for closure monitoring
                active_tracked_trade = trade

                print(f"\n✅ OPENED {trade['direction']} {trade['pair']} @ {trade['entry']:.4f}")

                send_message(
                    f"📈 {mode_label} TRADE OPEN\n\n"
                    f"Pair  : {trade['pair']}\n"
                    f"Side  : {trade['direction']}\n"
                    f"HTF   : {best['higher_timeframe']}\n"
                    f"Entry : {trade['entry']:.4f}\n"
                    f"SL    : {trade['stop_loss']:.4f}\n"
                    f"TP    : {trade['take_profit']:.4f}\n"
                    f"Score : {best['score']}"
                )

                trade_found = True
                break

            if not trade_found:
                print("\n❌ No valid trade found this scan.")

    except Exception as e:
        print(f"\n⚠️ Error occurred during scan loop: {e}")
        traceback.print_exc()

    time.sleep(SCAN_INTERVAL)
