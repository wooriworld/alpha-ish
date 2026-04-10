import type { MarketType } from 'src/enum/market';

export interface StockSymbol {
  symbol: string;
  display_symbol: string;
  description: string;
  name_kr: string;
  market: MarketType;
  exchange_name: string;
  logo_url: string;
  type: string;
}
