import axios from "../services/axios";

export async function fetchRandomWord(): Promise<string> {
  const res = await axios.get("/random");
  return res.data.word;
}
