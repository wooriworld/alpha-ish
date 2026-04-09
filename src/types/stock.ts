import type { MarketType } from 'src/enum/market';

export interface StockSymbol {
  symbol: string;
  display_symbol: string;
  description: string;
  market: MarketType;
  type: string;
}
