// Wordle feedback logic
export function getWordleFeedback(guess: string, answer: string): string[] {
  const feedback = Array(5).fill('.');
  const answerArr = answer.split('');
  const guessArr = guess.split('');
  const used = Array(5).fill(false);

  // First pass: green
  for (let i = 0; i < 5; i++) {
    if (guessArr[i] === answerArr[i]) {
      feedback[i] = 'g';
      used[i] = true;
      answerArr[i] = '';
    }
  }
  // Second pass: yellow
  for (let i = 0; i < 5; i++) {
    if (feedback[i] === 'g') continue;
    const idx = answerArr.findIndex((a, j) => a === guessArr[i] && !used[j]);
    if (idx !== -1) {
      feedback[i] = 'y';
      used[idx] = true;
      answerArr[idx] = '';
    }
  }
  return feedback;
}
