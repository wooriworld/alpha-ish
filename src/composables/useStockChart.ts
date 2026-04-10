import { ref } from 'vue';
import type { Candle } from 'src/types/chart';
import { fetchCandles } from 'src/services/chartService';

export function useStockChart() {
  const candles = ref<Candle[]>([]);
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  async function load(symbol: string) {
    isLoading.value = true;
    error.value = null;
    candles.value = [];

    try {
      candles.value = await fetchCandles(symbol, '1d', '3mo');
    } catch {
      error.value = '차트 데이터를 불러오지 못했습니다.';
    } finally {
      isLoading.value = false;
    }
  }

  return { candles, isLoading, error, load };
}
