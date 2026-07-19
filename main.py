from exchange.bitget import get_candles
from indicators.ema import calculate_ema

print("=" * 40)
print("🚀 EMA TEST")
print("=" * 40)

data = get_candles("BTCUSDT")

candles = data["data"]

ema9 = calculate_ema(candles, 9)
ema21 = calculate_ema(candles, 21)
ema50 = calculate_ema(candles, 50)

print(f"EMA 9  : {ema9}")
print(f"EMA 21 : {ema21}")
print(f"EMA 50 : {ema50}")