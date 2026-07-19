from exchange.bitget import get_candles
from indicators.ema import calculate_ema
from indicators.atr import calculate_atr
from indicators.rsi import calculate_rsi

print("=" * 40)
print("🚀 MARKET ANALYZER")
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

    print("EMA 9 :", round(ema9, 2))
    print("EMA 21:", round(ema21, 2))
    print("EMA 50:", round(ema50, 2))
    print("ATR   :", round(atr, 2))
    print("RSI   :", rsi)

    if ema9 > ema21 > ema50:
        trend = "BULLISH"
    elif ema9 < ema21 < ema50:
        trend = "BEARISH"
    else:
        trend = "SIDEWAYS"

    print()
    print("Trend:", trend)

    if rsi > 70:
        print("RSI Status: OVERBOUGHT")
    elif rsi < 30:
        print("RSI Status: OVERSOLD")
    else:
        print("RSI Status: NORMAL")