<template>
  <q-page class="tv-page column">
    <q-splitter
      v-model="splitterModel"
      :limits="[55, 85]"
      class="tv-splitter col"
    >
      <!-- 차트 영역 -->
      <template #before>
        <div class="tv-chart-container">
          <div class="tv-chart-header">
            <div class="tv-chart-info">
              <h2 class="tv-chart-symbol">BTC/USDT</h2>
              <div class="tv-chart-price-row">
                <span class="tv-price-value">$50,234.56</span>
                <span class="tv-price-change positive">+2.34%</span>
              </div>
            </div>
            <div class="tv-timeframe-btns row q-gutter-xs">
              <q-btn
                v-for="tf in timeframes"
                :key="tf"
                unelevated
                dense
                :label="tf"
                class="tv-tf-btn"
                :class="{ 'tv-tf-active': activeTimeframe === tf }"
                @click="activeTimeframe = tf"
              />
            </div>
          </div>

          <!-- 차트 플레이스홀더 (추후 TradingView Lightweight Charts 연동) -->
          <div class="tv-chart-area">
            <div class="tv-chart-placeholder">
              <q-icon name="show_chart" size="64px" class="tv-chart-icon" />
              <p class="tv-chart-placeholder-text">차트 영역 (TradingView Lightweight Charts)</p>
            </div>
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
import { ref } from 'vue';
import StrategyPanel from 'components/StrategyPanel.vue';
import CompareDialog from 'components/CompareDialog.vue';
import 'src/css/chart.css';

const splitterModel = ref(72);
const showCompare = ref(false);
const activeTimeframe = ref('1분');
const timeframes = ['1분', '5분', '1시간', '1일'];
</script>
