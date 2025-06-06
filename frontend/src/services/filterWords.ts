import axios from "../services/axios";
import type { HistoryEntry } from "../utils/types";

export async function fetchFilteredWords(
  history: HistoryEntry[],
  endpoint?: string
): Promise<{ possible_words: string[]; best_guess: string | null }> {
  const url = `/${endpoint || "filter"}`;
  const res = await axios.post(url, { history });
  if (!res.data.possible_words && !res.data.best_guess) return { possible_words: [], best_guess: null };
  return { possible_words: res.data.possible_words, best_guess: res.data.best_guess };
}
