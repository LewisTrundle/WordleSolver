import { WordleGrid } from './components/WordleGrid';
import { useWordleGame } from './hooks/useWordleGame';
import { usePossibleWords } from './hooks/usePossibleWords';
import { StrategySidebar } from './components/StrategySidebar';
import { runSimulation } from './services/simulation';
import { useWordleControls } from './hooks/useWordleControls';
import { Controls } from './components/Controls';

function App() {
  const {
    controls: { mode, level, hardMode, customWord, startWord, simResult, simRunning},
    setControls: { setMode, setLevel, setHardMode, setCustomWord, setStartWord, setSimResult, setSimRunning },
    answer,
  } = useWordleControls();

  const { guess, feedback, history, revealing, showAnswer, toggleShowAnswer } = useWordleGame(answer);
  const { possibleWords, bestGuess } = usePossibleWords(history, level);

  // Calculate the top offset for the tooltip (align with current row)
  const rowHeight = 48;
  const currentRowIdx = revealing ? history.length : history.length;
  const tooltipTop = rowHeight * currentRowIdx;

  // Simulation runner
  async function runSimulationHandler() {
    setSimRunning(true);
    setSimResult(null);
    try {
      const strategy =
        level === 2 ? 'entropy' :
        level === 3 ? 'frequency' :
        level === 4 ? 'partition' :
        level === 5 ? 'minimax' :
        'filter';
      const result = await runSimulation({
        strategy,
        hardMode,
        startWord: startWord
      });
      setSimResult(result);
    } catch {
      setSimResult(null);
      // Optionally show error
    } finally {
      setSimRunning(false);
    }
  }

  return (
    <div className="page-container">
      <div className="wordle-main-container flex-1">
        <h1>Wordle Solver</h1>
        <Controls
          level={level}
          setLevel={setLevel}
          hardMode={hardMode}
          setHardMode={setHardMode}
          mode={mode}
          setMode={setMode}
          customWord={customWord}
          setCustomWord={setCustomWord}
          startWord={startWord}
          setStartWord={setStartWord}
          simRunning={simRunning}
          simResult={simResult}
          runSimulationHandler={runSimulationHandler}
        />
        {/* Only show the game UI if not in simulation mode */}
        {mode !== 'simulation' && (
          <>
            <button
              className="mb-4 px-4 py-2 rounded bg-pink-700 text-white font-semibold hover:bg-pink-800 transition"
              onClick={toggleShowAnswer}
            >
              {showAnswer ? `Answer: ${answer.toUpperCase()}` : "Reveal Answer"}
            </button>
            <div className="relative flex flex-col items-center">
              <WordleGrid history={history} revealing={revealing} guess={guess} feedback={feedback} />
              {bestGuess && (
                <div className="mb-2 text-pink-700 font-semibold">
                  Best Guess: <span className="font-mono">{bestGuess.toUpperCase()}</span>
                </div>
              )}
              {possibleWords.length > 0 && (
                <div
                  className="absolute right-[-180px] z-10"
                  style={{ top: tooltipTop, minWidth: 40 }}
                >
                  <div className="group relative inline-block">
                    <span className="bg-gray-800 text-white rounded px-2 py-1 text-xs cursor-pointer border border-pink-700">
                      {possibleWords.length} words
                    </span>
                    <div className="absolute left-1/2 -translate-x-1/2 mt-2 w-48 max-h-64 overflow-y-auto bg-white text-black border border-gray-400 rounded shadow-lg opacity-0 group-hover:opacity-100 pointer-events-none group-hover:pointer-events-auto transition-opacity duration-200 z-20 text-xs p-2">
                      {possibleWords.map(w => (
                        <div key={w}>{w}</div>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </div>
          </>
        )}
      </div>
      <StrategySidebar />
    </div>
  );
}

export default App;