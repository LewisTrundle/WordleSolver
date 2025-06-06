import axios from "./axios";

export type SimulationParams = {
  strategy: string;
  hardMode: boolean;
  startWord: string;
};

export type SimulationResult = {
  avgGuesses: number;
  maxGuesses: number;
  totalTimeMs: number;
  totalWords: number;
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
  return res.data;
}
