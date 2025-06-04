export type Feedback = string[];
export type HistoryEntry = { guess: string; feedback: string };
export type Revealing = null | { guess: string; feedback: string[]; step: number };
