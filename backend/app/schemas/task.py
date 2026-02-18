"""
Task 用 Pydantic スキーマ定義。

リクエストバリデーションとレスポンスシリアライゼーションを分離。
TaskStatus enum をスキーマ層でも共有。
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.task import TaskStatus


class TaskCreate(BaseModel):
    """タスク作成リクエストスキーマ"""

    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="タスクタイトル",
        examples=["APIエンドポイントの実装"],
    )
    description: str | None = Field(
        default=None,
        description="タスクの説明",
    )
    status: TaskStatus = Field(
        default=TaskStatus.TODO,
        description="タスクステータス",
    )
    priority: int = Field(
        default=0,
        ge=0,
        description="優先度（数値が大きいほど高優先）",
    )
    due_date: datetime | None = Field(
        default=None,
        description="期限日時（UTC）",
    )


class TaskUpdate(BaseModel):
    """
    タスク更新リクエストスキーマ。

    全フィールドをオプションにして部分更新をサポート。
    """

    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="タスクタイトル",
    )
    description: str | None = Field(
        default=None,
        description="タスクの説明",
    )
    status: TaskStatus | None = Field(
        default=None,
        description="タスクステータス",
    )
    priority: int | None = Field(
        default=None,
        ge=0,
        description="優先度",
    )
    due_date: datetime | None = Field(
        default=None,
        description="期限日時（UTC）",
    )


class TaskRead(BaseModel):
    """タスク読み取りレスポンススキーマ"""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    project_id: uuid.UUID
    title: str
    description: str | None
    status: TaskStatus
    priority: int
    due_date: datetime | None
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
