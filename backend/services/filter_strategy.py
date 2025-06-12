import random

def filter_strategy(possible_words):
    return {'best_guess': random.choice(possible_words), 'possible_words': possible_words}