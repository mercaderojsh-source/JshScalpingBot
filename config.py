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

LIVE_TRADING = False          # Keep False until Calibration Batch #2 is verified

# =========================
# Futures Settings
# =========================

MARGIN_MODE = "crossed"      # crossed | isolated
LEVERAGE = 5
MAX_OPEN_POSITIONS = 10      # Completely removes position bottlenecking
MAX_DAILY_LOSS = 5.0         # Scaled for $50 balance

# =========================
# Trading Pairs (ADAUSDT & PEPEUSDT Pruned)
# =========================

PAIRS = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "DOGEUSDT",
    "LINKUSDT",
    "SUIUSDT",
    "AVAXUSDT",
    "NEARUSDT",
    "XRPUSDT",
    "APTUSDT",
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

MIN_SCORE = 40.0              # Raised from 32.0 to filter low-conviction market chop
REQUIRE_STRONG_BUY = True     # Enforce 'STRONG BUY' / 'STRONG SELL' setups only

# =========================
# Risk Management
# =========================

RISK_PER_TRADE = 2.0         # % of account balance ($1.00 per trade on $50 balance)
ATR_STOP_MULTIPLIER = 1.8    # Expanded stop distance to survive noise
TAKE_PROFIT_RR = 1.2         # Lowered from 1.5 for faster, higher-probability scalp exits

# =========================
# Paper Trading
# =========================

START_BALANCE = 50.00        # Reset starting paper balance
