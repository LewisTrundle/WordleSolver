import time
import random
from collections import defaultdict
from utils.word_list_loader import WORD_LIST
from utils.filter import get_feedback_pattern
from services.entropy_strategy import best_guess_entropy as entropy_strategy
from services.frequency_strategy import best_guess_frequency as frequency_strategy
from services.partition_strategy import best_guess_partition as partition_strategy
from services.minimax_strategy import best_guess_minimax as minimax_strategy

# Map strategy names to their respective functions
STRATEGY_MAP = {
    'entropy': lambda words: _format_strategy_result(entropy_strategy(words)),
    'frequency': lambda words: _format_simple_strategy_result(frequency_strategy(words)),
    'partition': lambda words: _format_simple_strategy_result(partition_strategy(words, get_feedback_pattern)),
    'minimax': lambda words: _format_simple_strategy_result(minimax_strategy(words, get_feedback_pattern)),
    'filter': lambda words: (random.choice(words), None, None),
}

def _format_strategy_result(result):
    # For strategies that return candidates and scores (like entropy)
    best = result['best_guess']
    top_candidates = []
    if 'candidates' in result:
        for cand in result['candidates'][:3]:
            top_candidates.append({'word': cand['word'], 'score': cand.get('score')})
    return best['word'], best.get('score'), top_candidates

def _format_simple_strategy_result(result):
    # For strategies that only return a best guess
    best = result['best_guess']
    return best['word'], None, None

def pick_next_guess(strategy: str, possible_words):
    """
    Pick the next guess using the selected strategy.
    Always returns (next_guess, strategy_score, top_candidates).
    """
    pick_func = STRATEGY_MAP.get(strategy, STRATEGY_MAP['filter'])
    return pick_func(possible_words)


def simulate_single_word(answer: str, strategy: str, start_word: str, all_answers: list) -> dict:
    guesses = 1
    possible_words = list(all_answers)
    history = []
    current_guess = start_word
    solved = (current_guess == answer)
    start_time = time.time()

    # First guess
    feedback = get_feedback_pattern(current_guess, answer)
    next_guess, strategy_score, top_candidates = pick_next_guess(strategy, possible_words)
    history.append({
        'guess': current_guess,
        'feedback': feedback,
        'guessNo': guesses,
        'strategyScore': strategy_score,
        'topCandidates': top_candidates,
        'possibleWordsCount': len(possible_words)
    })
    if current_guess == answer:
        end_time = time.time()
        return {
            'answer': answer,
            'guesses': guesses,
            'timeTakenMs': int((end_time - start_time) * 1000),
            'solved': True,
            'history': history
        }

    while not solved:
        # Filter possible words based on feedback history
        possible_words = [w for w in possible_words if get_feedback_pattern(current_guess, w) == feedback]
        if not possible_words:
            break
        # --- STRATEGY IS CALLED HERE ---
        next_guess, strategy_score, top_candidates = pick_next_guess(strategy, possible_words)
        guesses += 1
        feedback = get_feedback_pattern(next_guess, answer)
        history.append({
            'guess': next_guess,
            'feedback': feedback,
            'guessNo': guesses,
            'strategyScore': strategy_score,
            'topCandidates': top_candidates,
            'possibleWordsCount': len(possible_words)
        })
        current_guess = next_guess
        if current_guess == answer:
            solved = True
    end_time = time.time()
    is_solved = solved and guesses <= 6
    return {
        'answer': answer,
        'guesses': guesses,
        'timeTakenMs': int((end_time - start_time) * 1000),
        'solved': is_solved,
        'history': history
    }


def simulate_wordle_service(strategy: str = 'filter', hard_mode: bool = False, start_word: str = 'slate'):
    strategy = strategy
    hard_mode = bool(hard_mode)
    start_word = str(start_word).lower()
    all_answers = [w for w in WORD_LIST if len(w) == 5][:200]
    total_words = len(all_answers)
    details = []
    guess_distribution = defaultdict(int)
    start_time = time.time()
    for answer in all_answers:
        result = simulate_single_word(answer, strategy, start_word, all_answers)
        details.append(result)
        guess_distribution[result['guesses']] += 1
    end_time = time.time()
    total_guesses = sum(int(k) * v for k, v in guess_distribution.items())
    avg_guesses = total_guesses / total_words if total_words else 0
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
                'slowestTime': max(details, key=lambda x: x['timeTakenMs'])['timeTakenMs'],
                'fastestTime': min(details, key=lambda x: x['timeTakenMs'])['timeTakenMs'],
                'totalTime': int((end_time - start_time) * 1000),
                'avgTime': int((end_time - start_time) * 1000 / len(all_answers))
            },
            'words': {
                'totalWords': total_words,
                'solvedWords': total_words - len(unsolved_words),
                'unsolvedWords': unsolved_words,
            },
            'distribution': dict(guess_distribution)
        },
        'details': details
    }
