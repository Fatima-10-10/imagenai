from datetime import datetime, timedelta

cache_store = {}
CACHE_EXPIRY_MINUTES = 60

def get_from_cache(key: str):
    if key in cache_store:
        data, expiry = cache_store[key]
        if datetime.now() < expiry:
            return data
        else:
            del cache_store[key]
    return None

def set_in_cache(key: str, value):
    expiry = datetime.now() + timedelta(minutes=CACHE_EXPIRY_MINUTES)
    cache_store[key] = (value, expiry)