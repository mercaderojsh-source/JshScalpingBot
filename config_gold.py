# ==========================================
# JshScalpingBot - Gold (XAUUSDT) Config
# ==========================================

# 1. Inherit all default configuration settings
from config import *

# 2. Account & Risk Overrides
INITIAL_BALANCE = 50.0       # Independent $50.00 Paper Balance
LEVERAGE = 5                 # 5x Leverage
MAX_OPEN_POSITIONS = 1       # Focus on 1 Gold trade at a time
POSITION_SIZE_PERCENT = 0.80 # Margin allocation per trade

# 3. Market Watchlist Override
PAIRS = ["XAUUSDT"]
WATCHLIST = ["XAUUSDT"]

# 4. Strategy & Indicator Tuning
TIMEFRAME = "5m"
MIN_SCORE = 45.0             # High-conviction entry threshold
TAKE_PROFIT_RR = 1.5         # 1:1.5 Risk-to-Reward ratio
STOP_LOSS_PCT = 0.0035       # 0.35% Stop Loss (~$14.12 Gold price swing)

# Indicators
EMA_FAST = 9
EMA_SLOW = 21
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

# 5. Isolated Output Files
LOG_FILE = "trade_history_gold.csv"
STATE_FILE = "paper_account_gold.json"
