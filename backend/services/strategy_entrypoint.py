from utils.filter import filter_possible_words
from .entropy.entropy import entropy


def strategy_entrypoint(possible_answers=None, possible_guesses=None, history=None, **kwargs):
    if possible_answers is None:
        if history is None: return
        possible_answers = filter_possible_words(history)
    if possible_guesses is None:
        possible_guesses = possible_answers
    return entropy(possible_answers, possible_guesses, **kwargs)