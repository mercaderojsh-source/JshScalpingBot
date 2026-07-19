import pandas as pd


def calculate_atr(candles, period=14):

    highs = []
    lows = []
    closes = []

    # Bitget candles are oldest -> newest
    for candle in candles:
        highs.append(float(candle[2]))
        lows.append(float(candle[3]))
        closes.append(float(candle[4]))

    df = pd.DataFrame({
        "high": highs,
        "low": lows,
        "close": closes
    })

    previous_close = df["close"].shift(1)

    tr = pd.concat([
        df["high"] - df["low"],
        (df["high"] - previous_close).abs(),
        (df["low"] - previous_close).abs()
    ], axis=1).max(axis=1)

    atr = tr.rolling(period).mean()

    return float(atr.iloc[-1])