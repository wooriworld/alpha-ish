<template>
  <div class="tv-strategy-panel">
    <!-- 실행 버튼 영역 -->
    <div class="tv-action-row">
      <q-btn
        unelevated
        class="tv-execute-btn"
        label="전략 실행"
        @click="handleExecute"
      />
      <q-btn
        unelevated
        class="tv-compare-btn"
        icon="bar_chart"
        title="전략 비교"
        @click="$emit('compare')"
      />
    </div>

    <!-- 전략 옵션 -->
    <q-card flat class="tv-options-card">
      <q-card-section>
        <div class="tv-section-title">전략 옵션</div>

        <div class="tv-form-row">
          <div class="tv-form-label">전략 선택</div>
          <q-select
            v-model="strategy"
            :options="strategyOptions"
            dense
            outlined
            dark
            class="tv-strategy-select"
          />
        </div>

        <div class="tv-form-row">
          <div class="tv-form-label">기간</div>
          <q-input
            v-model="period"
            type="number"
            dense
            outlined
            dark
            class="tv-period-input"
            placeholder="20"
          />
        </div>

        <div class="tv-form-row">
          <div class="tv-form-label">포지션 크기</div>
          <div class="tv-position-group">
            <q-input
              v-model="positionSize"
              type="number"
              dense
              outlined
              dark
              class="tv-pos-input"
              placeholder="1.0"
            />
            <q-select
              v-model="positionUnit"
              :options="['BTC', '%']"
              dense
              outlined
              dark
              class="tv-unit-select"
            />
          </div>
        </div>

        <div class="tv-form-row">
          <q-checkbox
            v-model="autoRebalance"
            label="자동 재조정"
            dark
            class="tv-auto-checkbox"
          />
        </div>
      </q-card-section>
    </q-card>

    <!-- 전략 리포트 탭 -->
    <q-card flat class="tv-report-card">
      <q-tabs
        v-model="activeTab"
        dense
        align="justify"
        class="tv-report-tabs"
        indicator-color="primary"
        active-color="white"
        inactive-color="grey-6"
      >
        <q-tab name="report1" label="보고서1" />
        <q-tab name="report2" label="보고서2" />
        <q-tab name="report3" label="보고서3" />
      </q-tabs>

      <q-separator dark />

      <q-tab-panels v-model="activeTab" animated class="tv-tab-panels">
        <q-tab-panel name="report1" class="tv-tab-panel">
          <report-stats title="전략 보고서 1 - SMA 전략" :stats="report1Stats" />
        </q-tab-panel>
        <q-tab-panel name="report2" class="tv-tab-panel">
          <report-stats title="전략 보고서 2 - RSI 전략" :stats="report2Stats" />
        </q-tab-panel>
        <q-tab-panel name="report3" class="tv-tab-panel">
          <report-stats title="전략 보고서 3 - MACD 전략" :stats="report3Stats" />
        </q-tab-panel>
      </q-tab-panels>
    </q-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import ReportStats from 'components/ReportStats.vue';
import 'src/css/strategy.css';

defineEmits(['compare']);

const strategy = ref('단순이동평균 (SMA)');
const strategyOptions = [
  '단순이동평균 (SMA)',
  '지수이동평균 (EMA)',
  'RSI 전략',
  'MACD 전략',
  '볼린저밴드',
];
const period = ref('20');
const positionSize = ref('1.0');
const positionUnit = ref('BTC');
const autoRebalance = ref(false);
const activeTab = ref('report1');

const report1Stats = [
  { label: '총 수익률', value: '+34.5%', type: 'positive' as const },
  { label: '총 거래 수', value: '127', type: 'neutral' as const },
  { label: '승률', value: '64.2%', type: 'neutral' as const },
  { label: '평균 수익', value: '+2.3%', type: 'positive' as const },
  { label: '평균 손실', value: '-1.1%', type: 'negative' as const },
  { label: '최대 낙폭', value: '-8.7%', type: 'negative' as const },
  { label: '샤프 비율', value: '1.84', type: 'neutral' as const },
];

const report2Stats = [
  { label: '총 수익률', value: '+28.3%', type: 'positive' as const },
  { label: '총 거래 수', value: '89', type: 'neutral' as const },
  { label: '승률', value: '71.9%', type: 'neutral' as const },
  { label: '평균 수익', value: '+3.1%', type: 'positive' as const },
  { label: '평균 손실', value: '-1.8%', type: 'negative' as const },
  { label: '최대 낙폭', value: '-6.2%', type: 'negative' as const },
  { label: '샤프 비율', value: '2.12', type: 'neutral' as const },
];

const report3Stats = [
  { label: '총 수익률', value: '+41.2%', type: 'positive' as const },
  { label: '총 거래 수', value: '156', type: 'neutral' as const },
  { label: '승률', value: '58.3%', type: 'neutral' as const },
  { label: '평균 수익', value: '+2.8%', type: 'positive' as const },
  { label: '평균 손실', value: '-0.9%', type: 'negative' as const },
  { label: '최대 낙폭', value: '-11.3%', type: 'negative' as const },
  { label: '샤프 비율', value: '1.67', type: 'neutral' as const },
];

function handleExecute() {
  // 전략 실행 (추후 구현)
}
</script>
