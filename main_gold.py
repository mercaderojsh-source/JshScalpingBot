import sys
import os

# 1. Load Gold Configuration
import config_gold as config

# 2. Inject config_gold globally into sys.modules so all imported sub-modules use Gold settings
sys.modules['config'] = config

# 3. Import primary bot main module
import main

if __name__ == "__main__":
    print("\n==========================================")
    print("🏆 Starting JshScalpingBot - Gold (XAUUSDT)")
    print("==========================================\n")
    
    # Execute main loop directly if main exposes main(), or let module top-level run
    if hasattr(main, "main"):
        main.main()
