import numpy as np
import os
import pickle
from functools import lru_cache
from utils.filter import get_feedback_pattern
from utils.word_list_loader import GUESS_LIST, ANSWER_LIST

FEEDBACK_PATTERN_FILE = os.path.join(os.path.dirname(__file__), '../../data/feedback_patterns.npy')
FEEDBACK_PATTERN_INDEX_FILE = os.path.join(os.path.dirname(__file__), '../../data/feedback_pattern_indices.pkl')

def load_feedback_table():
    patterns = np.load(FEEDBACK_PATTERN_FILE)
    with open(FEEDBACK_PATTERN_INDEX_FILE, 'rb') as f:
        indices = pickle.load(f)
    guess_to_idx = {word: i for i, word in enumerate(indices['guesses'])}
    answer_to_idx = {word: i for i, word in enumerate(indices['answers'])}
    return patterns, guess_to_idx, answer_to_idx

FEEDBACK_PATTERNS, GUESS_TO_IDX, ANSWER_TO_IDX = load_feedback_table()

@lru_cache(maxsize=100000)
def feedback_pattern_cached(guess, answer):
    return get_feedback_pattern(guess, answer)

def precomputed_feedback_pattern(guess, answer):
    gi = GUESS_TO_IDX[guess]
    ai = ANSWER_TO_IDX[answer]
    return FEEDBACK_PATTERNS[gi, ai]
