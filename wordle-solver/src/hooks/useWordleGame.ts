import { useState, useEffect, useCallback } from 'react';
import { getWordleFeedback } from '../utils/wordle';
import type { Feedback, HistoryEntry, Revealing } from '../utils/types';

export function useWordleGame(answer: string) {
  const [gameState, setGameState] = useState<{
    guess: string;
    feedback: Feedback;
    history: HistoryEntry[];
    revealing: Revealing;
    showAnswer: boolean;
  }>({
    guess: '',
    feedback: ['.', '.', '.', '.', '.'],
    history: [],
    revealing: null,
    showAnswer: false,
  });

  // Handles keyboard input for the Wordle game.
  // - Ignores input if an input field is focused or if a reveal animation is in progress.
  // - Appends letter keys to the guess (up to 5 letters).
  // - Handles backspace to remove the last letter.
  // - On Enter (with 5 letters), generates feedback and starts the reveal animation.
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Ignore if typing in an input field
      if (document.activeElement && (document.activeElement as HTMLElement).tagName === 'INPUT') return;
      // Block input during reveal animation
      if (gameState.revealing) return;
      // Handle letter input
      if (e.key.length === 1 && /[a-zA-Z]/.test(e.key)) {
        if (gameState.guess.length < 5) {
          setGameState(s => ({ ...s, guess: (s.guess + e.key.toLowerCase()).slice(0, 5) }));
        }
      } else if (e.key === 'Backspace') {
        // Remove last letter
        setGameState(s => ({ ...s, guess: s.guess.slice(0, -1) }));
      } else if (e.key === 'Enter' && gameState.guess.length === 5) {
        // Submit guess and start reveal
        const autoFeedback = getWordleFeedback(gameState.guess, answer);
        setGameState(s => ({ ...s, revealing: { guess: s.guess, feedback: autoFeedback, step: 0 } }));
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [gameState.guess, gameState.revealing, answer]);

  // Handles the step-by-step reveal animation for Wordle feedback.
  // - If a reveal is in progress (revealing is not null), increment the reveal step every 300ms.
  // - When all 5 letters are revealed, wait 400ms, then:
  //   - Add the guess and feedback to the history
  //   - Reset the guess and feedback state
  //   - Clear the revealing state to allow new input
  useEffect(() => {
    const { revealing } = gameState;
    if (!revealing) return;
    if (revealing.step < 5) {
      const timeout = setTimeout(() => {
        setGameState(s => ({
          ...s,
          revealing: s.revealing ? { ...s.revealing, step: s.revealing.step + 1 } : null,
        }));
      }, 300);
      return () => clearTimeout(timeout);
    } else {
      // After reveal, add to history and reset
      setTimeout(() => {
        setGameState(s => ({
          ...s,
          history: [...s.history, { guess: revealing.guess, feedback: revealing.feedback.join('') }],
          guess: '',
          feedback: ['.', '.', '.', '.', '.'],
          revealing: null,
        }));
      }, 400);
    }
  }, [gameState]);

  // Toggle showAnswer
  const toggleShowAnswer = useCallback(() => {
    setGameState(s => ({ ...s, showAnswer: !s.showAnswer }));
  }, []);

  // Expose state and setters
  return {
    ...gameState,
    setGameState,
    toggleShowAnswer,
  };
}
