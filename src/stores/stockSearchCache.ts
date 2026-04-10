import { defineStore } from 'pinia';
import type { StockSymbol } from 'src/types/stock';

export const useStockSearchCacheStore = defineStore('stockSearchCache', {
  state: () => ({
    cache: {} as Record<string, StockSymbol[]>,
  }),
  actions: {
    has(query: string): boolean {
      return query in this.cache;
    },
    get(query: string): StockSymbol[] {
      return this.cache[query] ?? [];
    },
    set(query: string, results: StockSymbol[]): void {
      this.cache[query] = results;
    },
  },
});
