from exchange.bitget import get_candles

print("=" * 40)
print("🚀 Testing Candle Data")
print("=" * 40)

data = get_candles("BTCUSDT")

print(data)