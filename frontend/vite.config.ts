// Vite 設定ファイル
// API プロキシ設定を含む（開発時のCORS問題を回避）
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
    plugins: [sveltekit()],
    server: {
        // 開発サーバーの API プロキシ設定
        // /api へのリクエストをバックエンドに転送（CORS回避）
        proxy: {
            '/api': {
                target: 'http://backend:8000',
                changeOrigin: true,
            },
            '/health': {
                target: 'http://backend:8000',
                changeOrigin: true,
            },
        },
    },
});
