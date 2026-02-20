# Training-0

プロジェクト管理アプリケーション。

## 🏗️ アーキテクチャ

```
Training-0/
├── backend/          # FastAPI (Python 3.13, async SQLAlchemy, PostgreSQL)
├── frontend/         # SvelteKit 5 (TypeScript, Svelte 5 Runes)
├── infra/            # Docker 本番設定, Nginx, スクリプト
├── .github/          # GitHub Actions CI/CD
└── docker-compose.yml
```

## 📦 技術スタック

| レイヤー | 技術 |
|---------|------|
| バックエンド | Python 3.13, FastAPI, SQLAlchemy 2.0 (async), Alembic, Pydantic v2 |
| フロントエンド | SvelteKit 5, Svelte 5, TypeScript |
| データベース | PostgreSQL 16 |
| インフラ | Docker, docker-compose, Nginx |
| CI/CD | GitHub Actions |
| パッケージ管理 | uv (backend), npm (frontend) |

## 📚 ドキュメント

開発に関する詳細な手順や情報については、`docs/` ディレクトリ配下のドキュメントを参照してください。

- **[🚀 セットアップ・開発ガイド](./docs/development.md)**
  - ローカル環境での起動手順
  - 開発時に使用するコマンド一覧
- **[📡 API エンドポイント](./docs/api.md)**
  - API機能の一覧と Swagger へのアクセス方法
- **[🏭 デプロイ・CI/CD](./docs/deployment.md)**
  - 本番環境での起動設定
  - GitHub Actions のワークフローについて
- **[📁 プロジェクト構成詳細](./docs/architecture.md)**
  - `backend/` および `frontend/` のディレクトリ構造詳細

## 📄 ライセンス

MIT
