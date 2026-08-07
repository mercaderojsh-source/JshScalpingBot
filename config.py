import os

# ==========================================
# JshScalpingBot Configuration (Gold Only)
# ==========================================

# Bitget API Credentials
BITGET_API_KEY = os.getenv("BITGET_API_KEY")
BITGET_API_SECRET = os.getenv("BITGET_API_SECRET")
BITGET_API_PASSPHRASE = os.getenv("BITGET_API_PASSPHRASE")

# Trading Mode & Balance
LIVE_TRADING = True           # Enable Live Trading on Bitget
START_BALANCE = 100.0        # Fallback for paper mode

# Futures & Risk Settings
MARGIN_MODE = "crossed"       # crossed | isolated
LEVERAGE = 10                # 10x Leverage
MAX_OPEN_POSITIONS = 2        # Allow up to 2 positions via pyramiding
MAX_DAILY_LOSS_PCT = 100.0   # Disabled daily loss limit
RISK_PER_TRADE = 5.0         # 5% risk allocation per entry

# Pyramiding Rules
ENABLE_PYRAMIDING = True     # Allow adding a second position when Position 1 is winning
PYRAMID_PROFIT_ATR = 1.0     # Required ATR gain before 2nd entry

# Watchlist (Gold Exclusive - Crypto Disabled)
PAIRS = ["XAUUSDT"]
WATCHLIST = PAIRS

# Scanner & High-Frequency Loop
TIMEFRAME = "1m"              # 1-minute candle timeframe
SCAN_INTERVAL = 1             # 1-second polling loop

# Strategy Thresholds
MIN_SCORE = 40.0              # Entry score threshold
REQUIRE_STRONG_BUY = False   # Allows standard BUY & SELL signals
MIN_TREND_SCORE = 4           # Responsive trend filter
ENABLE_RANGE_MODE = True      # Enables Bollinger Band bounce entries

# Risk/Reward Setup (Strictly beat exchange fees on Gold)
ATR_STOP_MULTIPLIER = 1.5    # 1.5x ATR stop distance
TAKE_PROFIT_RR = 3.0         # 1:3.0 R:R to force +$15.00+ price moves

# Session Liquidity Guard
ENABLE_SESSION_FILTER = True # Restricts entries to peak volatility hours (London & NY)

# Indicators
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

# Output Logs
LOG_FILE = "trade_history_gold_1m.csv"
STATE_FILE = "paper_account_gold_1m.json"
