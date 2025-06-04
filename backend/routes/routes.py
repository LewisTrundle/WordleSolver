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
