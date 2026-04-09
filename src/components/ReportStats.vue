<template>
  <div class="tv-report-stats">
    <div class="tv-report-title">{{ title }}</div>
    <div
      v-for="stat in stats"
      :key="stat.label"
      class="tv-stat-row"
    >
      <span class="tv-stat-label">{{ stat.label }}</span>
      <span :class="['tv-stat-value', `tv-stat-${stat.type}`]">{{ stat.value }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import 'src/css/strategy.css';

defineProps<{
  title: string;
  stats: Array<{
    label: string;
    value: string;
    type: 'positive' | 'negative' | 'neutral';
  }>;
}>();
</script>
