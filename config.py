import os

# ==========================================
# JshScalpingBot Configuration (Gold Only Mode)
# ==========================================

# Bitget API Credentials
BITGET_API_KEY = os.getenv("BITGET_API_KEY")
BITGET_API_SECRET = os.getenv("BITGET_API_SECRET")
BITGET_API_PASSPHRASE = os.getenv("BITGET_API_PASSPHRASE")

# Trading Mode & Balance
LIVE_TRADING = True           # Enable Live Trading on Bitget
START_BALANCE = 100.0        # Fallback for paper mode

# Futures Settings (Calibrated for XAUUSDT)
MARGIN_MODE = "crossed"       # crossed | isolated
LEVERAGE = 10                # 10x Leverage for larger order sizing
MAX_OPEN_POSITIONS = 1        # Focus on 1 active trade
MAX_DAILY_LOSS_PCT = 15.0     # 15% daily drawdown cap buffer

# Market Focus (Locked exclusively to Gold)
PAIRS = ["XAUUSDT"]

# Scanner Settings (1m High-Frequency)
TIMEFRAME = "1m"              # 1-minute candle timeframe
SCAN_INTERVAL = 1             # 1-second scan loop

# Strategy & Signal Filters (Enables BOTH Long & Short setups)
MIN_SCORE = 40.0              # Entry threshold for 1m setups
REQUIRE_STRONG_BUY = False   # Allows standard BUY (Long) and SELL (Short) entries
MIN_TREND_SCORE = 4           # Responsive trend threshold
ENABLE_RANGE_MODE = True      # Range Buy (Long support) & Range Sell (Short resistance)

# Risk & Position Sizing
RISK_PER_TRADE = 5.0         # 5% risk allocation per trade
ATR_STOP_MULTIPLIER = 1.5    # 1.5x ATR stop distance
TAKE_PROFIT_RR = 2.0         # 1:2.0 Risk-to-Reward ratio
