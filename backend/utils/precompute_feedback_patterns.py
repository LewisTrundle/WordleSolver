import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np
import pickle
from utils.word_list_loader import ANSWER_LIST, GUESS_LIST
from utils.filter import get_feedback_pattern
import os


OUTPUT_FILE = os.path.join(os.path.dirname(__file__), '../data/feedback_patterns.npy')
all_guesses = list(set(GUESS_LIST) | set(ANSWER_LIST))
all_guesses.sort()
all_answers = list(ANSWER_LIST)
all_answers.sort()

guess_to_idx = {word: i for i, word in enumerate(all_guesses)}
answer_to_idx = {word: i for i, word in enumerate(all_answers)}

patterns = np.empty((len(all_guesses), len(all_answers)), dtype='U5')
for gi, guess in enumerate(all_guesses):
    for ai, answer in enumerate(all_answers):
        patterns[gi, ai] = get_feedback_pattern(guess, answer)


np.save(OUTPUT_FILE, patterns)
with open(os.path.join(os.path.dirname(__file__), '../data/feedback_pattern_indices.pkl'), 'wb') as f:
    pickle.dump({'guesses': all_guesses, 'answers': all_answers}, f)

print(f"Saved feedback patterns to {OUTPUT_FILE}")