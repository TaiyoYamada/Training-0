"""
Alembic 非同期マイグレーション環境設定。

SQLAlchemy 2.0 の非同期エンジンを使用して、
PostgreSQL に対するマイグレーションを実行する。
"""

import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from app.core.config import settings
from app.db.base import Base

# --- 全モデルをインポート（Alembic がメタデータを認識するために必須） ---
from app.models.project import Project  # noqa: F401
from app.models.task import Task  # noqa: F401

# Alembic Config オブジェクト（alembic.ini の値にアクセス）
config = context.config

# ロギング設定の読み込み
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# マイグレーション対象のメタデータ
# Base.metadata に全モデルのテーブル情報が含まれる
target_metadata = Base.metadata

# データベースURLを設定から動的に注入
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)


def run_migrations_offline() -> None:
    """
    オフラインモードでマイグレーションを実行する。

    データベースに接続せず、SQL文のみを生成する。
    本番環境でのマイグレーションスクリプトの事前確認に使用。
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """マイグレーションの実行（同期コンテキスト）"""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """
    非同期エンジンを使用してマイグレーションを実行する。

    async_engine_from_config で非同期エンジンを作成し、
    run_sync でマイグレーションを同期的に実行する。
    """
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """
    オンラインモードでマイグレーションを実行する。

    非同期エンジンを使用してデータベースに接続し、
    マイグレーションを適用する。
    """
    asyncio.run(run_async_migrations())


# --- マイグレーション実行モードの選択 ---
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
