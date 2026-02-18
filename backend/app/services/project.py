"""
Project サービス層。

ビジネスロジックをリポジトリ層とAPI層の間に配置する。
リポジトリの呼び出しをラップし、追加のバリデーションや
ビジネスルールを適用する場所。
"""

import uuid
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.project import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectService:
    """
    プロジェクト関連のビジネスロジック。

    リポジトリパターンを通じてDB操作を行い、
    HTTP例外のハンドリングも担当する。
    """

    def __init__(self, session: AsyncSession) -> None:
        self.repository = ProjectRepository(session)

    async def create_project(self, data: ProjectCreate) -> Any:
        """
        新しいプロジェクトを作成する。

        Args:
            data: 作成リクエストスキーマ

        Returns:
            作成されたプロジェクトインスタンス
        """
        return await self.repository.create(data.model_dump())

    async def get_project(self, project_id: uuid.UUID) -> Any:
        """
        IDでプロジェクトを取得する。

        見つからない場合は 404 エラーを返す。

        Args:
            project_id: 対象のUUID

        Returns:
            プロジェクトインスタンス

        Raises:
            HTTPException: プロジェクトが見つからない場合
        """
        project = await self.repository.get_by_id(project_id)
        if project is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"プロジェクトが見つかりません: {project_id}",
            )
        return project

    async def get_projects(
        self,
        *,
        page: int = 1,
        per_page: int = 20,
    ) -> dict[str, Any]:
        """
        プロジェクト一覧をページネーション付きで取得する。

        Args:
            page: ページ番号
            per_page: 1ページあたりの件数

        Returns:
            ページネーションレスポンス辞書
        """
        return await self.repository.get_multi(page=page, per_page=per_page)

    async def update_project(
        self, project_id: uuid.UUID, data: ProjectUpdate
    ) -> Any:
        """
        プロジェクトを部分更新する。

        None でない値のみを更新対象とする（PATCH的な操作）。

        Args:
            project_id: 対象のUUID
            data: 更新リクエストスキーマ

        Returns:
            更新されたプロジェクトインスタンス

        Raises:
            HTTPException: プロジェクトが見つからない場合
        """
        # exclude_unset=True: リクエストに含まれないフィールドは除外
        update_data = data.model_dump(exclude_unset=True)
        project = await self.repository.update(project_id, update_data)
        if project is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"プロジェクトが見つかりません: {project_id}",
            )
        return project

    async def delete_project(self, project_id: uuid.UUID) -> None:
        """
        プロジェクトを削除する。

        関連するタスクも CASCADE で削除される。

        Args:
            project_id: 対象のUUID

        Raises:
            HTTPException: プロジェクトが見つからない場合
        """
        deleted = await self.repository.delete(project_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"プロジェクトが見つかりません: {project_id}",
            )
