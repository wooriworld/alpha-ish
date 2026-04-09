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
          <q-input
            v-model="searchQuery"
            dense
            outlined
            dark
            placeholder="심볼, 지표 검색..."
            class="tv-search-input"
          >
            <template #prepend>
              <q-icon name="search" class="tv-search-icon" />
            </template>
          </q-input>
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
import { ref } from 'vue';
import AlphaLogo from 'components/AlphaLogo.vue';
import 'src/css/layout.css';

const searchQuery = ref('');
</script>
