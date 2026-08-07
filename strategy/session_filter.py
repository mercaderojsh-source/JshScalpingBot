from datetime import datetime, timezone

def is_liquidity_window_active():
    """Returns True only during high-liquidity Gold sessions (London Open & NY Overlap)."""
    now_utc = datetime.now(timezone.utc).time()
    
    # Session 1: London Open (07:00 to 10:00 UTC)
    london_open = (now_utc >= datetime.strptime("07:00", "%H:%M").time() and 
                   now_utc <= datetime.strptime("10:00", "%H:%M").time())
                   
    # Session 2: London / New York Overlap (13:00 to 17:00 UTC)
    ny_overlap = (now_utc >= datetime.strptime("13:00", "%H:%M").time() and 
                  now_utc <= datetime.strptime("17:00", "%H:%M").time())
                  
    return london_open or ny_overlap
