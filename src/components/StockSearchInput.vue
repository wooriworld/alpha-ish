<template>
  <q-select
    v-model="selected"
    :options="options"
    use-input
    hide-selected
    fill-input
    input-debounce="0"
    dense
    outlined
    dark
    placeholder="심볼, 지표 검색..."
    class="tv-search-select"
    popup-content-class="tv-search-popup"
    @filter="onFilter"
    @update:model-value="onSelect"
  >
    <template #prepend>
      <q-icon name="search" size="16px" />
    </template>

    <template #append>
      <q-spinner v-if="isLoading" size="14px" color="blue-5" />
    </template>

    <template #option="scope">
      <q-item v-bind="scope.itemProps">
        <div class="stock-option">
          <span
            class="stock-option__badge"
            :class="scope.opt.market === 'KRX' ? 'stock-option__badge--krx' : 'stock-option__badge--us'"
          >
            {{ scope.opt.market }}
          </span>
          <div class="stock-option__info">
            <span class="stock-option__symbol">{{ scope.opt.display_symbol }}</span>
            <span class="stock-option__name">{{ scope.opt.description }}</span>
          </div>
        </div>
      </q-item>
    </template>

    <template #no-option>
      <div class="tv-search-empty">
        {{ isLoading ? '검색 중...' : '검색 결과가 없습니다.' }}
      </div>
    </template>
  </q-select>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import type { StockSymbol } from 'src/types/stock';
import { useStockSearch } from 'src/composables/useStockSearch';
import 'src/css/search.css';

const emit = defineEmits<{
  select: [stock: StockSymbol];
}>();

const selected = ref<StockSymbol | null>(null);
const options = ref<StockSymbol[]>([]);
const { isLoading, search } = useStockSearch();

function onFilter(query: string, done: (callbackFn: () => void) => void) {
  void search(query).then((data) => {
    done(() => {
      options.value = data;
    });
  });
}

function onSelect(stock: StockSymbol | null) {
  if (!stock) return;
  emit('select', stock);
  selected.value = null;
}
</script>
