import { ref } from 'vue';
import type { StockSymbol } from 'src/types/stock';
import { searchStocks } from 'src/services/stockSearchService';

export function useStockSearch() {
  const results = ref<StockSymbol[]>([]);
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  let debounceTimer: ReturnType<typeof setTimeout> | null = null;

  async function search(query: string): Promise<StockSymbol[]> {
    return new Promise((resolve) => {
      if (debounceTimer) clearTimeout(debounceTimer);

      if (!query.trim()) {
        results.value = [];
        resolve([]);
        return;
      }

      debounceTimer = setTimeout(() => {
        isLoading.value = true;
        error.value = null;
        searchStocks(query)
          .then((data) => {
            results.value = data;
            resolve(data);
          })
          .catch(() => {
            error.value = '검색 중 오류가 발생했습니다.';
            results.value = [];
            resolve([]);
          })
          .finally(() => {
            isLoading.value = false;
          });
      }, 300);
    });
  }

  return { results, isLoading, error, search };
}
