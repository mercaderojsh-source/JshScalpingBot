# ==========================================
# JshScalpingBot - Gold (XAUUSDT) Config
# ==========================================

# 1. Inherit default configuration settings
from config import *

# 2. Account & Risk Overrides (Calibrated for $11.26 Live Balance)
START_BALANCE = 11.26        # Exact Bitget live balance
INITIAL_BALANCE = 11.26      # Baseline fallback
LEVERAGE = 5                 # 5x Leverage
MAX_OPEN_POSITIONS = 1       # Focus on 1 Gold trade at a time
MAX_DAILY_LOSS = 1.12        # Strict 10% daily risk cap ($1.12 max drawdown)
RISK_PER_TRADE = 2.0        # 2% risk per trade (~$0.22 max risk per trade)

# 3. Market Watchlist Override
PAIRS = ["XAUUSDT"]
WATCHLIST = ["XAUUSDT"]

# 4. Scanner & High-Frequency Settings
TIMEFRAME = "1m"             # 1-minute candle timeframe for rapid scalping
SCAN_INTERVAL = 1            # Near-instant 1-second scan loop

# 5. Strategy & Indicator Tuning (1m High-Frequency Rules)
MIN_SCORE = 55.0             # Lowered to capture fast 1m momentum shifts
REQUIRE_STRONG_BUY = False   # Allow standard BUY/SELL signals on 1m
MIN_TREND_SCORE = 6          # Responsive trend threshold for 1m charts

# Risk/Reward Setup (Fee-Aware Parameters)
ATR_STOP_MULTIPLIER = 1.0   # Tight stop loss distance
TAKE_PROFIT_RR = 1.6        # Target 1:1.6 Risk-to-Reward ratio (covers taker fees)

# Fast Indicators for 1m Charts
EMA_FAST = 5
EMA_SLOW = 13
RSI_PERIOD = 9
RSI_OVERBOUGHT = 75
RSI_OVERSOLD = 25

# 6. Isolated Output Files
LOG_FILE = "trade_history_gold_1m.csv"
STATE_FILE = "paper_account_gold_1m.json"
