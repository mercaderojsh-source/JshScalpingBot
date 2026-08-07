import sys
import os

# 1. Load Gold Configuration
import config_gold as config

# 2. Inject config_gold globally into sys.modules so all imported sub-modules use Gold settings
sys.modules['config'] = config

print("\n==========================================")
print("🏆 Starting JshScalpingBot - Gold (XAUUSDT) [1m Rapid Scalper]")
print("==========================================\n")

# 3. Import primary bot main module (executes scan loop with Gold overrides active)
import main

if __name__ == "__main__":
    if hasattr(main, "main"):
        main.main()
