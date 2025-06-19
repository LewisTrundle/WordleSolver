import numpy as np
from collections import defaultdict
from .entropy_cache import ENTROPY_CACHE, ENTROPY_CACHE_LOCK
from .feedback_cache import precomputed_feedback_pattern, feedback_pattern_cached

def calculate_entropy(guess, possible_answers, use_entropy_cache,
                      use_feedback_cache, use_precomputed_entropy, use_precomputed_feedback):
    if not possible_answers: return 0.0
    if use_entropy_cache:
        key = (guess, tuple(sorted(possible_answers)))
        with ENTROPY_CACHE_LOCK:
            if key in ENTROPY_CACHE: return ENTROPY_CACHE[key]
    pattern_counts = defaultdict(int)
    for answer in possible_answers:
        pattern = precomputed_feedback_pattern(guess, answer) if use_precomputed_feedback else feedback_pattern_cached(guess, answer)
        pattern_counts[pattern] += 1
    counts = np.array(list(pattern_counts.values()), dtype=np.float64)
    total = counts.sum()
    if total == 0:
        entropy = 0.0
    else:
        probs = counts / total
        entropy = -np.sum(probs * np.log2(probs))
    if use_entropy_cache:
        with ENTROPY_CACHE_LOCK:
            ENTROPY_CACHE[key] = float(entropy)
    return float(entropy)
