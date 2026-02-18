"""
API ルーター集約モジュール。

全てのルートモジュールをまとめて、
メインアプリケーションに登録する単一のルーターを提供する。
"""

from fastapi import APIRouter

from app.api.routes import health, projects, tasks

# メインAPIルーター（全ルートの集約ポイント）
api_router = APIRouter()

# --- ヘルスチェック（プレフィックスなし） ---
api_router.include_router(health.router)

# --- バージョン付きAPIルート ---
# /api/v1 プレフィックスで名前空間を分離
# 将来的な v2 API との共存を可能にする
api_router.include_router(projects.router, prefix="/api/v1")
api_router.include_router(tasks.router, prefix="/api/v1")
