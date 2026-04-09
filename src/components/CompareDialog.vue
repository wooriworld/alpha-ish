<template>
  <q-dialog v-model="isOpen" class="tv-compare-dialog">
    <q-card class="tv-compare-card">
      <!-- 헤더 -->
      <q-card-section class="tv-compare-header row items-center justify-between no-wrap">
        <div class="tv-compare-title">전략 보고서 비교</div>
        <q-btn
          flat
          dense
          round
          icon="close"
          class="tv-close-btn"
          @click="isOpen = false"
        />
      </q-card-section>

      <q-separator dark />

      <!-- 비교 테이블 -->
      <q-card-section class="tv-compare-content">
        <q-markup-table flat dark class="tv-compare-table">
          <thead>
            <tr>
              <th class="text-left tv-th-label">지표</th>
              <th class="text-center tv-th-report">
                보고서 1
                <span class="tv-th-strategy">SMA 전략</span>
              </th>
              <th class="text-center tv-th-report">
                보고서 2
                <span class="tv-th-strategy">RSI 전략</span>
              </th>
              <th class="text-center tv-th-report">
                보고서 3
                <span class="tv-th-strategy">MACD 전략</span>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in compareRows" :key="row.label">
              <td class="tv-td-label">{{ row.label }}</td>
              <td
                class="text-center"
                :class="getValueClass(row.values[0])"
              >
                {{ row.values[0] }}
                <span v-if="row.best === 0" class="tv-best-badge">★ 최고</span>
              </td>
              <td
                class="text-center"
                :class="getValueClass(row.values[1])"
              >
                {{ row.values[1] }}
                <span v-if="row.best === 1" class="tv-best-badge">★ 최고</span>
              </td>
              <td
                class="text-center"
                :class="getValueClass(row.values[2])"
              >
                {{ row.values[2] }}
                <span v-if="row.best === 2" class="tv-best-badge">★ 최고</span>
              </td>
            </tr>
          </tbody>
        </q-markup-table>

        <!-- 종합 분석 -->
        <q-card flat class="tv-analysis-card">
          <q-card-section>
            <div class="tv-analysis-title">종합 분석</div>
            <ul class="tv-analysis-list">
              <li>
                <span class="tv-highlight-green">보고서 3 (MACD)</span>:
                가장 높은 총 수익률 (+41.2%)과 가장 적은 평균 손실 (-0.9%)
              </li>
              <li>
                <span class="tv-highlight-blue">보고서 2 (RSI)</span>:
                가장 높은 승률 (71.9%)과 샤프 비율 (2.12), 가장 낮은 최대 낙폭 (-6.2%)
              </li>
              <li>
                <span class="tv-highlight-yellow">보고서 1 (SMA)</span>:
                안정적인 중간 성과, 균형 잡힌 전략
              </li>
            </ul>
          </q-card-section>
        </q-card>
      </q-card-section>

      <!-- 액션 -->
      <q-card-actions align="right" class="tv-compare-actions">
        <q-btn
          unelevated
          label="닫기"
          class="tv-close-action-btn"
          @click="isOpen = false"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import 'src/css/compare.css';

const props = defineProps<{ modelValue: boolean }>();
const emit = defineEmits(['update:modelValue']);

const isOpen = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val),
});

const compareRows = [
  { label: '총 수익률', values: ['+34.5%', '+28.3%', '+41.2%'], best: 2 },
  { label: '총 거래 수', values: ['127', '89', '156'], best: -1 },
  { label: '승률', values: ['64.2%', '71.9%', '58.3%'], best: 1 },
  { label: '평균 수익', values: ['+2.3%', '+3.1%', '+2.8%'], best: 1 },
  { label: '평균 손실', values: ['-1.1%', '-1.8%', '-0.9%'], best: 2 },
  { label: '최대 낙폭', values: ['-8.7%', '-6.2%', '-11.3%'], best: 1 },
  { label: '샤프 비율', values: ['1.84', '2.12', '1.67'], best: 1 },
];

function getValueClass(value: string | undefined): string {
  if (!value) return 'tv-neutral';
  if (value.startsWith('+')) return 'tv-positive';
  if (value.startsWith('-')) return 'tv-negative';
  return 'tv-neutral';
}
</script>
