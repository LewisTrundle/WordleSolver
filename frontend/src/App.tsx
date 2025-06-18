import { useWordleControls } from './hooks/useWordleControls';
import { useSimulation } from './hooks/useSimulation';
import { StrategySidebar } from './components/StrategySidebar';
import { Controls } from './components/Controls';
import { GameBoard } from './components/GameBoard';
import { SimulationPanel } from './components/SimulationPanel';

function App() {
  const { controls, setControls, answer } = useWordleControls();
  const { mode, level, hardMode, startWord } = controls;
  const { simRunning, simResult, runSimulationHandler } = useSimulation();

  const handleRunSimulation = () => {
    runSimulationHandler(hardMode, startWord, level);
  };

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
            runSimulationHandler={handleRunSimulation}
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