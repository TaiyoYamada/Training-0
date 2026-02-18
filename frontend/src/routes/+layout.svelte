<!--
  共通レイアウト

  全ページに適用されるレイアウトコンポーネント。
  ヘッダーとメインコンテンツ領域を定義する。
-->
<script lang="ts">
  import '../app.css';
  import Header from '$lib/components/Header.svelte';

  let { children } = $props();
</script>

<div class="app">
  <Header />
  <main class="main">
    {@render children()}
  </main>
</div>

<style>
  .app {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }

  .main {
    flex: 1;
    padding: var(--space-8) 0;
  }
</style>
