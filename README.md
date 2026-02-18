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

## 🚀 セットアップ

### 前提条件

- Docker Desktop
- Git

### 起動手順

```bash
# 1. リポジトリをクローン
git clone <repository-url>
cd Training-0

# 2. 環境変数ファイルを作成
cp .env.example .env

# 3. コンテナをビルド＆起動
docker compose up --build -d

# 4. 初回マイグレーション（初回のみ）
docker compose exec backend alembic revision --autogenerate -m "initial migration"
docker compose exec backend alembic upgrade head

# 5. アクセス確認
open http://localhost:5173    # フロントエンド
open http://localhost:8000/docs  # Swagger UI
curl http://localhost:8000/health  # ヘルスチェック
```

### 停止

```bash
docker compose down           # コンテナ停止
docker compose down -v        # コンテナ + データ削除
```

## 📡 API エンドポイント

| メソッド | パス | 説明 |
|---------|------|------|
| GET | `/health` | ヘルスチェック |
| GET | `/api/v1/projects` | プロジェクト一覧 |
| POST | `/api/v1/projects` | プロジェクト作成 |
| GET | `/api/v1/projects/{id}` | プロジェクト詳細 |
| PATCH | `/api/v1/projects/{id}` | プロジェクト更新 |
| DELETE | `/api/v1/projects/{id}` | プロジェクト削除 |
| GET | `/api/v1/projects/{id}/tasks` | タスク一覧 |
| POST | `/api/v1/projects/{id}/tasks` | タスク作成 |
| PATCH | `/api/v1/projects/{id}/tasks/{task_id}` | タスク更新 |
| DELETE | `/api/v1/projects/{id}/tasks/{task_id}` | タスク削除 |

## 🛠️ 開発コマンド

### バックエンド

```bash
cd backend

# 依存関係インストール
uv sync --dev

# 開発サーバー起動（ローカル）
uv run uvicorn app.main:app --reload --port 8000

# リント
uv run ruff check .

# フォーマット
uv run ruff format .

# 型チェック
uv run mypy app/
```

### フロントエンド

```bash
cd frontend

# 依存関係インストール
npm install

# 開発サーバー起動
npm run dev

# 型チェック
npm run check

# 本番ビルド
npm run build
```

## 🏭 本番デプロイ

```bash
# 本番用 docker-compose で起動
docker compose -f infra/docker/production-compose.yml up --build -d
```

本番構成では Nginx リバースプロキシが 80 番ポートで全トラフィックを処理し、
`/api/` → バックエンド、それ以外 → フロントエンドにルーティングします。

## 🔄 CI/CD

| ワークフロー | トリガー | 内容 |
|-------------|---------|------|
| `backend.yml` | push / PR（backend/ 変更時） | Ruff lint → Mypy → Pytest |
| `docker.yml` | push to main | Docker イメージビルド + SHA タグ |

## 📁 プロジェクト構成（詳細）

<details>
<summary>backend/</summary>

```
backend/
├── app/
│   ├── api/routes/          # API ルート定義
│   ├── core/config.py       # 環境設定（dev/staging/prod）
│   ├── db/                  # DB セッション + DI
│   ├── models/              # SQLAlchemy モデル
│   ├── repositories/        # データアクセス層
│   ├── schemas/             # Pydantic スキーマ
│   ├── services/            # ビジネスロジック
│   └── main.py              # エントリーポイント
├── alembic/                 # マイグレーション
├── Dockerfile               # マルチステージビルド
└── pyproject.toml           # uv プロジェクト定義
```
</details>

<details>
<summary>frontend/</summary>

```
frontend/
├── src/
│   ├── lib/
│   │   ├── api/client.ts    # fetch ベース API クライアント
│   │   ├── types/index.ts   # TypeScript 型定義
│   │   └── components/      # 共通コンポーネント
│   └── routes/
│       ├── +layout.svelte   # 共通レイアウト
│       ├── +page.svelte     # プロジェクト一覧
│       └── projects/[id]/   # プロジェクト詳細
├── Dockerfile               # マルチステージ（dev/production）
├── svelte.config.js
└── package.json
```
</details>

## 📄 ライセンス

MIT
