import time
from collections import defaultdict
from utils.word_list_loader import ANSWER_LIST, ANSWER_LIST_LENGTH
from utils.filter import get_feedback_pattern
from services.filter_strategy import filter_strategy
from services.entropy_strategy import best_guess_entropy as entropy_strategy
from services.frequency_strategy import best_guess_frequency as frequency_strategy
from services.partition_strategy import best_guess_partition as partition_strategy
from services.minimax_strategy import best_guess_minimax as minimax_strategy
from classes.GameState import GameState


STRATEGY_MAP = {
    'entropy': lambda words, **kwargs: entropy_strategy(words, **kwargs),
    'frequency': lambda words, **kwargs: frequency_strategy(words),
    'partition': lambda words, **kwargs: partition_strategy(words, get_feedback_pattern),
    'minimax': lambda words, **kwargs: minimax_strategy(words, get_feedback_pattern),
    'filter': lambda words, **kwargs: filter_strategy(words),
}


def simulate_single_word(answer: str, strategy: str, start_word: str) -> dict:
    state = GameState(answer, start_word)
    strategy_func = STRATEGY_MAP.get(strategy)
    return state.solve(lambda words: strategy_func(words))


def simulate_wordle_service(strategy: str = 'filter', hard_mode: bool = False, start_word: str = 'slate', stop_requested: list = None):
    start_word = str(start_word).lower()
    details = []
    guess_distribution = defaultdict(int)
    start_time = time.time()
    for idx, answer in enumerate(ANSWER_LIST):
        result = simulate_single_word(answer, strategy, start_word)
        details.append(result)
        guess_distribution[result['guesses']] += 1
    end_time = time.time()
    total_guesses = sum(int(k) * v for k, v in guess_distribution.items())
    avg_guesses = total_guesses / (len(details) if details else 1)
    min_guesses = min(map(int, guess_distribution.keys())) if guess_distribution else 0
    max_guesses = max(map(int, guess_distribution.keys())) if guess_distribution else 0
    unsolved_words = [d['answer'] for d in details if not d['solved']]
    return {
        'summary': {
            'strategy': strategy,
            'startWord': start_word,
            'hardMode': hard_mode,
        },
        'stats': {
            'guesses': {
                'totalGuesses': total_guesses,
                'avgGuesses': avg_guesses,
                'maxGuesses': max_guesses,
                'minGuesses': min_guesses
            },
            'time': {
                'slowestTime': max(details, key=lambda x: x['timeTakenMs'])['timeTakenMs'] if details else 0,
                'fastestTime': min(details, key=lambda x: x['timeTakenMs'])['timeTakenMs'] if details else 0,
                'totalTime': int((end_time - start_time) * 1000),
                'avgTime': int((end_time - start_time) * 1000 / (len(details) if details else 1))
            },
            'words': {
                'totalWords': ANSWER_LIST_LENGTH,
                'solvedWords': len([d for d in details if d['solved']]),
                'unsolvedWords': unsolved_words,
            },
            'distribution': dict(guess_distribution)
        },
        'details': details
    }
