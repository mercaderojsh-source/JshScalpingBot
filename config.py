import os

# ==========================================
# JshScalpingBot Configuration (Dynamic Live Capital)
# ==========================================

# ==========================================
# Bitget API Credentials
# ==========================================

BITGET_API_KEY = os.getenv("BITGET_API_KEY")
BITGET_API_SECRET = os.getenv("BITGET_API_SECRET")
BITGET_API_PASSPHRASE = os.getenv("BITGET_API_PASSPHRASE")

# ==========================================
# Trading Mode
# ==========================================

LIVE_TRADING = True           # Enable Live Trading on Bitget

# ==========================================
# Account Baseline (Paper Trader Fallback Only)
# ==========================================

START_BALANCE = 100.0        # Default fallback for paper mode; Live trading fetches live API balance

# ==========================================
# Futures Settings
# ==========================================

MARGIN_MODE = "crossed"       # crossed | isolated
LEVERAGE = 5
MAX_OPEN_POSITIONS = 1        # Max 1 open position at a time
MAX_DAILY_LOSS_PCT = 10.0     # Dynamic 10% daily drawdown cap

# ==========================================
# Trading Pairs
# ==========================================

PAIRS = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "NEARUSDT",
    "SUIUSDT",
    "APTUSDT",
    "XRPUSDT",
    "LINKUSDT",
    "AVAXUSDT",
    "DOGEUSDT"
]

# ==========================================
# Scanner Settings (1m High-Frequency)
# ==========================================

TIMEFRAME = "1m"              # 1-minute candle timeframe for rapid scalping
SCAN_INTERVAL = 1             # 1-second scan loop

# ==========================================
# Strategy Thresholds (Active Execution Rules)
# ==========================================

MIN_SCORE = 40.0              # Active entry threshold for 1m setups
REQUIRE_STRONG_BUY = False   # Allow standard BUY/SELL entries
MIN_TREND_SCORE = 4           # Responsive trend threshold for 1m charts
ENABLE_RANGE_MODE = True      # Enable Range Scalping (Bollinger Band bounces)

# ==========================================
# Risk Management (Dynamic Percentage Scaling)
# ==========================================

RISK_PER_TRADE = 2.0         # 2% of dynamic live Bitget balance per trade
ATR_STOP_MULTIPLIER = 1.5    # Expanded stop distance (1.5x ATR)
TAKE_PROFIT_RR = 2.0         # 1:2.0 Risk-to-Reward ratio (beats exchange fees)
