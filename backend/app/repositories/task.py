"""
Task リポジトリ。

BaseRepository を継承し、Task モデル固有の
データベース操作を追加する。
論理削除フィルタやプロジェクトID別取得をサポート。
"""

import math
import uuid
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.repositories.base import BaseRepository


class TaskRepository(BaseRepository[Task]):
    """
    Task モデル用リポジトリ。

    基底CRUDに加え、以下のカスタムクエリを提供:
    - プロジェクトIDでのタスク一覧取得（ページネーション付き）
    - 論理削除されたタスクのフィルタリング
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Task, session)

    async def get_by_project_id(
        self,
        project_id: uuid.UUID,
        *,
        page: int = 1,
        per_page: int = 20,
        include_deleted: bool = False,
    ) -> dict[str, Any]:
        """
        特定のプロジェクトに属するタスク一覧を取得する。

        Args:
            project_id: 対象プロジェクトのUUID
            page: ページ番号（1始まり）
            per_page: 1ページあたりの件数
            include_deleted: 論理削除されたタスクを含めるか

        Returns:
            items, total, page, per_page, pages を含む辞書
        """
        # 基本的な条件: プロジェクトIDでフィルタ
        conditions = [Task.project_id == project_id]

        # 論理削除フィルタ（デフォルトでは削除済みを除外）
        if not include_deleted:
            conditions.append(Task.is_deleted == False)  # noqa: E712

        # 全件数を取得
        count_stmt = select(func.count()).select_from(Task).where(*conditions)
        total_result = await self.session.execute(count_stmt)
        total = total_result.scalar_one()

        # ページネーション付きでデータを取得
        offset = (page - 1) * per_page
        stmt = select(Task).where(*conditions).offset(offset).limit(per_page)
        result = await self.session.execute(stmt)
        items = list(result.scalars().all())

        return {
            "items": items,
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": math.ceil(total / per_page) if total > 0 else 0,
        }

    async def soft_delete(self, record_id: uuid.UUID) -> Task | None:
        """
        タスクを論理削除する（is_deleted = True に設定）。

        物理削除ではなく、フラグを立てることでデータを保持する。

        Args:
            record_id: 対象タスクのUUID

        Returns:
            更新されたタスクインスタンス、見つからなければ None
        """
        return await self.update(record_id, {"is_deleted": True})
