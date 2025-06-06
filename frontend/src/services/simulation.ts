import axios from "./axios";

export type SimulationParams = {
  strategy: string;
  hardMode: boolean;
  startWord: string;
};

export type SimulationWordHistory = {
  guess: string;
  feedback: string;
  guessNo: number;
  strategyScore?: number;
  topCandidates?: { word: string; score?: number }[];
  possibleWordsCount?: number;
};

export type SimulationWordDetail = {
  answer: string;
  guesses: number;
  timeTakenMs: number;
  solved: boolean;
  history: SimulationWordHistory[];
};

export type SimulationResult = {
  summary: {
    strategy: string;
    startWord: string;
    hardMode: boolean;
  };
  stats: {
    guesses: {
      totalGuesses: number;
      avgGuesses: number;
      maxGuesses: number;
      minGuesses: number;
    };
    time: {
      slowestTime: number;
      fastestTime: number;
      totalTime: number;
      avgTime: number;
    };
    words: {
      totalWords: number;
      unsolvedWords: string[];
    };
    distribution: Record<string, number>;
  };
  details: SimulationWordDetail[];
};

export async function runSimulation({
  strategy,
  hardMode,
  startWord
}: SimulationParams): Promise<SimulationResult> {
  const res = await axios.post("/simulate", {
    strategy,
    hardMode,
    startWord
  });
  console.log("Simulation result:", res.data);
  return res.data;
}
