import sys
# Override default config import with Gold config
import config_gold as config

# Swap out the module reference before main logic executes
sys.modules['config'] = config

# Run primary bot script
from main import main

if __name__ == "__main__":
    main()
