import { useState, useEffect } from 'react';
import { fetchRandomWord } from '../services/randomWord';

export function useRandomAnswer() {
  const [answer, setAnswer] = useState<string>('');
  useEffect(() => {
    fetchRandomWord().then(setAnswer);
  }, []);
  return [answer, setAnswer] as const;
}
