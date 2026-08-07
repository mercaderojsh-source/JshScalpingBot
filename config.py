import os

# ==========================================
# JshScalpingBot Configuration (Live - $11.26 Capital)
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
# Futures Settings
# ==========================================

MARGIN_MODE = "crossed"       # crossed | isolated
LEVERAGE = 5
MAX_OPEN_POSITIONS = 1        # Max 1 open position for $11.26 account
MAX_DAILY_LOSS = 1.12         # Strict 10% daily drawdown cap ($1.12)

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

MIN_SCORE = 40.0              # Lowered to 40.0 to trigger 1m trades actively
REQUIRE_STRONG_BUY = False   # Allow standard BUY/SELL entries
MIN_TREND_SCORE = 4           # Responsive trend threshold for 1m charts
ENABLE_RANGE_MODE = True      # Enable Range Scalping (Bollinger Band bounces)

# ==========================================
# Risk Management
# ==========================================

RISK_PER_TRADE = 2.0         # 2% risk per trade (~$0.22 per trade on $11.26 balance)
ATR_STOP_MULTIPLIER = 1.0    # Fee-aware stop distance
TAKE_PROFIT_RR = 1.6         # 1:1.6 Risk-to-Reward ratio

# ==========================================
# Account State Baseline
# ==========================================

START_BALANCE = 11.26        # Exact Bitget live balance
