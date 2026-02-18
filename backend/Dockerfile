# ===========================================
# Training-0 Dockerfile
# Python 3.13 + uv + FastAPI
# マルチステージビルド + 非rootユーザー
# ===========================================

# =========================================
# ステージ1: ビルダー（依存関係のインストール）
# =========================================
FROM python:3.13-slim AS builder

# uv のインストール（高速パッケージマネージャー）
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 作業ディレクトリの設定
WORKDIR /app

# 依存関係定義ファイルのコピー（キャッシュ活用のため先にコピー）
COPY pyproject.toml ./

# 依存関係のインストール（本番用のみ）
# --no-dev: 開発用依存関係を除外
# --frozen: ロックファイルを固定（再現性を保証）
RUN uv sync --no-dev --no-install-project

# =========================================
# ステージ2: ランタイム（最終イメージ）
# =========================================
FROM python:3.13-slim AS runtime

# セキュリティ: 非rootユーザーの作成
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid 1000 --create-home appuser

WORKDIR /app

# ビルダーステージから仮想環境をコピー
COPY --from=builder /app/.venv /app/.venv

# アプリケーションコードのコピー
COPY app/ ./app/
COPY alembic/ ./alembic/
COPY alembic.ini ./
COPY pyproject.toml ./

# 環境変数の設定
# PATH に仮想環境の bin を追加（uv が作成した .venv を使用）
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 非rootユーザーに切り替え
USER appuser

# ポートの公開
EXPOSE 8000

# ヘルスチェック（Docker のヘルスチェック機能）
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# アプリケーション起動コマンド
# --host 0.0.0.0: 全インターフェースでリッスン（コンテナ内から外部アクセス可能に）
# --port 8000: ポート番号
# --workers 1: ワーカー数（開発環境用。本番では増やす）
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
