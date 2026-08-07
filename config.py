import os

# ==========================================
# JshScalpingBot Configuration (Unlimited Daily Loss Mode)
# ==========================================

# Bitget API Credentials
BITGET_API_KEY = os.getenv("BITGET_API_KEY")
BITGET_API_SECRET = os.getenv("BITGET_API_SECRET")
BITGET_API_PASSPHRASE = os.getenv("BITGET_API_PASSPHRASE")

# Trading Mode & Balance
LIVE_TRADING = True           # Enable Live Trading on Bitget
START_BALANCE = 100.0        # Fallback for paper mode

# Futures Settings
MARGIN_MODE = "crossed"       # crossed | isolated
LEVERAGE = 10                # 10x Leverage
MAX_OPEN_POSITIONS = 1        # Max 1 open position at a time
MAX_DAILY_LOSS_PCT = 100.0   # DISABLED: 100% cap allows continuous trading without daily loss lockouts

# Market Focus
PAIRS = ["XAUUSDT"]

# Scanner Settings (1m High-Frequency)
TIMEFRAME = "1m"              # 1-minute candle timeframe
SCAN_INTERVAL = 1             # 1-second scan loop

# Strategy Thresholds
MIN_SCORE = 40.0              # Entry threshold for 1m setups
REQUIRE_STRONG_BUY = False   # Allows standard BUY/SELL entries
MIN_TREND_SCORE = 4           # Responsive trend threshold
ENABLE_RANGE_MODE = True      # Range mode enabled

# Risk & Position Sizing
RISK_PER_TRADE = 5.0         # 5% risk allocation per trade
ATR_STOP_MULTIPLIER = 1.5    # 1.5x ATR stop distance
TAKE_PROFIT_RR = 2.0         # 1:2.0 Risk-to-Reward ratio
