<template>
  <div ref="wrapEl" class="stock-chart-wrap">
    <div ref="chartEl" class="stock-chart-el" />

    <div v-if="isLoading" class="stock-chart-overlay">
      <q-spinner size="32px" color="blue-4" />
      <span>차트 불러오는 중...</span>
    </div>

    <div v-else-if="error" class="stock-chart-overlay">
      <q-icon name="error_outline" size="32px" color="negative" />
      <span>{{ error }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onBeforeUnmount, nextTick } from 'vue';
import {
  createChart,
  CandlestickSeries,
  TickMarkType,
  type IChartApi,
  type ISeriesApi,
  type UTCTimestamp,
} from 'lightweight-charts';
import type { Candle } from 'src/types/chart';
import { MarketType } from 'src/enum/market';
import 'src/css/chart.css';

const props = defineProps<{
  candles: Candle[];
  isLoading: boolean;
  error: string | null;
  market: MarketType;
}>();

function formatPrice(price: number): string {
  if (props.market === MarketType.KRX) {
    return Math.round(price).toLocaleString('ko-KR');
  }
  // US: 1달러 이상은 소수점 2자리, 미만은 4자리
  const decimals = price >= 1 ? 2 : 4;
  return price.toLocaleString('en-US', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
}

const wrapEl = ref<HTMLElement | null>(null);
const chartEl = ref<HTMLElement | null>(null);
let chart: IChartApi | null = null;
let series: ISeriesApi<'Candlestick'> | null = null;
let chartReady = false;

function initChart(width: number, height: number) {
  if (!chartEl.value || chartReady) return;
  chartReady = true;

  const isKRX = props.market === MarketType.KRX;

  chart = createChart(chartEl.value, {
    width,
    height,
    layout: {
      background: { color: '#1a1d29' },
      textColor: '#9598a1',
    },
    grid: {
      vertLines: { color: '#2a2e3e' },
      horzLines: { color: '#2a2e3e' },
    },
    crosshair: {
      vertLine: { color: '#5d6a7e' },
      horzLine: { color: '#5d6a7e' },
    },
    rightPriceScale: { borderColor: '#2a2e3e' },
    timeScale: {
      borderColor: '#2a2e3e',
      timeVisible: true,
      tickMarkFormatter: (time: number, tickMarkType: TickMarkType) => {
        const d = new Date(time * 1000);
        const mm = String(d.getMonth() + 1).padStart(2, '0');
        const dd = String(d.getDate()).padStart(2, '0');
        // Year 레벨은 연도, 그 외는 MM/DD
        if (tickMarkType === TickMarkType.Year) {
          return String(d.getFullYear());
        }
        return `${mm}/${dd}`;
      },
    },
  });

  series = chart.addSeries(CandlestickSeries, {
    upColor: '#26a69a',
    downColor: '#ef5350',
    borderUpColor: '#26a69a',
    borderDownColor: '#ef5350',
    wickUpColor: '#26a69a',
    wickDownColor: '#ef5350',
    priceFormat: {
      type: 'custom',
      minMove: isKRX ? 1 : 0.01,
      formatter: (price: number) => formatPrice(price),
    },
  });

  if (props.candles.length) renderCandles(props.candles);
}

function renderCandles(candles: Candle[]) {
  if (!series) return;
  series.setData(
    candles.map((c) => ({
      time: c.time as UTCTimestamp,
      open: c.open,
      high: c.high,
      low: c.low,
      close: c.close,
    })),
  );
  chart?.timeScale().fitContent();
}

// wrapEl의 실제 크기가 잡히는 순간 차트 초기화
const resizeObserver = new ResizeObserver((entries) => {
  const { width, height } = entries[0]!.contentRect;
  if (width === 0 || height === 0) return;

  if (!chartReady) {
    initChart(width, height);
  } else {
    chart?.resize(width, height);
  }
});

onMounted(() => {
  if (wrapEl.value) resizeObserver.observe(wrapEl.value);
});

onBeforeUnmount(() => {
  resizeObserver.disconnect();
  chart?.remove();
});

watch(
  () => props.candles,
  async (candles) => {
    if (!candles.length) return;
    await nextTick();
    renderCandles(candles);
  },
);
</script>
