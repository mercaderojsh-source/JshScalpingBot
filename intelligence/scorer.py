# intelligence/scorer.py

from dataclasses import dataclass


@dataclass
class ScoreBreakdown:
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


def calculate_score(
    trend_score,
    ema_score,
    momentum_score,
    atr_score,
    rsi_score,
    volume_score,
    structure_score,
):
    """
    Returns a ScoreBreakdown object.

    All inputs are already normalized.

    Maximum:
        Trend      25
        EMA        20
        Momentum   15
        ATR        15
        RSI        10
        Volume     10
        Structure   5
    """

    return ScoreBreakdown(
        trend=min(trend_score, 25),
        ema=min(ema_score, 20),
        momentum=min(momentum_score, 15),
        atr=min(atr_score, 15),
        rsi=min(rsi_score, 10),
        volume=min(volume_score, 10),
        structure=min(structure_score, 5),
    )