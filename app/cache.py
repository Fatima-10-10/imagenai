import shelve
from datetime import datetime, timedelta

CACHE_FILE = "cache_store"
CACHE_EXPIRY_MINUTES = 60

def get_from_cache(key: str):
    with shelve.open(CACHE_FILE) as db:
        if key in db:
            data, expiry = db[key]
            if datetime.now() < expiry:
                return data
            else:
                del db[key]
    return None

def set_in_cache(key: str, value):
    expiry = datetime.now() + timedelta(minutes=CACHE_EXPIRY_MINUTES)
    with shelve.open(CACHE_FILE) as db:
        db[key] = (value, expiry)

def get_cache_stats():
    stats = {"total": 0, "active": 0, "expired": 0}
    with shelve.open(CACHE_FILE) as db:
        for key in db:
            stats["total"] += 1
            _, expiry = db[key]
            if datetime.now() < expiry:
                stats["active"] += 1
            else:
                stats["expired"] += 1
    return stats