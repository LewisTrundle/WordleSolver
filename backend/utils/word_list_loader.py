import os

WORD_LIST_PATH = os.path.join(os.path.dirname(__file__), '../wordle_words.txt')
def load_word_list():
    with open(WORD_LIST_PATH, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

WORD_LIST = load_word_list()
