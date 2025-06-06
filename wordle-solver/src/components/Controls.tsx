import { LEVELS } from '../utils/levels';
import { ModeSelector } from './ModeSelector';
import type { SimulationResult } from '../services/simulation';

type ControlsProps = {
  level: number;
  setLevel: (level: number) => void;
  hardMode: boolean;
  setHardMode: (val: boolean) => void;
  mode: string;
  setMode: (m: 'random' | 'custom' | 'simulation') => void;
  customWord: string;
  setCustomWord: (w: string) => void;
  startWord: string;
  setStartWord: (w: string) => void;
  simRunning?: boolean;
  simResult?: SimulationResult | null;
  runSimulationHandler?: () => void;
};

export const Controls = ({
  level,
  setLevel,
  hardMode,
  setHardMode,
  mode,
  setMode,
  customWord,
  setCustomWord,
  startWord,
  setStartWord,
  simRunning,
  simResult,
  runSimulationHandler
}: ControlsProps) => (
  <div className="flex flex-col items-center gap-2 w-full mb-4">
    <ModeSelector mode={mode} setMode={setMode} />
    {mode === 'custom' && (
      <input
        className="border rounded px-2 py-1 text-center text-lg"
        type="text"
        maxLength={5}
        value={customWord}
        onChange={e => setCustomWord(e.target.value.replace(/[^a-zA-Z]/g, '').slice(0, 5))}
        placeholder="Enter 5-letter word"
      />
    )}
    {mode === 'simulation' && (
      <div className="flex flex-col gap-2 items-center w-full">
        <div className="flex flex-row items-center gap-4 mb-2">
          <label className="font-semibold">Solver Level:</label>
          <select
            className="rounded px-2 py-1 bg-gray-800 border border-gray-700 text-white"
            value={level}
            onChange={e => setLevel(Number(e.target.value))}
          >
            {LEVELS.map(l => (
              <option key={l.value} value={l.value}>{l.label}</option>
            ))}
          </select>
          <label className="flex items-center gap-2 ml-4">
            <input type="checkbox" checked={hardMode} onChange={e => setHardMode(e.target.checked)} />
            Hard Mode
          </label>
        </div>
        <label className="flex flex-col items-start w-full">
          <span className="mb-1 font-semibold">Starting Word:</span>
          <input
            className="border rounded px-2 py-1 w-full text-center text-lg"
            type="text"
            maxLength={5}
            value={startWord}
            onChange={e => setStartWord(e.target.value.replace(/[^a-zA-Z]/g, '').slice(0, 5))}
            placeholder="e.g. SLATE"
          />
        </label>
        {runSimulationHandler && (
          <button
            className="mt-2 px-4 py-2 rounded bg-pink-700 text-white font-semibold hover:bg-pink-800 transition disabled:opacity-50"
            onClick={runSimulationHandler}
            disabled={simRunning || startWord.length !== 5}
          >
            {simRunning ? 'Running...' : 'Run Simulation'}
          </button>
        )}
        {simResult && (
          <div className="mt-2 p-2 bg-gray-800 text-white rounded text-xs w-full">
            <div><strong>Simulation Results</strong></div>
            <div>Total Words: {simResult.totalWords}</div>
            <div>Average Guesses: {simResult.avgGuesses.toFixed(3)}</div>
            <div>Max Guesses: {simResult.maxGuesses}</div>
            <div>Total Time: {(simResult.totalTimeMs / 1000).toFixed(2)}s</div>
          </div>
        )}
      </div>
    )}
    {/* Show level/hardMode controls if not simulation mode */}
    {mode !== 'simulation' && (
      <div className="flex flex-row items-center gap-4 mb-2">
        <label className="font-semibold">Solver Level:</label>
        <select
          className="rounded px-2 py-1 bg-gray-800 border border-gray-700 text-white"
          value={level}
          onChange={e => setLevel(Number(e.target.value))}
        >
          {LEVELS.map(l => (
            <option key={l.value} value={l.value}>{l.label}</option>
          ))}
        </select>
        <label className="flex items-center gap-2 ml-4">
          <input type="checkbox" checked={hardMode} onChange={e => setHardMode(e.target.checked)} />
          Hard Mode
        </label>
      </div>
    )}
  </div>
);
