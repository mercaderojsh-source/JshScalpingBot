# ==========================================
# JshScalpingBot - Gold (XAUUSDT Exclusive) Config
# ==========================================

from config import *

# Account & Risk Overrides
START_BALANCE = 100.0        # Paper mode fallback
LEVERAGE = 10                # 10x Leverage
MAX_OPEN_POSITIONS = 1       # Focus strictly on 1 position
MAX_DAILY_LOSS_PCT = 100.0   # DISABLED: Allows infinite consecutive trades regardless of daily loss
RISK_PER_TRADE = 5.0         # 5% risk allocation per trade

# Market Watchlist Override
PAIRS = ["XAUUSDT"]
WATCHLIST = ["XAUUSDT"]

# Scanner & High-Frequency Settings
TIMEFRAME = "1m"             # 1-minute candle timeframe
SCAN_INTERVAL = 1            # 1-second polling loop

# Strategy Rules
MIN_SCORE = 40.0             # Active entry score
REQUIRE_STRONG_BUY = False   # Permits both LONG and SHORT trades
MIN_TREND_SCORE = 4          # Trend filter threshold
ENABLE_RANGE_MODE = True     # Enables Range Long and Range Short

# Risk/Reward Setup
ATR_STOP_MULTIPLIER = 1.5   # 1.5x ATR stop loss distance
TAKE_PROFIT_RR = 2.0        # 1:2.0 Risk-to-Reward ratio

# Indicators
EMA_FAST = 5
EMA_SLOW = 13
RSI_PERIOD = 9
RSI_OVERBOUGHT = 75
RSI_OVERSOLD = 25

# Range Scalper Settings
BB_PERIOD = 20
BB_STD_DEV = 2.0
RSI_RANGE_OVERSOLD = 35
RSI_RANGE_OVERBOUGHT = 65

# Output Logs
LOG_FILE = "trade_history_gold_1m.csv"
STATE_FILE = "paper_account_gold_1m.json"
