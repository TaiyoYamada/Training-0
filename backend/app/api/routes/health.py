"""
ヘルスチェック API ルート。

アプリケーションとデータベースの稼働状態を確認するためのエンドポイント。
ロードバランサーやモニタリングツールから利用される。
"""

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.dependencies import get_db_session
from app.schemas.health import HealthCheckResponse

router = APIRouter(tags=["ヘルスチェック"])


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    summary="ヘルスチェック",
    description="アプリケーションとDB接続の稼働状態を確認する",
)
async def health_check(
    db: AsyncSession = Depends(get_db_session),
) -> HealthCheckResponse:
    """
    ヘルスチェックエンドポイント。

    - アプリケーションの稼働状態を確認
    - PostgreSQL への接続を検証（SELECT 1 クエリ）
    - バージョン情報を返却
    """
    # データベース接続の確認
    db_status = "connected"
    try:
        await db.execute(text("SELECT 1"))
    except Exception:
        db_status = "disconnected"

    return HealthCheckResponse(
        status="healthy" if db_status == "connected" else "unhealthy",
        database=db_status,
        version=settings.APP_VERSION,
    )
