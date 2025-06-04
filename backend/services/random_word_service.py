import random
from utils.word_list_loader import WORD_LIST

def get_random_word():
    """
    Returns a random word from the provided word list.
    """
    return random.choice(WORD_LIST)
