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
MAX_OPEN_POSITIONS = 10      # Completely removes position bottlenecking
MAX_DAILY_LOSS = 5.0         # Scaled slightly for $50 paper balance

# =========================
# Trading Pairs (Expanded for High Signal Frequency)
# =========================

PAIRS = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "DOGEUSDT",
    "LINKUSDT",
    "SUIUSDT",
    "AVAXUSDT",
    "PEPEUSDT",
    "NEARUSDT",
    "XRPUSDT",
    "APTUSDT",
    "ADAUSDT",
    "SHIBUSDT",
    "BNBUSDT"
]

# =========================
# Scanner
# =========================

SCAN_INTERVAL = 10           # Scan every 10 seconds for rapid 1m setups

# =========================
# Strategy Thresholds
# =========================

MIN_SCORE = 32.0              # Calibrated score threshold for 1m intelligence scale
REQUIRE_STRONG_BUY = True     # Enforce 'STRONG BUY' / 'STRONG SELL' setups only

# =========================
# Risk Management
# =========================

RISK_PER_TRADE = 2.0         # % of account balance ($1.00 per trade on $50 balance)
ATR_STOP_MULTIPLIER = 1.8    # Expanded stop distance to survive noise
TAKE_PROFIT_RR = 1.5         # Realistic 1 : 1.5 Risk/Reward for 1m scalping

# =========================
# Paper Trading
# =========================

START_BALANCE = 50.00        # Updated start balance
