from collections import Counter

def best_guess_frequency(possible_words):
    """
    For each possible word, calculate a frequency score based on how common its letters are in each position among all possible words.
    Returns the word with the highest frequency score and a list of all possible words with their scores.
    This method favors words with common letters in each slot.
    """
    letter_counts = [Counter() for _ in range(5)]
    for word in possible_words:
        for i, c in enumerate(word):
            letter_counts[i][c] += 1
    def score(word):
        return sum(letter_counts[i][c] for i, c in enumerate(word))
    frequency_pairs = [
        {'word': word, 'value': score(word)}
        for word in possible_words
    ]
    best_guess = max(frequency_pairs, key=lambda x: x['value']) if frequency_pairs else {'word': None, 'value': -1}
    frequency_pairs.sort(key=lambda x: x['value'], reverse=True)
    return {'best_guess': best_guess, 'possible_words': frequency_pairs}
