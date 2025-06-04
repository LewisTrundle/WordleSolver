
interface WordleRowProps {
  letters: string[];
  feedback: string[];
  revealStep: number;
  revealing: boolean;
}

export const WordleRow = ({ letters, feedback, revealStep, revealing }: WordleRowProps) => (
  <div className="wordle-row">
    {letters.map((letter, colIdx) => {
      let cellClass = "wordle-cell wordle-bg-default";
      if (feedback[colIdx] === "g" && (!revealing || colIdx < revealStep)) cellClass = "wordle-cell wordle-bg-green";
      else if (feedback[colIdx] === "y" && (!revealing || colIdx < revealStep)) cellClass = "wordle-cell wordle-bg-yellow";
      else if (feedback[colIdx] === "." && letter !== "" && (!revealing || colIdx < revealStep)) cellClass = "wordle-cell wordle-bg-grey";
      return (
        <div
          key={colIdx}
          className={cellClass}
        >
          {letter.toUpperCase()}
        </div>
      );
    })}
  </div>
);
