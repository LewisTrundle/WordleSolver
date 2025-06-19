import time
from utils.word_list_loader import ANSWER_LIST, GUESS_LIST
from utils.filter import filter_words_custom, get_feedback_pattern


class GameState:
    def __init__(self, answer: str, start_word: str):
        self.answer = answer
        self.next_guess = start_word
        self.guesses = 0
        self.history = []
        self.possible_answers = list(ANSWER_LIST)
        self.possible_guesses = list(GUESS_LIST) + list(ANSWER_LIST)
        self.solved = False

    def add_history(self, feedback: str) -> None:
        self.history.append({
            'guess': self.next_guess,
            'feedback': feedback,
            'guessNo': self.guesses,
            'possibleWordsCount': len(self.possible_answers)
        })

    def update_possible_answers(self, feedback, use_guesses=False) -> None:
        self.possible_answers = filter_words_custom(self.next_guess, feedback, self.possible_answers)
        if use_guesses:
            self.possible_guesses = filter_words_custom(self.next_guess, feedback, self.possible_guesses)
        else:
            self.possible_guesses = self.possible_answers.copy()

    # Make a guess, update history, and check if solved
    # If not solved, update possible answers and choose next guess using provided strategy
    def make_guess(self, strategy_func, **kwargs):
        self.guesses += 1
        feedback = get_feedback_pattern(self.next_guess, self.answer)
        self.add_history(feedback)
        self.solved = (self.next_guess == self.answer)
        if not self.solved:
            self.update_possible_answers(feedback, use_guesses=kwargs.get('use_guesses', False))
            result = strategy_func(self.possible_answers, self.possible_guesses, **kwargs)
            #print(f"{self.answer} Guess #{self.guesses}: {self.next_guess} \n\t| {len(self.possible_answers)} - {self.possible_answers} \n\t|{len(self.possible_guesses)} - {self.possible_guesses} \n\t| next guess: {result['best_guess']} \n\t best guesses: {result['possible_words'][:10]}")
            if isinstance(result['best_guess'], dict):
                self.next_guess = result.get('best_guess', {}).get('word')
            else:
                self.next_guess = result['best_guess']

    def solve(self, strategy_func, **kwargs) -> dict:
        start_time = time.time()
        while not self.solved:
            if self.guesses >= 15:
                print(f"Exceeded max guesses: {self.guesses} for answer: {self.answer} with history: {self.history}")
                break
            self.make_guess(strategy_func, **kwargs)
        end_time = time.time()
        return {
            'answer': self.answer,
            'guesses': self.guesses,
            'timeTakenMs': int((end_time - start_time) * 1000),
            'solved': self.is_solved,
            'history': self.history
        }

    @property
    def is_solved(self) -> bool:
        # A game is only considered solved if the number of guesses is within the limit
        return self.solved and self.guesses <= 6