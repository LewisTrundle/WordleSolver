import React from 'react';
import type { SimulationResult } from '../services/simulation';

export interface SimulationPanelProps {
  simRunning?: boolean;
  simResult?: SimulationResult | null;
  startWord: string;
  runSimulationHandler: () => void;
}

export const SimulationPanel: React.FC<SimulationPanelProps> = ({
  simRunning,
  simResult,
  startWord,
  runSimulationHandler
}) => (
  <div className="flex flex-col gap-2 items-center mt-2 w-full">
    <div className="flex gap-2 w-full justify-center">
      <button
        className="mt-2 px-4 py-2 rounded bg-pink-700 text-white font-semibold hover:bg-pink-800 transition disabled:opacity-50"
        onClick={runSimulationHandler}
        disabled={simRunning || startWord.length !== 5}
      >
        {simRunning ? 'Running...' : 'Run Simulation'}
      </button>
      <button
        className="mt-2 px-4 py-2 rounded bg-gray-600 text-white font-semibold hover:bg-gray-700 transition disabled:opacity-50"
        onClick={() => console.log('Stop Simulation')}
        disabled={!simRunning}
      >
        Stop
      </button>
    </div>
    {simResult && (
      <div className="mt-2 p-2 bg-gray-800 text-white rounded text-xs w-full">
        <div><strong>Simulation Results</strong></div>
        <div>Strategy: {simResult.summary.strategy}</div>
        <div>Start Word: {simResult.summary.startWord}</div>
        <div>Hard Mode: {simResult.summary.hardMode ? 'Yes' : 'No'}</div>
        <div>Total Words: {simResult.stats.words.totalWords}</div>
        <div>Unsolved Words: {simResult.stats.words.unsolvedWords.length}</div>
        <div>Average Guesses: {simResult.stats.guesses.avgGuesses.toFixed(3)}</div>
        <div>Max Guesses: {simResult.stats.guesses.maxGuesses}</div>
        <div>Slowest Time: {simResult.stats.time.slowestTime}ms</div>
        <div>Fastest Time: {simResult.stats.time.fastestTime}ms</div>
        <div>Average Time: {simResult.stats.time.avgTime}ms</div>
        <div>Total Time: {(simResult.stats.time.totalTime / 1000).toFixed(2)}s</div>
        <div className="mt-2">
          <strong>Guess Distribution:</strong>
          <ul>
            {Object.entries(simResult.stats.distribution).map(([guesses, count]) => (
              <li key={guesses}>{guesses} guesses: {count}</li>
            ))}
          </ul>
        </div>
        {simResult.stats.words.unsolvedWords.length > 0 && (
          <div className="mt-2">
            <strong>Unsolved Words:</strong>
            <span> {simResult.stats.words.unsolvedWords.join(', ')}</span>
          </div>
        )}
        <details className="mt-2">
          <summary className="cursor-pointer">Show Per-Word Details</summary>
          <div style={{ maxHeight: 300, overflowY: 'auto' }}>
            {simResult.details.slice(0, 20).map(word => (
              <div key={word.answer} className="mb-2 p-2 border rounded">
                <div>
                  <strong>{word.answer}</strong> ({word.solved ? 'Solved' : 'Unsolved'}) - {word.guesses} guesses, {word.timeTakenMs}ms
                </div>
                <table className="w-full text-xs">
                  <thead>
                    <tr>
                      <th>#</th>
                      <th>Guess</th>
                      <th>Feedback</th>
                      <th>Score</th>
                      <th>Top Candidates</th>
                      <th>Possible Words</th>
                    </tr>
                  </thead>
                  <tbody>
                    {word.history.map(h => (
                      <tr key={h.guessNo}>
                        <td>{h.guessNo}</td>
                        <td>{h.guess}</td>
                        <td>{h.feedback}</td>
                        <td>{h.strategyScore !== undefined ? h.strategyScore?.toFixed(3) : '-'}</td>
                        <td>
                          {h.topCandidates
                            ? h.topCandidates.map(c => `${c.word} (${c.score !== undefined ? c.score?.toFixed(2) : '-'})`).join(', ')
                            : '-'}
                        </td>
                        <td>{h.possibleWordsCount}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ))}
            {simResult.details.length > 20 && <div>Showing first 20 words...</div>}
          </div>
        </details>
      </div>
    )}
  </div>
);
