# ==========================================
# JshScalpingBot - Gold (XAUUSDT) Config
# ==========================================

# 1. Inherit all default configuration settings
from config import *

# 2. Account & Risk Overrides (Calibrated for $11.26 Live Balance)
START_BALANCE = 11.26        # Exact Bitget live balance
INITIAL_BALANCE = 11.26      # Paper baseline fallback
LEVERAGE = 5                 # 5x Leverage
MAX_OPEN_POSITIONS = 1       # Focus on 1 Gold trade at a time
MAX_DAILY_LOSS = 1.12        # Strict 10% daily risk cap ($1.12 max drawdown)
RISK_PER_TRADE = 2.0        # 2% risk per trade (~$0.22 max risk per trade)

# 3. Market Watchlist Override
PAIRS = ["XAUUSDT"]
WATCHLIST = ["XAUUSDT"]

# 4. Strategy & Indicator Tuning (Optimized Production Rules)
TIMEFRAME = "5m"
MIN_SCORE = 62.0             # High-conviction entry threshold (Rejects noise < 62.0)
REQUIRE_STRONG_BUY = True    # Enforce 'STRONG BUY' / 'STRONG SELL' setups only
MIN_TREND_SCORE = 8          # Filters out range chop (Rejects Trend Score < 8)

# Risk/Reward Setup
ATR_STOP_MULTIPLIER = 1.2   # Tightened stop loss distance
TAKE_PROFIT_RR = 1.8        # Target 1:1.8 Risk-to-Reward ratio

# Indicators
EMA_FAST = 9
EMA_SLOW = 21
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

# 5. Isolated Output Files
LOG_FILE = "trade_history_gold.csv"
STATE_FILE = "paper_account_gold.json"
