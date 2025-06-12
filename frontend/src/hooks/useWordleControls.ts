import { useState } from 'react';
import { useRandomAnswer } from '../hooks/useRandomAnswer';
import type { SimulationResult } from '../services/simulation';


export function useWordleControls() {
  const [answerRandom] = useRandomAnswer();
  const [mode, setMode] = useState<'random' | 'custom' | 'simulation'>('random');
  const [level, setLevel] = useState<number>(1);
  const [hardMode, setHardMode] = useState<boolean>(false);
  const [customWord, setCustomWord] = useState<string>('');
  const [startWord, setStartWord] = useState<string>('salet');
  const [simResult, setSimResult] = useState<SimulationResult | null>(null);
  const [simRunning, setSimRunning] = useState<boolean>(false);

  const answer = mode === 'random' ? answerRandom : customWord.trim().toLowerCase();

  return {
    controls: {
      mode,
      level,
      hardMode,
      customWord,
      startWord,
      simResult,
      simRunning,
    },
    setControls: {
      setMode,
      setLevel,
      setHardMode,
      setCustomWord,
      setStartWord,
      setSimResult,
      setSimRunning,
    },
    answer,
  };
}
