from flask import Blueprint, request, jsonify # type: ignore
from utils.filter import (
    get_filtered_words_from_data,
    get_feedback_pattern
)
import random
from services.entropy_strategy import best_guess_entropy as entropy_strategy
from services.frequency_strategy import best_guess_frequency as frequency_strategy
from services.partition_strategy import best_guess_partition as partition_strategy
from services.minimax_strategy import best_guess_minimax as minimax_strategy
from services.random_word_service import get_random_word

wordle_bp = Blueprint('wordle', __name__)

@wordle_bp.route('/random', methods=['GET'])
def random_word():
    word = get_random_word()
    return jsonify({"word": word})

@wordle_bp.route('/filter', methods=['POST'])
def filter_words():
    data = request.get_json(silent=True)
    possible_words = get_filtered_words_from_data(data)
    return jsonify({"possible_words": possible_words, "best_guess": random.choice(possible_words)})


@wordle_bp.route('/entropy', methods=['POST'])
def best_guess_entropy():
    data = request.get_json(silent=True)
    possible_words = get_filtered_words_from_data(data)
    result = entropy_strategy(possible_words)
    return jsonify(result)


@wordle_bp.route('/frequency', methods=['POST'])
def best_guess_frequency():
    data = request.get_json(silent=True)
    possible_words = get_filtered_words_from_data(data)
    result = frequency_strategy(possible_words)
    return jsonify(result)


@wordle_bp.route('/partition', methods=['POST'])
def best_guess_partition():
    data = request.get_json(silent=True)
    possible_words = get_filtered_words_from_data(data)
    result = partition_strategy(possible_words, get_feedback_pattern)
    return jsonify(result)


@wordle_bp.route('/minimax', methods=['POST'])
def best_guess_minimax():
    data = request.get_json(silent=True)
    possible_words = get_filtered_words_from_data(data)
    result = minimax_strategy(possible_words, get_feedback_pattern)
    return jsonify(result)


@wordle_bp.route('/simulate', methods=['POST'])
def simulate_wordle():
    """
    Run a simulation of solving all possible answers using the selected strategy, hard mode, and starting word.
    Expects JSON: { 'strategy': 'entropy'|'frequency'|'partition'|'minimax'|'filter', 'hardMode': bool, 'startWord': str }
    Returns: { avgGuesses, maxGuesses, totalTimeMs, totalWords }
    """
    import time
    data = request.get_json(silent=True) or {}
    strategy = data.get('strategy', 'filter')
    hard_mode = bool(data.get('hardMode', False))
    start_word = str(data.get('startWord', 'slate')).lower()

    # Map strategy string to function
    strategy_map = {
        'entropy': lambda words: entropy_strategy(words)['best_guess']['word'],
        'frequency': lambda words: frequency_strategy(words)['best_guess']['word'],
        'partition': lambda words: partition_strategy(words, get_feedback_pattern)['best_guess']['word'],
        'minimax': lambda words: minimax_strategy(words, get_feedback_pattern)['best_guess']['word'],
        'filter': lambda words: random.choice(words),
    }
    pick_next = strategy_map.get(strategy, strategy_map['filter'])

    # Load all possible answers
    from utils.word_list_loader import WORD_LIST
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
            # Filter possible words based on history
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
    return jsonify({
        'avgGuesses': total_guesses / len(all_answers),
        'maxGuesses': max_guesses,
        'totalTimeMs': int((end_time - start_time) * 1000),
        'totalWords': len(all_answers)
    })
