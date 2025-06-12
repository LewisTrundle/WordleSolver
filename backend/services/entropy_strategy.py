from collections import defaultdict
from utils.word_list_loader import ANSWER_LIST, GUESS_LIST
from utils.filter import filter_possible_words, get_feedback_pattern
import numpy as np
from functools import lru_cache
import os
import pickle
from concurrent.futures import ThreadPoolExecutor, as_completed

# Memoize feedback patterns for (guess, answer) pairs
@lru_cache(maxsize=100000)
def feedback_pattern_cached(guess, answer):
    return get_feedback_pattern(guess, answer)

# Persistent entropy cache file
ENTROPY_CACHE_FILE = os.path.join(os.path.dirname(__file__), '../data/entropy_cache.pkl')

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

def calculate_entropy(guess, possible_answers):
    """
    For a given guess, calculate the expected information gain (entropy) over all possible answers.
    Uses memoization for feedback patterns and numpy for fast entropy calculation.
    """
    if not possible_answers:
        # No possible answers left, entropy is undefined (return 0)
        return 0.0
    key = (guess, frozenset(possible_answers))
    if key in ENTROPY_CACHE:
        return ENTROPY_CACHE[key]
    pattern_counts = defaultdict(int)
    for answer in possible_answers:
        pattern = feedback_pattern_cached(guess, answer)
        pattern_counts[pattern] += 1
    counts = np.array(list(pattern_counts.values()), dtype=np.float64)
    total = counts.sum()
    if total == 0:
        entropy = 0.0
    else:
        probs = counts / total
        entropy = -np.sum(probs * np.log2(probs))
    ENTROPY_CACHE[key] = float(entropy)
    return float(entropy)

def best_guess_entropy(sort=False, parallel=False, history=None):
    possible_guesses = filter_possible_words(history)
    possible_answers = filter_possible_words(history) if history else ANSWER_LIST.copy()
    entropy_pairs = []
    best_entry = {'word': None, 'value': -1}

    def entropy_worker(guess):
        val = calculate_entropy(guess, possible_answers)
        return {'word': guess, 'value': val}

    if parallel:
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(entropy_worker, guess): guess for guess in possible_guesses}
            for future in as_completed(futures):
                entry = future.result()
                entropy_pairs.append(entry)
    else:
        for guess in possible_guesses:
            entry = entropy_worker(guess)
            entropy_pairs.append(entry)

    if sort:
        entropy_pairs.sort(key=lambda x: x['value'], reverse=True)
        best_entry = entropy_pairs[0] if entropy_pairs else {'word': None, 'value': -1}
    else:
        best_entry = max(entropy_pairs, key=lambda x: x['value']) if entropy_pairs else {'word': None, 'value': -1}

    print(entropy_pairs[:5], flush=True)  # Debugging output to see first few entries
    save_entropy_cache()
    return {'best_guess': best_entry, 'possible_words': entropy_pairs}