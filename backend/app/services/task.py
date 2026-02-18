"""
Task サービス層。

タスク操作のビジネスロジック。
プロジェクトの存在確認を含むバリデーションを提供。
"""

import uuid
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.project import ProjectRepository
from app.repositories.task import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    """
    タスク関連のビジネスロジック。

    タスク操作の前にプロジェクトの存在を確認し、
    整合性を保証する。
    """

    def __init__(self, session: AsyncSession) -> None:
        self.repository = TaskRepository(session)
        self.project_repository = ProjectRepository(session)

    async def _ensure_project_exists(self, project_id: uuid.UUID) -> None:
        """
        プロジェクトの存在を確認する（内部ヘルパー）。

        Args:
            project_id: 確認対象のプロジェクトUUID

        Raises:
            HTTPException: プロジェクトが見つからない場合
        """
        project = await self.project_repository.get_by_id(project_id)
        if project is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"プロジェクトが見つかりません: {project_id}",
            )

    async def create_task(
        self, project_id: uuid.UUID, data: TaskCreate
    ) -> Any:
        """
        新しいタスクを作成する。

        事前にプロジェクトの存在を確認する。

        Args:
            project_id: 所属プロジェクトのUUID
            data: 作成リクエストスキーマ

        Returns:
            作成されたタスクインスタンス
        """
        await self._ensure_project_exists(project_id)
        task_data = data.model_dump()
        task_data["project_id"] = project_id
        return await self.repository.create(task_data)

    async def get_task(
        self, project_id: uuid.UUID, task_id: uuid.UUID
    ) -> Any:
        """
        特定のタスクを取得する。

        Args:
            project_id: 所属プロジェクトのUUID
            task_id: 対象タスクのUUID

        Returns:
            タスクインスタンス

        Raises:
            HTTPException: タスクが見つからないか、プロジェクトに属していない場合
        """
        await self._ensure_project_exists(project_id)
        task = await self.repository.get_by_id(task_id)
        if task is None or task.project_id != project_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"タスクが見つかりません: {task_id}",
            )
        return task

    async def get_tasks(
        self,
        project_id: uuid.UUID,
        *,
        page: int = 1,
        per_page: int = 20,
        include_deleted: bool = False,
    ) -> dict[str, Any]:
        """
        プロジェクトに属するタスク一覧をページネーション付きで取得する。

        Args:
            project_id: 対象プロジェクトのUUID
            page: ページ番号
            per_page: 1ページあたりの件数
            include_deleted: 論理削除されたタスクを含めるか

        Returns:
            ページネーションレスポンス辞書
        """
        await self._ensure_project_exists(project_id)
        return await self.repository.get_by_project_id(
            project_id,
            page=page,
            per_page=per_page,
            include_deleted=include_deleted,
        )

    async def update_task(
        self,
        project_id: uuid.UUID,
        task_id: uuid.UUID,
        data: TaskUpdate,
    ) -> Any:
        """
        タスクを部分更新する。

        Args:
            project_id: 所属プロジェクトのUUID
            task_id: 対象タスクのUUID
            data: 更新リクエストスキーマ

        Returns:
            更新されたタスクインスタンス

        Raises:
            HTTPException: タスクが見つからない場合
        """
        # プロジェクト存在確認 & タスクがそのプロジェクトに属しているか確認
        await self.get_task(project_id, task_id)
        update_data = data.model_dump(exclude_unset=True)
        task = await self.repository.update(task_id, update_data)
        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"タスクが見つかりません: {task_id}",
            )
        return task

    async def delete_task(
        self,
        project_id: uuid.UUID,
        task_id: uuid.UUID,
        *,
        soft: bool = True,
    ) -> None:
        """
        タスクを削除する。

        デフォルトでは論理削除（ソフトデリート）。
        soft=False の場合は物理削除。

        Args:
            project_id: 所属プロジェクトのUUID
            task_id: 対象タスクのUUID
            soft: True=論理削除、False=物理削除
        """
        await self.get_task(project_id, task_id)
        if soft:
            result = await self.repository.soft_delete(task_id)
            if result is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"タスクが見つかりません: {task_id}",
                )
        else:
            deleted = await self.repository.delete(task_id)
            if not deleted:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"タスクが見つかりません: {task_id}",
                )
