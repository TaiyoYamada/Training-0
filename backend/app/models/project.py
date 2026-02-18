"""
Project モデル定義。

プロジェクト管理の基本エンティティ。
タスクとの1対多リレーションを持つ。
"""

from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin

# 循環インポート防止: 型チェック時のみ Task をインポート
if TYPE_CHECKING:
    from app.models.task import Task


class Project(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """
    プロジェクトテーブル。

    属性:
        id: UUID 主キー
        name: プロジェクト名（必須、最大255文字）
        description: プロジェクト説明（任意）
        tasks: このプロジェクトに属するタスク一覧（リレーション）
    """

    __tablename__ = "projects"

    # --- カラム定義 ---
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,  # 名前での検索を高速化
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        default=None,
    )

    # --- リレーション ---
    # Task との1対多関係。cascade でプロジェクト削除時にタスクも削除
    tasks: Mapped[list["Task"]] = relationship(
        "Task",
        back_populates="project",
        cascade="all, delete-orphan",
        lazy="selectin",  # N+1問題を防ぐためeager loadingを使用
    )

    def __repr__(self) -> str:
        return f"<Project(id={self.id}, name='{self.name}')>"
