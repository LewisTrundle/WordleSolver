interface ModeSelectorProps {
  mode: string;
  setMode: (m: 'random' | 'custom' | 'simulation') => void;
}

export const ModeSelector = ({ mode, setMode }: ModeSelectorProps) => {
  return (
    <div className="mb-2 flex gap-4">
      <label>
        <input
          type="radio"
          name="mode"
          value="random"
          checked={mode === 'random'}
          onChange={() => setMode('random')}
        />{' '}
        Random Word
      </label>
      <label>
        <input
          type="radio"
          name="mode"
          value="custom"
          checked={mode === 'custom'}
          onChange={() => setMode('custom')}
        />{' '}
        Custom Word
      </label>
      <label>
        <input
          type="radio"
          name="mode"
          value="simulation"
          checked={mode === 'simulation'}
          onChange={() => setMode('simulation')}
        />{' '}
        Simulation
      </label>
    </div>
  );
}
