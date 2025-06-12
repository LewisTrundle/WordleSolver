import os

WORDLE_ANSWERS_PATH = os.path.join(os.path.dirname(__file__), '../data/wordle-answers.txt')
WORDLE_GUESSES_PATH = os.path.join(os.path.dirname(__file__), '../data/wordle-allowed-guesses.txt')
def load_wordle_answers():
    with open(WORDLE_ANSWERS_PATH, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
def load_wordle_guesses():
    with open(WORDLE_GUESSES_PATH, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

ANSWER_LIST = load_wordle_answers()
GUESS_LIST = load_wordle_guesses()
ANSWER_LIST_LENGTH = len(ANSWER_LIST)
GUESS_LIST_LENGTH = len(GUESS_LIST)
