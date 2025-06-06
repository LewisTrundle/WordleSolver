
export const StrategySidebar = () => {
  return (
    <aside className="strategy-sidebar">
      <h2 className="strategy-title">Solve Strategies</h2>
      <div className="mb-4 text-xs text-gray-700">
        <strong>About Starting Words:</strong> <br />
        The best starting word in Wordle depends on the solving strategy you use. For example, words like <span className="font-mono">SLATE</span>, <span className="font-mono">CRANE</span>, and <span className="font-mono">RAISE</span> are often optimal for entropy-based strategies, as they maximize information gain. Frequency-based strategies favor words with the most common letters, such as <span className="font-mono">ARISE</span> or <span className="font-mono">TEARS</span>. Minimax and partition strategies may suggest different words that minimize the worst-case or average-case remaining possibilities. There is no single best starting word for all strategies—each method may have its own optimal choice.
      </div>
      <div className="strategy-section">
        <span className="strategy-label">Filter:</span> Simply picks a random word from the list of possible answers.
      </div>
      <div className="strategy-section">
        <span className="strategy-label">Entropy:</span> Chooses the word that maximizes information gain, aiming to reduce the set of possible answers as much as possible with each guess.
      </div>
      <div className="strategy-section">
        <span className="strategy-label">Frequency:</span> Picks the word with the most common letters among remaining possibilities, increasing the chance of hitting correct letters early.
      </div>
      <div className="strategy-section">
        <span className="strategy-label">Partition:</span> Selects the word that best splits the remaining words into even groups, making it easier to narrow down the answer.
      </div>
      <div className="strategy-section">
        <span className="strategy-label">Minimax:</span> Minimizes the worst-case number of remaining words after a guess, ensuring the hardest scenario is as easy as possible.
      </div>
    </aside>
  );
}
