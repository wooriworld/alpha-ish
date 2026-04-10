import type { Candle } from 'src/types/chart';

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000';

export async function fetchCandles(
  symbol: string,
  interval = '1d',
  range = '1y',
): Promise<Candle[]> {
  const params = new URLSearchParams({ symbol, interval, range });
  const res = await fetch(`${API_BASE}/api/chart?${params.toString()}`);
  if (!res.ok) throw new Error(`차트 조회 실패: ${res.status}`);
  return res.json() as Promise<Candle[]>;
}
