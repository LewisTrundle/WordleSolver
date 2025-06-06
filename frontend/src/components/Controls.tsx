import { LEVELS } from '../utils/levels';
import { ModeSelector } from './ModeSelector';
import type { SimulationResult } from '../services/simulation';

// Grouped props for cleaner usage
export type ControlsProps = {
  controls: {
    mode: string;
    level: number;
    hardMode: boolean;
    customWord: string;
    startWord: string;
    simRunning?: boolean;
    simResult?: SimulationResult | null;
  };
  setControls: {
    setMode: (m: 'random' | 'custom' | 'simulation') => void;
    setLevel: (level: number) => void;
    setHardMode: (val: boolean) => void;
    setCustomWord: (w: string) => void;
    setStartWord: (w: string) => void;
  };
};

export const Controls = ({ controls, setControls }: ControlsProps) => {
  const { mode, level, hardMode, customWord, startWord } = controls;
  const { setMode, setLevel, setHardMode, setCustomWord, setStartWord } = setControls;
  return (
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
};
