"""
Project CRUD API ルート。

プロジェクトの作成・取得・更新・削除エンドポイントを提供する。
"""

import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_db_session
from app.schemas.common import PaginatedResponse
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate
from app.services.project import ProjectService

router = APIRouter(
    prefix="/projects",
    tags=["プロジェクト"],
)


@router.post(
    "",
    response_model=ProjectRead,
    status_code=status.HTTP_201_CREATED,
    summary="プロジェクト作成",
    description="新しいプロジェクトを作成する",
)
async def create_project(
    data: ProjectCreate,
    db: AsyncSession = Depends(get_db_session),
) -> ProjectRead:
    """プロジェクトを新規作成する"""
    service = ProjectService(db)
    project = await service.create_project(data)
    return ProjectRead.model_validate(project)


@router.get(
    "",
    response_model=PaginatedResponse[ProjectRead],
    summary="プロジェクト一覧取得",
    description="プロジェクト一覧をページネーション付きで取得する",
)
async def get_projects(
    page: int = Query(default=1, ge=1, description="ページ番号"),
    per_page: int = Query(default=20, ge=1, le=100, description="1ページあたりの件数"),
    db: AsyncSession = Depends(get_db_session),
) -> PaginatedResponse[ProjectRead]:
    """プロジェクト一覧を取得する"""
    service = ProjectService(db)
    result = await service.get_projects(page=page, per_page=per_page)
    return PaginatedResponse[ProjectRead](
        items=[ProjectRead.model_validate(p) for p in result["items"]],
        total=result["total"],
        page=result["page"],
        per_page=result["per_page"],
        pages=result["pages"],
    )


@router.get(
    "/{project_id}",
    response_model=ProjectRead,
    summary="プロジェクト取得",
    description="指定されたIDのプロジェクトを取得する",
)
async def get_project(
    project_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
) -> ProjectRead:
    """指定IDのプロジェクトを取得する"""
    service = ProjectService(db)
    project = await service.get_project(project_id)
    return ProjectRead.model_validate(project)


@router.patch(
    "/{project_id}",
    response_model=ProjectRead,
    summary="プロジェクト更新",
    description="指定されたIDのプロジェクトを部分更新する",
)
async def update_project(
    project_id: uuid.UUID,
    data: ProjectUpdate,
    db: AsyncSession = Depends(get_db_session),
) -> ProjectRead:
    """プロジェクトを部分更新する"""
    service = ProjectService(db)
    project = await service.update_project(project_id, data)
    return ProjectRead.model_validate(project)


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="プロジェクト削除",
    description="指定されたIDのプロジェクトを削除する（関連タスクも削除）",
)
async def delete_project(
    project_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
) -> None:
    """プロジェクトとその関連タスクを削除する"""
    service = ProjectService(db)
    await service.delete_project(project_id)
