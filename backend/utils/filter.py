import numpy as np # type: ignore
from utils.word_list_loader import WORD_LIST


def filter_possible_words(history, word_list):
    possible_words = word_list.copy()
    for entry in history:
        guess = entry.get('guess', '')
        feedback = entry.get('feedback', '')
        if guess and feedback and len(guess) == 5 and len(feedback) == 5:
            possible_words = filter_words_custom(guess, feedback, possible_words)
    return possible_words

def get_filtered_words_from_data(data):
    history = data.get('history', []) if data else []
    possible_words = filter_possible_words(history, WORD_LIST)
    return possible_words



def filter_words_custom(guess, feedback, words):
    filtered = []
    for word in words:
        valid = True
        # Green pass: correct letter, correct place
        for i in range(5):
            if feedback[i] == 'g' and word[i] != guess[i]:
                valid = False
                break
        if not valid:
            continue
        # Yellow pass: correct letter, wrong place
        for i in range(5):
            g, f = guess[i], feedback[i]
            if f == 'y':
                if g not in word or word[i] == g:
                    valid = False
                    break
        if not valid:
            continue
        # Grey pass: letter not in word (except for greens/yellows)
        for i in range(5):
            g, f = guess[i], feedback[i]
            if f == '.':
                allowed = sum(1 for j in range(5) if guess[j] == g and feedback[j] in ('g', 'y'))
                if word.count(g) > allowed:
                    valid = False
                    break
        if not valid:
            continue
        # Always enforce hard mode: all green/yellow letters must be present
        for i, (g, f) in enumerate(zip(guess, feedback)):
            if f in ('g', 'y') and g not in word:
                valid = False
                break
        if valid:
            filtered.append(word)
    return filtered

def get_feedback_pattern(guess, answer):
    """
    Generate a Wordle-style feedback pattern for a guess/answer pair.
    Returns a string of length 5 with:
    - 'g' for green (correct letter, correct place)
    - 'y' for yellow (correct letter, wrong place)
    - '.' for grey (letter not in answer)
    """
    pattern = ['.'] * 5
    answer_chars = list(answer)
    # First pass: greens
    for i in range(5):
        if guess[i] == answer[i]:
            pattern[i] = 'g'
            answer_chars[i] = None  # Mark as used
    # Second pass: yellows
    for i in range(5):
        if pattern[i] == '.' and guess[i] in answer_chars:
            pattern[i] = 'y'
            answer_chars[answer_chars.index(guess[i])] = None  # Mark as used
    return ''.join(pattern)


