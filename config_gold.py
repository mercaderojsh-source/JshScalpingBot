# ==========================================
# JshScalpingBot - Gold (XAUUSDT) Config
# ==========================================

# 1. Inherit default configuration settings
from config import *

# 2. Account & Risk Overrides (Dynamic Live Capital)
LEVERAGE = 5                 # 5x Leverage
MAX_OPEN_POSITIONS = 1       # Focus on 1 Gold trade at a time
MAX_DAILY_LOSS_PCT = 10.0    # Dynamic 10% daily drawdown cap
RISK_PER_TRADE = 2.0        # 2% risk of dynamic live balance per trade

# 3. Market Watchlist Override
PAIRS = ["XAUUSDT"]
WATCHLIST = ["XAUUSDT"]

# 4. Scanner & High-Frequency Settings
TIMEFRAME = "1m"             # 1-minute candle timeframe for rapid scalping
SCAN_INTERVAL = 1            # Near-instant 1-second scan loop

# 5. Strategy Thresholds (Active Execution & Range Scalping Rules)
MIN_SCORE = 40.0             # Active entry threshold for 1m Gold trades
REQUIRE_STRONG_BUY = False   # Allow standard BUY/SELL entries on 1m
MIN_TREND_SCORE = 4          # Responsive trend threshold for 1m Gold charts
ENABLE_RANGE_MODE = True     # Enable Range Scalping (Bollinger Band bounces)

# Risk/Reward Setup (Fee-Aware Parameters)
ATR_STOP_MULTIPLIER = 1.5   # 1.5x ATR stop loss distance
TAKE_PROFIT_RR = 2.0        # Target 1:2.0 Risk-to-Reward ratio

# Fast Indicators for 1m Gold Charts
EMA_FAST = 5
EMA_SLOW = 13
RSI_PERIOD = 9
RSI_OVERBOUGHT = 75
RSI_OVERSOLD = 25

# Range Scalper Thresholds
BB_PERIOD = 20
BB_STD_DEV = 2.0
RSI_RANGE_OVERSOLD = 35
RSI_RANGE_OVERBOUGHT = 65

# 6. Isolated Output Files
LOG_FILE = "trade_history_gold_1m.csv"
STATE_FILE = "paper_account_gold_1m.json"
