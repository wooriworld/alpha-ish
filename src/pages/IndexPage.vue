<template>
  <q-page class="tv-page column" style="height: 0">
    <q-splitter v-model="splitterModel" :limits="[55, 85]" class="tv-splitter col">
      <!-- 차트 영역 -->
      <template #before>
        <div class="tv-chart-container">
          <div class="tv-chart-header">
            <div class="tv-chart-info">
              <div class="tv-chart-name-row">
                <h2 class="tv-chart-symbol">
                  {{ selectedStock ? (selectedStock.name_kr || selectedStock.description) : '-' }}
                </h2>
                <span v-if="currentPrice !== null" class="tv-chart-current-price">
                  {{ currentPrice }}
                </span>
              </div>
            </div>
            <div class="tv-timeframe-btns">
              <q-btn
                v-for="tf in timeframes"
                :key="tf.label"
                unelevated
                dense
                :label="tf.label"
                class="tv-tf-btn"
                :class="{ 'tv-tf-active': activeTimeframe === tf.label }"
                @click="activeTimeframe = tf.label"
              />
            </div>
          </div>

          <!-- 차트 -->
          <div class="tv-chart-area">
            <div v-if="!selectedStock" class="tv-chart-placeholder">
              <q-icon name="show_chart" size="64px" class="tv-chart-icon" />
              <p class="tv-chart-placeholder-text">종목을 검색하여 차트를 확인하세요</p>
            </div>
            <stock-chart
              v-else
              :candles="candles"
              :is-loading="isLoading"
              :error="error"
              :market="selectedStock?.market ?? MarketType.US"
            />
          </div>
        </div>
      </template>

      <!-- 전략 패널 -->
      <template #after>
        <strategy-panel @compare="showCompare = true" />
      </template>
    </q-splitter>

    <!-- 전략 비교 다이얼로그 -->
    <compare-dialog v-model="showCompare" />
  </q-page>
</template>

<script setup lang="ts">
import { ref, watch, computed, onMounted } from 'vue';
import { storeToRefs } from 'pinia';
import StrategyPanel from 'components/StrategyPanel.vue';
import CompareDialog from 'components/CompareDialog.vue';
import StockChart from 'components/StockChart.vue';
import { useSelectedStockStore } from 'src/stores/selectedStock';
import { useStockChart } from 'src/composables/useStockChart';
import { MarketType } from 'src/enum/market';
import 'src/css/chart.css';

const splitterModel = ref(72);
const showCompare = ref(false);

const timeframes = [
  { label: '1일', interval: '1d', range: '1y' },
  { label: '1주', interval: '1wk', range: '2y' },
  { label: '1개월', interval: '1mo', range: '5y' },
  { label: '3개월', interval: '3mo', range: '5y' },
  { label: '6개월', interval: '6mo', range: '10y' },
  { label: '1년', interval: '1y', range: '10y' },
  { label: '5년', interval: '5y', range: 'max' },
  { label: '전체', interval: 'max', range: 'max' },
];
const activeTimeframe = ref('1일');

const selectedStockStore = useSelectedStockStore();
const { stock: selectedStock } = storeToRefs(selectedStockStore);

const { candles, isLoading, error, load } = useStockChart();

onMounted(() => {
  if (selectedStock.value) void load(selectedStock.value.symbol);
});

watch(selectedStock, (stock) => {
  if (stock) void load(stock.symbol);
});

const currentPrice = computed(() => {
  const last = candles.value.at(-1);
  if (!last) return null;

  const market = selectedStock.value?.market ?? MarketType.US;
  if (market === MarketType.KRX) {
    return Math.round(last.close).toLocaleString('ko-KR') + '원';
  }
  const decimals = last.close >= 1 ? 2 : 4;
  return '$' + last.close.toLocaleString('en-US', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
});
</script>
