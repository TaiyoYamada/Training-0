"""
Task CRUD API ルート。

プロジェクトに紐づくタスクの作成・取得・更新・削除エンドポイントを提供する。
URL はネスト構造: /api/v1/projects/{project_id}/tasks
"""

import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_db_session
from app.schemas.common import PaginatedResponse
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.services.task import TaskService

router = APIRouter(
    prefix="/projects/{project_id}/tasks",
    tags=["タスク"],
)


@router.post(
    "",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
    summary="タスク作成",
    description="指定プロジェクトに新しいタスクを作成する",
)
async def create_task(
    project_id: uuid.UUID,
    data: TaskCreate,
    db: AsyncSession = Depends(get_db_session),
) -> TaskRead:
    """新しいタスクを作成する"""
    service = TaskService(db)
    task = await service.create_task(project_id, data)
    return TaskRead.model_validate(task)


@router.get(
    "",
    response_model=PaginatedResponse[TaskRead],
    summary="タスク一覧取得",
    description="指定プロジェクトのタスク一覧をページネーション付きで取得する",
)
async def get_tasks(
    project_id: uuid.UUID,
    page: int = Query(default=1, ge=1, description="ページ番号"),
    per_page: int = Query(default=20, ge=1, le=100, description="1ページあたりの件数"),
    include_deleted: bool = Query(default=False, description="削除済みタスクを含める"),
    db: AsyncSession = Depends(get_db_session),
) -> PaginatedResponse[TaskRead]:
    """プロジェクトのタスク一覧を取得する"""
    service = TaskService(db)
    result = await service.get_tasks(
        project_id,
        page=page,
        per_page=per_page,
        include_deleted=include_deleted,
    )
    return PaginatedResponse[TaskRead](
        items=[TaskRead.model_validate(t) for t in result["items"]],
        total=result["total"],
        page=result["page"],
        per_page=result["per_page"],
        pages=result["pages"],
    )


@router.get(
    "/{task_id}",
    response_model=TaskRead,
    summary="タスク取得",
    description="指定されたIDのタスクを取得する",
)
async def get_task(
    project_id: uuid.UUID,
    task_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
) -> TaskRead:
    """指定IDのタスクを取得する"""
    service = TaskService(db)
    task = await service.get_task(project_id, task_id)
    return TaskRead.model_validate(task)


@router.patch(
    "/{task_id}",
    response_model=TaskRead,
    summary="タスク更新",
    description="指定されたIDのタスクを部分更新する",
)
async def update_task(
    project_id: uuid.UUID,
    task_id: uuid.UUID,
    data: TaskUpdate,
    db: AsyncSession = Depends(get_db_session),
) -> TaskRead:
    """タスクを部分更新する"""
    service = TaskService(db)
    task = await service.update_task(project_id, task_id, data)
    return TaskRead.model_validate(task)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="タスク削除",
    description="指定されたIDのタスクを論理削除する",
)
async def delete_task(
    project_id: uuid.UUID,
    task_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
) -> None:
    """タスクを論理削除する（ソフトデリート）"""
    service = TaskService(db)
    await service.delete_task(project_id, task_id, soft=True)
