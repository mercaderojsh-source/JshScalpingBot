from exchange.bitget import get_candles
from indicators.ema import calculate_ema
from indicators.atr import calculate_atr
from strategy.market_analyzer import analyze_market

print("=" * 40)
print("🚀 MARKET ANALYZER")
print("=" * 40)

data = get_candles("BTCUSDT")
candles = data["data"]

ema9 = calculate_ema(candles, 9)
ema21 = calculate_ema(candles, 21)
ema50 = calculate_ema(candles, 50)
atr = calculate_atr(candles)

market = analyze_market(
    ema9,
    ema21,
    ema50,
    atr
)

print(f"EMA 9        : {ema9:.2f}")
print(f"EMA 21       : {ema21:.2f}")
print(f"EMA 50       : {ema50:.2f}")
print(f"ATR          : {atr:.2f}")
print()
print(f"Trend        : {market['trend']}")
print(f"Volatility   : {market['volatility']}")