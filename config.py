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
# Trading Pairs (Pruned High-Liquidity Pairs)
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
# Strategy Thresholds (Optimized Production Rules)
# ==========================================

MIN_SCORE = 62.0              # Strict entry threshold targeting high-conviction setups
REQUIRE_STRONG_BUY = True     # Enforce 'STRONG BUY' / 'STRONG SELL' setups only
MIN_TREND_SCORE = 8           # Rejects setups in range chop (Trend Score < 8)

# ==========================================
# Risk Management
# ==========================================

RISK_PER_TRADE = 2.0         # 2% risk per trade (~$0.22 per trade on $11.26 balance)
ATR_STOP_MULTIPLIER = 1.2    # Tight stop loss distance
TAKE_PROFIT_RR = 1.8         # Target 1:1.8 Risk-to-Reward ratio

# ==========================================
# Account State Baseline
# ==========================================

START_BALANCE = 11.26        # Exact Bitget live balance
