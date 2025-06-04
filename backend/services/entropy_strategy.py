from collections import defaultdict
from utils.filter import get_feedback_pattern
import numpy as np
from functools import lru_cache

# Memoize feedback patterns for (guess, answer) pairs
@lru_cache(maxsize=100000)
def feedback_pattern_cached(guess, answer):
    return get_feedback_pattern(guess, answer)

def calculate_entropy(guess, possible_words):
    """
    For a given guess, calculate the expected information gain (entropy) over all possible answers.
    Uses memoization for feedback patterns and numpy for fast entropy calculation.
    """
    pattern_counts = defaultdict(int)
    for answer in possible_words:
        pattern = feedback_pattern_cached(guess, answer)
        pattern_counts[pattern] += 1
    counts = np.array(list(pattern_counts.values()), dtype=np.float64)
    total = counts.sum()
    if total == 0:
        return 0.0
    probs = counts / total
    entropy = -np.sum(probs * np.log2(probs))
    return float(entropy)

def best_guess_entropy(possible_words):
    """
    For each possible guess, calculate the expected information gain (entropy) based on the current possible answers.
    Returns the guess with the highest entropy and a list of all possible words with their entropy values.
    This method helps maximize the information gained from each guess.
    """
    entropy_pairs = [
        {'word': guess, 'value': calculate_entropy(guess, possible_words)}
        for guess in possible_words
    ]
    best_entry = max(entropy_pairs, key=lambda x: x['value']) if entropy_pairs else {'word': None, 'value': -1}
    entropy_pairs.sort(key=lambda x: x['value'], reverse=True)
    return {'best_guess': best_entry, 'possible_words': entropy_pairs}