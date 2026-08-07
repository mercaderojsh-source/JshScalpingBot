# ==========================================
# JshScalpingBot - Gold Pyramiding Config
# ==========================================

from config import *

# Account & Risk Overrides
START_BALANCE = 100.0
LEVERAGE = 10
MAX_OPEN_POSITIONS = 2        # Set to 2 to allow follow-up pyramiding orders
MAX_DAILY_LOSS_PCT = 100.0   # Disabled daily limit
RISK_PER_TRADE = 5.0         # 5% risk allocation per entry

# Pyramiding / Scaling In Rules
ENABLE_PYRAMIDING = True     # Allow adding a second position when Position 1 is winning
PYRAMID_PROFIT_ATR = 1.0     # Position 1 must be in profit by at least 1.0x ATR before opening Position 2

# Market Watchlist
PAIRS = ["XAUUSDT"]
WATCHLIST = ["XAUUSDT"]

# Scanner & Timeframe
TIMEFRAME = "1m"
SCAN_INTERVAL = 1

# Strategy Rules
MIN_SCORE = 40.0
REQUIRE_STRONG_BUY = False
MIN_TREND_SCORE = 4
ENABLE_RANGE_MODE = True

# Risk/Reward Setup
ATR_STOP_MULTIPLIER = 1.2    # 1.2x ATR stop
TAKE_PROFIT_RR = 2.5         # 1:2.5 R:R sweet spot

# Session Liquidity Guard
ENABLE_SESSION_FILTER = True

# Indicators
EMA_FAST = 5
EMA_SLOW = 13
RSI_PERIOD = 9
RSI_OVERBOUGHT = 75
RSI_OVERSOLD = 25

BB_PERIOD = 20
BB_STD_DEV = 2.0
RSI_RANGE_OVERSOLD = 35
RSI_RANGE_OVERBOUGHT = 65

LOG_FILE = "trade_history_gold_1m.csv"
STATE_FILE = "paper_account_gold_1m.json"
