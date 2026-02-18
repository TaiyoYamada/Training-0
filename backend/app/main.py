"""
FastAPI アプリケーションエントリーポイント。

アプリケーションの初期化、ライフスパンイベント、
ミドルウェア設定、ルーター登録、構造化ロギングを行う。
"""

import logging
import sys
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api.router import api_router
from app.core.config import settings


def setup_logging() -> None:
    """
    構造化ロギングを設定する。

    環境モードに応じてログ形式を切り替え:
    - dev: 人間が読みやすいテキスト形式
    - prod: JSON 形式（ログ集約ツール向け）
    """
    # ルートロガーの設定
    root_logger = logging.getLogger()
    root_logger.setLevel(settings.log_level_int)

    # 既存のハンドラをクリア（重複防止）
    root_logger.handlers.clear()

    # コンソールハンドラの作成
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(settings.log_level_int)

    if settings.LOG_FORMAT == "json":
        # --- 本番環境向け: JSON 形式 ---
        # ログ集約ツール（CloudWatch, Datadog 等）でパースしやすい形式
        formatter = logging.Formatter(
            '{"time":"%(asctime)s","level":"%(levelname)s",'
            '"logger":"%(name)s","message":"%(message)s"}',
            datefmt="%Y-%m-%dT%H:%M:%S",
        )
    else:
        # --- 開発環境向け: テキスト形式 ---
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    handler.setFormatter(formatter)
    root_logger.addHandler(handler)

    # SQLAlchemy のログレベルを調整（DEBUGモード以外は抑制）
    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.DEBUG if settings.DEBUG else logging.WARNING
    )
    # uvicorn のアクセスログ
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)


# ロガーインスタンス
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    アプリケーションのライフスパンイベント。

    起動時: ロギング初期化、DB接続テスト
    シャットダウン時: リソースクリーンアップ
    """
    # --- 起動時の処理 ---
    setup_logging()

    logger.info("🚀 アプリケーション起動中...")
    logger.info("   アプリ名: %s", settings.APP_NAME)
    logger.info("   バージョン: %s", settings.APP_VERSION)
    logger.info("   環境: %s", settings.ENVIRONMENT.value)
    logger.info("   デバッグモード: %s", settings.DEBUG)
    logger.info("   ログレベル: %s", settings.LOG_LEVEL)

    # データベース接続テスト
    from app.db.session import async_engine

    try:
        async with async_engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("✅ データベース接続成功")
    except Exception as e:
        logger.error("❌ データベース接続失敗: %s", e)

    yield

    # --- シャットダウン時の処理 ---
    logger.info("🛑 アプリケーション終了中...")
    await async_engine.dispose()
    logger.info("✅ データベースエンジン破棄完了")


def create_app() -> FastAPI:
    """
    FastAPI アプリケーションファクトリ。

    テスト時にも使いやすいファクトリパターンを採用。
    本番環境では Swagger UI を無効化。
    """
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Training-0 バックエンドAPI",
        # 本番環境ではドキュメントを無効化
        docs_url="/docs" if not settings.is_production else None,
        redoc_url="/redoc" if not settings.is_production else None,
        openapi_url="/openapi.json" if not settings.is_production else None,
        lifespan=lifespan,
    )

    # --- CORS ミドルウェア ---
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # --- ルーター登録 ---
    app.include_router(api_router)

    return app


# アプリケーションインスタンス（uvicorn から参照される）
app = create_app()
