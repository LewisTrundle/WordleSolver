import threading
import os
import pickle
import numpy as np
from collections import defaultdict

ENTROPY_CACHE_FILE = os.path.join(os.path.dirname(__file__), '../../data/entropy_cache.pkl')
ENTROPY_CACHE_LOCK = threading.Lock()

# Try to load persistent entropy cache
try:
    with open(ENTROPY_CACHE_FILE, 'rb') as f:
        ENTROPY_CACHE = pickle.load(f)
except Exception:
    ENTROPY_CACHE = {}

def save_entropy_cache():
    try:
        with open(ENTROPY_CACHE_FILE, 'wb') as f:
            pickle.dump(ENTROPY_CACHE, f)
    except Exception:
        pass
