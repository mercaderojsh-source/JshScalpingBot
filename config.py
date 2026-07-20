import os

# =========================
# JshScalpingBot Configuration
# =========================

# Bitget API
BITGET_API_KEY = os.getenv("BITGET_API_KEY")
BITGET_API_SECRET = os.getenv("BITGET_API_SECRET")
BITGET_API_PASSPHRASE = os.getenv("BITGET_API_PASSPHRASE")

# Trading Mode
LIVE_TRADING = False

# Futures Settings
MARGIN_MODE = "crossed"      # crossed or isolated
LEVERAGE = 5                 # Default leverage
MAX_OPEN_POSITIONS = 1
MAX_DAILY_LOSS = 3.0         # USDT

# Trading Pairs
PAIRS = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "XRPUSDT",
    "BGBUSDT"
]

# Scanner
SCAN_INTERVAL = 30

# Strategy
MIN_SCORE = 75

# Paper Trading
START_BALANCE = 15.00

# Risk Management
RISK_PER_TRADE = 1.0         # % of account balance to risk
TAKE_PROFIT_RR = 2.0         # Risk : Reward (1:2)