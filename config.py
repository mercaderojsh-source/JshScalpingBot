import os

# =========================
# JshScalpingBot Configuration
# =========================

# =========================
# Bitget API
# =========================

BITGET_API_KEY = os.getenv("BITGET_API_KEY")
BITGET_API_SECRET = os.getenv("BITGET_API_SECRET")
BITGET_API_PASSPHRASE = os.getenv("BITGET_API_PASSPHRASE")

# =========================
# Trading Mode
# =========================

LIVE_TRADING = False

# =========================
# Futures Settings
# =========================

MARGIN_MODE = "crossed"      # crossed | isolated
LEVERAGE = 5
MAX_OPEN_POSITIONS = 1
MAX_DAILY_LOSS = 3.0         # USDT

# =========================
# Trading Pairs (Expanded to 10 High-Volume Pairs)
# =========================

PAIRS = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "XRPUSDT",
    "DOGEUSDT",
    "AVAXUSDT",
    "LINKUSDT",
    "NEARUSDT",
    "APTUSDT",
    "SUIUSDT",
]

# =========================
# Scanner
# =========================

SCAN_INTERVAL = 10           # Scan every 10 seconds for rapid 1m setups

# =========================
# Strategy Thresholds
# =========================

MIN_SCORE = 52               # Optimized score threshold for higher setup capture

# =========================
# Risk Management
# =========================

RISK_PER_TRADE = 2.0         # % of account balance
ATR_STOP_MULTIPLIER = 1.8    # Expanded stop distance to survive noise
TAKE_PROFIT_RR = 1.5         # Realistic 1 : 1.5 Risk/Reward for 1m scalping

# =========================
# Paper Trading
# =========================

START_BALANCE = 15.00
