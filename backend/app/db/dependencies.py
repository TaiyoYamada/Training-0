"""
依存性注入（DI）用データベースセッションプロバイダ。

FastAPI の Depends() 経由で各リクエストに
非同期DBセッションを提供する。
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_session_factory


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    リクエストスコープの非同期DBセッションを提供する。

    - 各リクエストに対して新しいセッションを生成
    - リクエスト終了時にセッションを自動クローズ
    - 例外発生時もセッションは確実にクローズされる（finally節）

    使用例:
        @router.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db_session)):
            ...
    """
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()
