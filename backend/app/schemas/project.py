"""
Project 用 Pydantic スキーマ定義。

リクエストバリデーション（Create / Update）と
レスポンスシリアライゼーション（Read）を分離。
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProjectCreate(BaseModel):
    """プロジェクト作成リクエストスキーマ"""

    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="プロジェクト名",
        examples=["マイプロジェクト"],
    )
    description: str | None = Field(
        default=None,
        description="プロジェクトの説明",
        examples=["これはサンプルプロジェクトです"],
    )


class ProjectUpdate(BaseModel):
    """
    プロジェクト更新リクエストスキーマ。

    全フィールドをオプションにすることで、
    部分更新（PATCH的な操作）をサポート。
    """

    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="プロジェクト名",
    )
    description: str | None = Field(
        default=None,
        description="プロジェクトの説明",
    )


class ProjectRead(BaseModel):
    """
    プロジェクト読み取りレスポンススキーマ。

    model_config の from_attributes=True により、
    SQLAlchemy モデルのインスタンスから直接変換が可能。
    """

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime
