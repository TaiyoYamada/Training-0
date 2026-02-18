#!/bin/bash
# ===========================================
# DB起動待機スクリプト
#
# PostgreSQL が接続可能になるまで待機する。
# Docker Compose の depends_on + healthcheck の
# 補助スクリプトとして使用。
#
# 使い方:
#   ./wait-for-db.sh postgres 5432 training0
# ===========================================

set -e

HOST="${1:-postgres}"
PORT="${2:-5432}"
USER="${3:-training0}"
MAX_RETRIES="${4:-30}"
RETRY_INTERVAL="${5:-2}"

echo "⏳ データベース接続を待機中... (${HOST}:${PORT})"

retries=0
until pg_isready -h "$HOST" -p "$PORT" -U "$USER" > /dev/null 2>&1; do
  retries=$((retries + 1))
  if [ "$retries" -ge "$MAX_RETRIES" ]; then
    echo "❌ タイムアウト: データベースに接続できませんでした (${MAX_RETRIES} 回リトライ)"
    exit 1
  fi
  echo "  リトライ中... ($retries/$MAX_RETRIES)"
  sleep "$RETRY_INTERVAL"
done

echo "✅ データベース接続成功 (${HOST}:${PORT})"
