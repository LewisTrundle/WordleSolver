import time
import random
from utils.word_list_loader import WORD_LIST
from utils.filter import get_feedback_pattern
from services.entropy_strategy import best_guess_entropy as entropy_strategy
from services.frequency_strategy import best_guess_frequency as frequency_strategy
from services.partition_strategy import best_guess_partition as partition_strategy
from services.minimax_strategy import best_guess_minimax as minimax_strategy

def simulate_wordle_service(strategy: str = 'filter', hard_mode: bool = False, start_word: str = 'slate'):
    """
    Run a simulation of solving all possible answers using the selected strategy, hard mode, and starting word.
    Expects JSON: { 'strategy': 'entropy'|'frequency'|'partition'|'minimax'|'filter', 'hardMode': bool, 'startWord': str }
    Returns: { avgGuesses, maxGuesses, totalTimeMs, totalWords }
    """
    strategy = strategy or 'filter'
    hard_mode = bool(hard_mode)
    start_word = str(start_word).lower()

    strategy_map = {
        'entropy': lambda words: entropy_strategy(words)['best_guess']['word'],
        'frequency': lambda words: frequency_strategy(words)['best_guess']['word'],
        'partition': lambda words: partition_strategy(words, get_feedback_pattern)['best_guess']['word'],
        'minimax': lambda words: minimax_strategy(words, get_feedback_pattern)['best_guess']['word'],
        'filter': lambda words: random.choice(words),
    }
    pick_next = strategy_map.get(strategy, strategy_map['filter'])

    all_answers = [w for w in WORD_LIST if len(w) == 5]
    total_guesses = 0
    max_guesses = 0
    start_time = time.time()
    for answer in all_answers:
        guesses = 1
        possible_words = all_answers.copy()
        history = [{'guess': start_word, 'feedback': get_feedback_pattern(start_word, answer)}]
        current_guess = start_word
        solved = (current_guess == answer)
        while not solved and guesses < 10:
            possible_words = [w for w in possible_words if get_feedback_pattern(current_guess, w) == history[-1]['feedback']]
            if not possible_words:
                break
            next_guess = pick_next(possible_words)
            guesses += 1
            feedback = get_feedback_pattern(next_guess, answer)
            history.append({'guess': next_guess, 'feedback': feedback})
            current_guess = next_guess
            if current_guess == answer:
                solved = True
        total_guesses += guesses
        if guesses > max_guesses:
            max_guesses = guesses
    end_time = time.time()
    return {
        'avgGuesses': total_guesses / len(all_answers),
        'maxGuesses': max_guesses,
        'totalTimeMs': int((end_time - start_time) * 1000),
        'totalWords': len(all_answers)
    }
