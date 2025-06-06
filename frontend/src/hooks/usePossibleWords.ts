import { useState, useEffect } from 'react';
import type { HistoryEntry } from '../utils/types';
import { fetchFilteredWords } from '../services/filterWords';

const endpoints = [
  'filter',
  'entropy',
  'frequency',
  'partition',
  'minimax',
  'nonanswer',
  'heuristic',
];

type WordScore = { word: string; value: number };
type ApiResponse = {
  possible_words: string[] | WordScore[];
  best_guess: string | null | WordScore;
};

export function usePossibleWords(history: HistoryEntry[], algorithmLevel: number) {
  const [possibleWords, setPossibleWords] = useState<string[]>([]);
  const [bestGuess, setBestGuess] = useState<string | null>(null);

  useEffect(() => {
    if (history.length > 0) {
      const endpoint = endpoints[algorithmLevel-1] || 'filter';
      fetchFilteredWords(history, endpoint).then((res: ApiResponse) => {
        let words: string[] = [];
        let best: string | null = null;
        switch (algorithmLevel) {
          case 1:
            words = Array.isArray(res.possible_words) ? (res.possible_words as string[]) : [];
            best = res.best_guess as string;
            break;
          default:
            words = (res.possible_words as WordScore[]).map((entry) => `${entry.word} (${entry.value.toFixed(2)})`);
            best = `${(res.best_guess as WordScore).word} (${(res.possible_words as WordScore[])[0]?.value.toFixed(2)})`;
        }
        setPossibleWords(words);
        setBestGuess(best);
      });
    } else {
      setPossibleWords([]);
      setBestGuess(null);
    }
  }, [history, algorithmLevel]);

  return {
    possibleWords, bestGuess
  };
}
