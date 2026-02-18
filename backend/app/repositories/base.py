"""
ジェネリック CRUD リポジトリ基底クラス。

型パラメータを使用して、全モデルに共通する
CRUD操作（Create / Read / Update / Delete）を汎用的に実装する。
"""

import math
import uuid
from typing import Any, Generic, TypeVar

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Base

# SQLAlchemy モデルの型パラメータ（Baseを継承した任意のモデル）
ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    ジェネリック CRUD リポジトリ。

    全モデルに共通するデータベース操作を提供する基底クラス。
    具体的なモデルクラスを型パラメータとして受け取り、
    型安全な操作を実現する。

    使用例:
        class ProjectRepository(BaseRepository[Project]):
            def __init__(self, session: AsyncSession):
                super().__init__(Project, session)
    """

    def __init__(self, model: type[ModelType], session: AsyncSession) -> None:
        """
        リポジトリを初期化する。

        Args:
            model: 操作対象の SQLAlchemy モデルクラス
            session: 非同期DBセッション
        """
        self.model = model
        self.session = session

    async def create(self, data: dict[str, Any]) -> ModelType:
        """
        新しいレコードを作成する。

        Args:
            data: モデルのフィールド名と値の辞書

        Returns:
            作成されたモデルインスタンス
        """
        instance = self.model(**data)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def get_by_id(self, record_id: uuid.UUID) -> ModelType | None:
        """
        IDでレコードを取得する。

        Args:
            record_id: 検索対象のUUID

        Returns:
            見つかった場合はモデルインスタンス、なければ None
        """
        stmt = select(self.model).where(self.model.id == record_id)  # type: ignore[attr-defined]
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_multi(
        self,
        *,
        page: int = 1,
        per_page: int = 20,
    ) -> dict[str, Any]:
        """
        ページネーション付きでレコード一覧を取得する。

        Args:
            page: ページ番号（1始まり）
            per_page: 1ページあたりの件数

        Returns:
            items, total, page, per_page, pages を含む辞書
        """
        # 全件数を取得
        count_stmt = select(func.count()).select_from(self.model)
        total_result = await self.session.execute(count_stmt)
        total = total_result.scalar_one()

        # ページネーション付きでデータを取得
        offset = (page - 1) * per_page
        stmt = select(self.model).offset(offset).limit(per_page)
        result = await self.session.execute(stmt)
        items = list(result.scalars().all())

        return {
            "items": items,
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": math.ceil(total / per_page) if total > 0 else 0,
        }

    async def update(
        self, record_id: uuid.UUID, data: dict[str, Any]
    ) -> ModelType | None:
        """
        既存のレコードを部分更新する。

        Args:
            record_id: 更新対象のUUID
            data: 更新するフィールド名と値の辞書（Noneの値は除外済みであること）

        Returns:
            更新されたモデルインスタンス、見つからなければ None
        """
        instance = await self.get_by_id(record_id)
        if instance is None:
            return None

        # 渡された値のみを更新（部分更新）
        for key, value in data.items():
            setattr(instance, key, value)

        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def delete(self, record_id: uuid.UUID) -> bool:
        """
        レコードを物理削除する。

        Args:
            record_id: 削除対象のUUID

        Returns:
            削除成功: True、レコードが見つからない: False
        """
        instance = await self.get_by_id(record_id)
        if instance is None:
            return False

        await self.session.delete(instance)
        await self.session.commit()
        return True
