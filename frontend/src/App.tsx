import { useWordleControls } from './hooks/useWordleControls';
import { StrategySidebar } from './components/StrategySidebar';
import { runSimulation } from './services/simulation';
import { Controls } from './components/Controls';
import { GameBoard } from './components/GameBoard';
import { SimulationPanel } from './components/SimulationPanel';

function App() {
  const { controls, setControls, answer } = useWordleControls();
  const { mode, level, hardMode, startWord, simRunning, simResult } = controls;

  // Simulation runner
  async function runSimulationHandler() {
    setControls.setSimRunning?.(true);
    setControls.setSimResult?.(null);
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
      setControls.setSimResult?.(result);
    } catch {
      setControls.setSimResult?.(null);
      // Optionally show error
    } finally {
      setControls.setSimRunning?.(false);
    }
  }

  return (
    <div className="page-container">
      <div className="wordle-main-container flex-1">
        <h1>Wordle Solver</h1>
        <Controls
          controls={controls}
          setControls={setControls}
        />
        {mode === 'simulation' && (
          <SimulationPanel
            simRunning={simRunning}
            simResult={simResult}
            startWord={startWord}
            runSimulationHandler={runSimulationHandler}
          />
        )}
        {mode !== 'simulation' && (
          <GameBoard answer={answer} level={level} />
        )}
      </div>
      <StrategySidebar />
    </div>
  );
}

export default App;