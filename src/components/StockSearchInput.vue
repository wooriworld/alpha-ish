<template>
  <!-- 헤더 내 검색 트리거 -->
  <div class="spotlight-trigger" @click="openSearch">
    <q-icon name="search" size="15px" class="spotlight-trigger__icon" />
    <span class="spotlight-trigger__text">Search</span>
    <kbd class="spotlight-trigger__kbd">⌘K</kbd>
  </div>

  <!-- Spotlight 오버레이 (body에 마운트) -->
  <Teleport to="body">
    <Transition name="spotlight">
      <div v-if="isOpen" class="spotlight-overlay" @click.self="closeSearch">
        <div class="spotlight-panel">
          <!-- 검색 입력 행 -->
          <div class="spotlight-input-row">
            <q-icon name="search" size="20px" class="spotlight-input-row__icon" />
            <input
              ref="inputRef"
              v-model="query"
              class="spotlight-input"
              placeholder="Search"
              autocomplete="off"
              spellcheck="false"
              @input="onInput"
              @keydown.escape.prevent="closeSearch"
              @keydown.arrow-down.prevent="moveFocus(1)"
              @keydown.arrow-up.prevent="moveFocus(-1)"
              @keydown.enter.prevent="selectFocused"
            />
            <button v-if="query" class="spotlight-input-row__clear" @click="clearQuery">
              <q-icon name="close" size="13px" />
            </button>
            <q-spinner
              v-else-if="isLoading"
              size="16px"
              color="blue-4"
              class="spotlight-input-row__spinner"
            />
          </div>

          <!-- 결과 영역 — 검색어가 있으면 선택 전까지 고정 표시 -->
          <div v-if="query" class="spotlight-body">
            <div class="spotlight-divider" />

            <!-- 로딩 중 -->
            <div v-if="isLoading && results.length === 0" class="spotlight-status">
              <q-spinner size="14px" color="blue-4" />
              <span>검색 중...</span>
            </div>

            <!-- 결과 없음 -->
            <div v-else-if="!isLoading && results.length === 0" class="spotlight-status">
              <q-icon name="search_off" size="18px" />
              <span>검색 결과가 없습니다.</span>
            </div>

            <!-- 결과 목록 -->
            <div v-else class="spotlight-results">
              <p class="spotlight-results__label">종목 / 지표</p>
              <div
                v-for="(item, idx) in results"
                :key="item.symbol"
                class="spotlight-item"
                :class="{ 'spotlight-item--focused': idx === focusedIdx }"
                @mouseenter="focusedIdx = idx"
                @click="selectItem(item)"
              >
                <!-- 로고 -->
                <div class="spotlight-item__logo">
                  <div class="spotlight-item__logo-fallback">
                    {{ (item.name_kr || item.description || item.display_symbol).charAt(0) }}
                  </div>
                </div>

                <!-- 티커 -->
                <span class="spotlight-item__code">{{ item.display_symbol }}</span>

                <!-- 종목명 (한글 우선, 없으면 영문) -->
                <span class="spotlight-item__name">{{
                  item.name_kr || item.description || '-'
                }}</span>

                <!-- 상장사 뱃지 -->
                <span
                  class="spotlight-item__exchange"
                  :class="getExchangeClass(item.exchange_name)"
                >
                  {{ item.exchange_name || item.market }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue';
import type { StockSymbol } from 'src/types/stock';
import { useStockSearch } from 'src/composables/useStockSearch';
import 'src/css/search.css';

const emit = defineEmits<{
  select: [stock: StockSymbol];
}>();

const { results, isLoading, search } = useStockSearch();

const isOpen = ref(false);
const query = ref('');
const focusedIdx = ref(-1);
const inputRef = ref<HTMLInputElement | null>(null);

function openSearch() {
  isOpen.value = true;
  focusedIdx.value = -1;
  void nextTick(() => inputRef.value?.focus());
}

function closeSearch() {
  isOpen.value = false;
  query.value = '';
  results.value = [];
  focusedIdx.value = -1;
}

function clearQuery() {
  query.value = '';
  results.value = [];
  focusedIdx.value = -1;
  inputRef.value?.focus();
}

function onInput(e: Event) {
  focusedIdx.value = -1;
  // v-model은 IME 조합 중 업데이트를 보류하므로 DOM 실제값을 직접 읽음
  const value = (e.target as HTMLInputElement).value;
  if (!value.trim()) {
    results.value = [];
    return;
  }
  void search(value);
}

function moveFocus(dir: number) {
  if (results.value.length === 0) return;
  const len = results.value.length;
  focusedIdx.value = (focusedIdx.value + dir + len) % len;
}

function selectFocused() {
  const item = results.value[focusedIdx.value];
  if (item) selectItem(item);
}

function selectItem(stock: StockSymbol) {
  emit('select', stock);
  closeSearch();
}

const EXCHANGE_CLASS_MAP: Record<string, string> = {
  KOSPI: 'spotlight-item__exchange--kospi',
  KOSDAQ: 'spotlight-item__exchange--kosdaq',
  KONEX: 'spotlight-item__exchange--konex',
  NASDAQ: 'spotlight-item__exchange--nasdaq',
  NYSE: 'spotlight-item__exchange--nyse',
  'NASDAQ GM': 'spotlight-item__exchange--nasdaq-gm',
  'NYSE Arca': 'spotlight-item__exchange--nyse-arca',
  'NYSE American': 'spotlight-item__exchange--nyse-american',
  'OTC Markets': 'spotlight-item__exchange--otc',
  'NASDAQ CM': 'spotlight-item__exchange--nasdaq-cm',
};

function getExchangeClass(exchangeName: string): string {
  return EXCHANGE_CLASS_MAP[exchangeName] ?? 'spotlight-item__exchange--otc';
}
</script>
