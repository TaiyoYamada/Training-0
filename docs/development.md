# 開発・セットアップガイド

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
