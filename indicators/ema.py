import pandas as pd


def calculate_ema(candles, period):

    closes = []

    for candle in candles:
        closes.append(float(candle[4]))

    df = pd.DataFrame(closes, columns=["close"])

    ema = df["close"].ewm(span=period).mean()

    return float(ema.iloc[-1])