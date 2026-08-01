import os

# ==========================================
# JshScalpingBot Configuration
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

LIVE_TRADING = False          # Keep False until Calibration Batch #3 is verified

# ==========================================
# Futures Settings
# ==========================================

MARGIN_MODE = "crossed"      # crossed | isolated
LEVERAGE = 5
MAX_OPEN_POSITIONS = 10      # Prevents position bottlenecking
MAX_DAILY_LOSS = 20.0        # Relaxed cap for paper calibration data collection

# ==========================================
# Trading Pairs (Pruned to 7 High-Liquidity Pairs)
# Removed SHIBUSDT (sub-cent decimal bug) & low performers
# ==========================================

PAIRS = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "NEARUSDT",
    "SUIUSDT",
    "APTUSDT",
    "XRPUSDT"
]

# ==========================================
# Scanner Settings
# ==========================================

SCAN_INTERVAL = 10           # Scan every 10 seconds for rapid setups

# ==========================================
# Strategy Thresholds (Calibration Batch #3 - Option A)
# ==========================================

MIN_SCORE = 50.0              # Lowered to 50.0 for accelerated data collection
REQUIRE_STRONG_BUY = False    # Allow standard BUY/SELL entries to increase trade velocity

# ==========================================
# Risk Management
# ==========================================

RISK_PER_TRADE = 2.0         # % of account balance ($1.00 risk per trade on $50 balance)
ATR_STOP_MULTIPLIER = 1.8    # Expanded stop distance to absorb noise
TAKE_PROFIT_RR = 1.2         # Target RR for fast, high-probability scalp exits

# ==========================================
# Paper Trading State
# ==========================================

START_BALANCE = 50.00        # Reset starting paper balance for Batch #3
