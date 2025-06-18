import { useState, useCallback } from 'react';
import { runSimulation } from '../services/simulation';

export function useSimulation() {
  const [simRunning, setSimRunning] = useState(false);
  const [simResult, setSimResult] = useState<any>(null);

  const runSimulationHandler = useCallback(
    async (hardMode: boolean, startWord: string, level: number) => {
      setSimRunning(true);
      setSimResult(null);
      try {
        const simStrategy =
          level === 2 ? 'entropy' :
          level === 3 ? 'frequency' :
          level === 4 ? 'partition' :
          level === 5 ? 'minimax' :
          'filter';
        const result = await runSimulation({
          strategy: simStrategy,
          hardMode,
          startWord
        });
        setSimResult(result);
      } catch {
        setSimResult(null);
      } finally {
        setSimRunning(false);
      }
    },
    []
  );

  return {
    simRunning,
    simResult,
    setSimResult,
    setSimRunning,
    runSimulationHandler
  };
}
