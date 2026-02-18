<!--
  Header コンポーネント

  アプリケーション全体の共通ヘッダー。
  ナビゲーションとアプリ名を表示する。
-->
<script lang="ts">
  // Svelte 5 Runes を使用
  let { currentPage = '' }: { currentPage?: string } = $props();
</script>

<header class="header">
  <div class="header-inner container">
    <a href="/" class="logo">
      <span class="logo-icon">⚡</span>
      <span class="logo-text">Training-0</span>
    </a>
    <nav class="nav">
      <a href="/" class="nav-link" class:active={currentPage === 'home'}>
        プロジェクト
      </a>
    </nav>
  </div>
</header>

<style>
  .header {
    background: var(--color-bg-secondary);
    border-bottom: 1px solid var(--color-border);
    position: sticky;
    top: 0;
    z-index: 100;
    backdrop-filter: blur(12px);
  }

  .header-inner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 60px;
  }

  .logo {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    color: var(--color-text-primary);
    font-weight: 700;
    font-size: var(--font-size-lg);
  }

  .logo:hover {
    color: var(--color-text-primary);
  }

  .logo-icon {
    font-size: var(--font-size-xl);
  }

  .nav {
    display: flex;
    gap: var(--space-4);
  }

  .nav-link {
    color: var(--color-text-secondary);
    font-size: var(--font-size-sm);
    font-weight: 500;
    padding: var(--space-2) var(--space-3);
    border-radius: var(--radius-sm);
    transition: all var(--transition-fast);
  }

  .nav-link:hover,
  .nav-link.active {
    color: var(--color-text-primary);
    background: var(--color-bg-hover);
  }
</style>
