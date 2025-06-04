import { LEVELS } from '../utils/levels';

type ControlsProps = {
  level: number;
  setLevel: (level: number) => void;
  hardMode: boolean;
  setHardMode: (val: boolean) => void;
};

export const Controls = ({ level, setLevel, hardMode, setHardMode }: ControlsProps) => (
  <div className="flex flex-row items-center gap-4 mb-4">
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
);
