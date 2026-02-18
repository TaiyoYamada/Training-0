// SvelteKit 設定ファイル
// adapter-node: Node.js サーバーとしてビルド（Docker デプロイ向け）
import adapter from '@sveltejs/adapter-node';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
  // TypeScript / CSS プリプロセッサの有効化
  preprocess: vitePreprocess(),

  kit: {
    // Node.js アダプター（本番環境で node build で起動）
    adapter: adapter({
      out: 'build',       // ビルド出力先
      precompress: true,  // gzip / brotli 圧縮を事前生成
    }),
  },
};

export default config;
