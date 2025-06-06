import React from 'react';
import type { SimulationResult } from '../services/simulation';

interface SimulationPanelProps {
  simRunning?: boolean;
  simResult?: SimulationResult | null;
  startWord: string;
  runSimulationHandler: () => void;
}

export const SimulationPanel: React.FC<SimulationPanelProps> = ({
  simRunning,
  simResult,
  startWord,
  runSimulationHandler,
}) => (
  <div className="flex flex-col gap-2 items-center mt-2 w-full">
    <button
      className="mt-2 px-4 py-2 rounded bg-pink-700 text-white font-semibold hover:bg-pink-800 transition disabled:opacity-50"
      onClick={runSimulationHandler}
      disabled={simRunning || startWord.length !== 5}
    >
      {simRunning ? 'Running...' : 'Run Simulation'}
    </button>
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
);
