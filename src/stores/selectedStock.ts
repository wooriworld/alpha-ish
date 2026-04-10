import { defineStore } from 'pinia';
import type { StockSymbol } from 'src/types/stock';
import { MarketType } from 'src/enum/market';

export const DEFAULT_STOCK: StockSymbol = {
  symbol: '005930.KS',
  display_symbol: '005930',
  description: 'Samsung Electronics',
  name_kr: '삼성전자',
  market: MarketType.KRX,
  exchange_name: 'KOSPI',
  logo_url: '',
  type: 'EQUITY',
};

export const useSelectedStockStore = defineStore('selectedStock', {
  state: () => ({
    stock: DEFAULT_STOCK,
  }),
  actions: {
    select(stock: StockSymbol) {
      this.stock = stock;
    },
  },
});
