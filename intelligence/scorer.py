from dataclasses import dataclass


@dataclass
class ScoreBreakdown:
    pair: str

    trend: float
    ema: float
    momentum: float
    atr: float
    rsi: float
    volume: float
    structure: float

    @property
    def total(self):
        return round(
            self.trend
            + self.ema
            + self.momentum
            + self.atr
            + self.rsi
            + self.volume
            + self.structure,
            2,
        )

    def as_dict(self):
        return {
            "pair": self.pair,
            "trend": self.trend,
            "ema": self.ema,
            "momentum": self.momentum,
            "atr": self.atr,
            "rsi": self.rsi,
            "volume": self.volume,
            "structure": self.structure,
            "total": self.total,
        }


def calculate_score(
    pair,
    trend,
    ema,
    momentum,
    atr,
    rsi,
    volume,
    structure,
):
    """
    All values must already be normalized.

    Max scores

    Trend      25
    EMA         20
    Momentum    15
    ATR         15
    RSI         10
    Volume      10
    Structure    5
    """

    return ScoreBreakdown(
        pair=pair,
        trend=min(trend, 25),
        ema=min(ema, 20),
        momentum=min(momentum, 15),
        atr=min(atr, 15),
        rsi=min(rsi, 10),
        volume=min(volume, 10),
        structure=min(structure, 5),
    )