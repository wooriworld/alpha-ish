import { defineStore } from 'pinia';
import type { StockSymbol } from 'src/types/stock';

export const useSelectedStockStore = defineStore('selectedStock', {
  state: () => ({
    stock: null as StockSymbol | null,
  }),
  actions: {
    select(stock: StockSymbol) {
      this.stock = stock;
    },
  },
});
