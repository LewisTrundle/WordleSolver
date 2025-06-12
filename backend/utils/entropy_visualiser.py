import matplotlib.pyplot as plt
from wordle_guesser import score_words_by_entropy, ANSWER_LIST

def plot_entropy_distribution(possible_words):
    scored = score_words_by_entropy(possible_words)
    words, entropies = zip(*scored[:50])  # Top 50 for clarity

    plt.figure(figsize=(12, 6))
    bars = plt.bar(words, entropies, color="skyblue")
    plt.xticks(rotation=90)
    plt.ylabel("Entropy (bits)")
    plt.title("Top 50 Guesses by Entropy")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_entropy_distribution(ANSWER_LIST)
