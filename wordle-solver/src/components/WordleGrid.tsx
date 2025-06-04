import type { HistoryEntry, Revealing } from "../utils/types";
import { WordleRow } from "./WordleRow";

type WordleGridProps = {
  history: HistoryEntry[];
  revealing: null | Revealing;
  guess: string;
  feedback: string[];
};

export const WordleGrid = ({ history, revealing, guess, feedback }: WordleGridProps) => (
  <div className="wordle-grid-container">
    <div className="wordle-grid">
      {[...Array(6)].map((_, rowIdx) => {
        const rowState = {
          letters: [] as string[],
          feedback: [] as string[],
          revealStep: 5,
          isRevealing: false,
        };

        // If currently revealing a guess, show the revealing state for the current row
        if (revealing && rowIdx === history.length) {
          rowState.letters = revealing.guess.padEnd(5, " ").split("");
          rowState.feedback = revealing.feedback;
          rowState.revealStep = revealing.step;
          rowState.isRevealing = true;
        // If this row is a previous guess, show the guess and feedback from history
        } else if (rowIdx < history.length) {
          rowState.letters = history[rowIdx].guess.split("");
          rowState.feedback = history[rowIdx].feedback.split("");
        // If this is the current guess row (not revealing), show the current guess and feedback
        } else if (rowIdx === history.length && !revealing) {
          rowState.letters = guess.padEnd(5, " ").split("");
          rowState.feedback = feedback;
        // Otherwise, show an empty row
        } else {
          rowState.letters = Array(5).fill("");
          rowState.feedback = Array(5).fill(".");
        }
        return (
          <WordleRow
            key={rowIdx}
            letters={rowState.letters}
            feedback={rowState.feedback}
            revealStep={rowState.revealStep}
            revealing={rowState.isRevealing}
          />
        );
      })}
    </div>
  </div>
);
