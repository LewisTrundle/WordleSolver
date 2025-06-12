from utils.word_list_loader import ANSWER_LIST


def get_filtered_words_from_data(data):
    history = data.get('history', []) if data else []
    possible_words = filter_possible_words(history)
    return possible_words


def filter_possible_words(history):
    possible_words = ANSWER_LIST.copy()
    for entry in history:
        guess = entry.get('guess', '')
        feedback = entry.get('feedback', '')
        if guess and feedback and len(guess) == 5 and len(feedback) == 5:
            possible_words = filter_words_custom(guess, feedback, possible_words)
    return possible_words


def filter_words_custom(guess, feedback, answers):
    filtered = []
    #print(f"{guess} {feedback} {len(answers)} words before filtering", flush=True)
    for word in answers:
        valid = True
        for i in range(5):
            g, f = guess[i], feedback[i]
            # If the letter is green, it must match the word at that position
            if f == 'g' and word[i] != g:
                valid = False
                break
        if not valid:
            continue
        for i in range(5):
            g, f = guess[i], feedback[i]
            # If the letter is yellow, it must be in the word but not at that position
            if f == 'y':
                if g not in word or word[i] == g:
                    valid = False
                    break
        if not valid:
            continue
        for i in range(5):
            g, f = guess[i], feedback[i]
            # If the letter is gray, it must not be in the word
            if f == '.':
                allowed = sum(1 for j in range(5) if guess[j] == g and feedback[j] in ('g', 'y'))
                if word.count(g) > allowed:
                    valid = False
                    break
        if not valid:
            continue
        # Always enforce hard mode: all green/yellow letters must be present
        for i, (g, f) in enumerate(zip(guess, feedback)):
            if f in ('g', 'y') and g not in word:
                valid = False
                break
        if valid:
            filtered.append(word)
    return filtered


def get_feedback_pattern(guess, answer):
    pattern = ['.'] * 5
    answer_chars = list(answer)
    for i in range(5):
        if guess[i] == answer[i]:
            pattern[i] = 'g'
            answer_chars[i] = None  # Mark as used
    for i in range(5):
        if pattern[i] == '.' and guess[i] in answer_chars:
            pattern[i] = 'y'
            answer_chars[answer_chars.index(guess[i])] = None
    return ''.join(pattern)


