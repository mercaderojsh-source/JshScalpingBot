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
MAX_OPEN_POSITIONS = 1        # Max 1 open position at a time for $11.26 account
MAX_DAILY_LOSS = 1.12         # Strict 10% daily risk cap ($1.12 max daily drawdown)

# ==========================================
# Trading Pairs (High-Liquidity Scalping Pairs)
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
SCAN_INTERVAL = 1             # Near-instant 1-second scan loop

# ==========================================
# Strategy Thresholds (1m Calibrated Rules)
# ==========================================

MIN_SCORE = 55.0              # Lowered to capture fast 1m momentum shifts
REQUIRE_STRONG_BUY = False   # Set to False to allow standard BUY/SELL setups
MIN_TREND_SCORE = 6           # Responsive trend threshold for 1m charts

# ==========================================
# Risk Management (Fee-Aware Parameters)
# ==========================================

RISK_PER_TRADE = 2.0         # 2% risk per trade (~$0.22 per trade on $11.26 balance)
ATR_STOP_MULTIPLIER = 1.0    # Tight stop distance for 1m candles
TAKE_PROFIT_RR = 1.6         # Target 1:1.6 Risk-to-Reward ratio (covers taker fees)

# ==========================================
# Account State Baseline
# ==========================================

START_BALANCE = 11.26        # Exact Bitget live balance
