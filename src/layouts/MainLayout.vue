<template>
  <q-layout view="hHh lpR fFf" class="tv-layout">
    <q-header class="tv-header">
      <q-toolbar class="tv-toolbar">
        <!-- 로고 -->
        <div class="tv-logo">
          <alpha-logo />
          <span class="tv-logo-text">
            Alpha<span class="tv-logo-accent">-ish</span>
          </span>
        </div>

        <!-- 검색창 -->
        <div class="tv-search-wrapper">
          <stock-search-input @select="onSymbolSelect" />
        </div>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>

    <q-footer class="tv-footer">
      <p class="tv-footer-text">© 2026 Alpha-ish. All rights reserved.</p>
    </q-footer>
  </q-layout>
</template>

<script setup lang="ts">
import AlphaLogo from 'components/AlphaLogo.vue';
import StockSearchInput from 'components/StockSearchInput.vue';
import type { StockSymbol } from 'src/types/stock';
import 'src/css/layout.css';

function onSymbolSelect(stock: StockSymbol) {
  // TODO: 차트 연동 시 선택된 종목 전달
  console.log('선택된 종목:', stock);
}
</script>
