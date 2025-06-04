from collections import defaultdict

def best_guess_minimax(possible_words, get_feedback_pattern):
    """
    For each possible guess, find the worst-case (maximum) number of possible answers left after that guess for any feedback pattern.
    Returns the guess that minimizes this worst-case (minimax strategy) and a list of all possible words with their worst-case values.
    This method minimizes the maximum possible loss.
    """
    minimax_pairs = []
    for guess in possible_words:
        pattern_counts = defaultdict(int)
        for answer in possible_words:
            pattern = get_feedback_pattern(guess, answer)
            pattern_counts[pattern] += 1
        worst = max(pattern_counts.values())
        minimax_pairs.append({'word': guess, 'value': worst})
    best_entry = min(minimax_pairs, key=lambda x: x['value']) if minimax_pairs else {'word': None, 'value': -1}
    minimax_pairs.sort(key=lambda x: x['value'])
    return {'best_guess': best_entry, 'possible_words': minimax_pairs}
