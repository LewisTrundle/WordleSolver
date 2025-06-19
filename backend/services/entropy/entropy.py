from concurrent.futures import ThreadPoolExecutor, as_completed
from .calculate_entropy import calculate_entropy
from .entropy_cache import save_entropy_cache

def entropy(possible_answers, possible_guesses, sort=False, parallel=False, 
            use_entropy_cache=False, use_feedback_cache=False, 
            use_precomputed_entropy=False, use_precomputed_feedback=False):
    entropy_pairs = []
    best_entry = {'word': None, 'value': -1}

    def entropy_worker(guess):
        val = calculate_entropy(guess, possible_answers, use_precomputed, use_cache)
        return {'word': guess, 'value': val}

    if parallel:
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(entropy_worker, guess): guess for guess in possible_guesses}
            for future in as_completed(futures):
                entry = future.result()
                entropy_pairs.append(entry)
    else:
        for guess in possible_guesses:
            entry = entropy_worker(guess)
            entropy_pairs.append(entry)

    if sort:
        entropy_pairs.sort(key=lambda x: x['value'], reverse=True)
        best_entry = entropy_pairs[0] if entropy_pairs else {'word': None, 'value': -1}
    else:
        best_entry = max(entropy_pairs, key=lambda x: x['value']) if entropy_pairs else {'word': None, 'value': -1}

    save_entropy_cache()
    return {'best_guess': best_entry, 'possible_words': entropy_pairs}
