"""
非同期データベースエンジン＆セッション設定モジュール。

SQLAlchemy 2.0 の非同期機能を使用して、
PostgreSQL (asyncpg) への接続を管理する。
"""

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

# --- 非同期エンジンの作成 ---
# pool_pre_ping: 接続の死活監視（stale connection 防止）
# echo: DEBUG時のみSQLログを出力
async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

# --- 非同期セッションファクトリの作成 ---
# expire_on_commit=False: コミット後にオブジェクトを期限切れにしない
# （非同期コンテキストでの lazy loading エラーを防止するため重要）
async_session_factory = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)
