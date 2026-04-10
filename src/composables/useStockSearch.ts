import { ref } from 'vue';
import { debounce } from 'lodash';
import type { StockSymbol } from 'src/types/stock';
import { searchStocks } from 'src/services/stockSearchService';
import { useStockSearchCacheStore } from 'src/stores/stockSearchCache';

export function useStockSearch() {
  const results = ref<StockSymbol[]>([]);
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  const cacheStore = useStockSearchCacheStore();

  const search = debounce(async (query: string) => {
    const trimmed = query.trim();
    if (!trimmed) {
      results.value = [];
      return;
    }

    // 캐시 히트 시 API 생략
    if (cacheStore.has(trimmed)) {
      results.value = cacheStore.get(trimmed);
      return;
    }

    isLoading.value = true;
    error.value = null;

    try {
      const data = await searchStocks(trimmed);
      cacheStore.set(trimmed, data);
      results.value = data;
    } catch {
      error.value = '검색 중 오류가 발생했습니다.';
      results.value = [];
    } finally {
      isLoading.value = false;
    }
  }, 300);

  return { results, isLoading, error, search };
}
