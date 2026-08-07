import os

# ==========================================
# JshScalpingBot Configuration (Crypto Scalper)
# ==========================================

# Bitget API Credentials
BITGET_API_KEY = os.getenv("BITGET_API_KEY")
BITGET_API_SECRET = os.getenv("BITGET_API_SECRET")
BITGET_API_PASSPHRASE = os.getenv("BITGET_API_PASSPHRASE")

# Trading Mode & Balance
LIVE_TRADING = True           # Enable Live Trading on Bitget
START_BALANCE = 100.0        # Fallback for paper mode

# Futures & Risk Settings
MARGIN_MODE = "crossed"       # crossed | isolated
LEVERAGE = 10                # 10x Leverage
MAX_OPEN_POSITIONS = 2        # Allow up to 2 concurrent crypto trades
MAX_DAILY_LOSS_PCT = 100.0   # Disabled daily loss limit
RISK_PER_TRADE = 5.0         # 5% risk allocation per entry

# Pyramiding Rules
ENABLE_PYRAMIDING = True     # Allow adding to winning trades
PYRAMID_PROFIT_ATR = 1.0     # Required ATR gain before 2nd entry

# Active Crypto Watchlist (High Volatility & Deep Liquidity)
PAIRS = ["SOLUSDT", "ETHUSDT", "BTCUSDT", "DOGEUSDT"]
WATCHLIST = PAIRS

# Scanner & High-Frequency Loop
TIMEFRAME = "1m"              # 1-minute scalping candles
SCAN_INTERVAL = 2             # 2-second scan loop to prevent rate limits

# Strategy Thresholds
MIN_SCORE = 40.0              # Entry score threshold
REQUIRE_STRONG_BUY = False   # Allows standard BUY & SELL signals
MIN_TREND_SCORE = 4           # Responsive trend filter
ENABLE_RANGE_MODE = True      # Enables Bollinger Band bounce entries

# Risk/Reward Setup (Crypto Volatility Calibrated)
ATR_STOP_MULTIPLIER = 1.5    # 1.5x ATR stop distance
TAKE_PROFIT_RR = 2.0         # 1:2.0 Risk-to-Reward ratio (easily beats fees on crypto)

# Indicators
EMA_FAST = 5
EMA_SLOW = 13
RSI_PERIOD = 9
RSI_OVERBOUGHT = 75
RSI_OVERSOLD = 25

# Range Scalper Thresholds
BB_PERIOD = 20
BB_STD_DEV = 2.0
RSI_RANGE_OVERSOLD = 35
RSI_RANGE_OVERBOUGHT = 65

# Output Logs
LOG_FILE = "trade_history_crypto_1m.csv"
STATE_FILE = "paper_account_crypto_1m.json"
