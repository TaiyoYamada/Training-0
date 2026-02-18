"""
Task モデル定義。

プロジェクトに紐づくタスクエンティティ。
ステータス管理、優先度、論理削除をサポート。
"""

import enum
import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin
from app.models.project import Project


class TaskStatus(str, enum.Enum):
    """
    タスクのステータスを表す列挙型。

    str を継承することで、JSON シリアライズ時に文字列として扱われる。
    """

    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Task(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """
    タスクテーブル。

    属性:
        id: UUID 主キー
        project_id: 所属プロジェクトのUUID（外部キー）
        title: タスクタイトル（必須）
        description: タスク説明（任意）
        status: タスクステータス（todo / in_progress / done）
        priority: 優先度（数値、デフォルト0）
        due_date: 期限日時（任意）
        is_deleted: 論理削除フラグ（ソフトデリート）
    """

    __tablename__ = "tasks"

    # --- カラム定義 ---
    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,  # プロジェクト別タスク検索を高速化
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        default=None,
    )
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus, name="task_status", native_enum=True),
        nullable=False,
        default=TaskStatus.TODO,
        server_default=TaskStatus.TODO.value,
    )
    priority: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )
    due_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )
    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )

    # --- リレーション ---
    project: Mapped["Project"] = relationship(
        "Project",
        back_populates="tasks",
    )

    def __repr__(self) -> str:
        return f"<Task(id={self.id}, title='{self.title}', status={self.status})>"
