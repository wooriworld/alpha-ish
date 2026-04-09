import type { StockSymbol } from 'src/types/stock';

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000';

export async function searchStocks(query: string, market = 'ALL'): Promise<StockSymbol[]> {
  const params = new URLSearchParams({ q: query, market, limit: '15' });
  const res = await fetch(`${API_BASE}/api/search?${params.toString()}`);
  if (!res.ok) throw new Error(`검색 실패: ${res.status}`);
  return res.json() as Promise<StockSymbol[]>;
}
