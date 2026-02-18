"""
共通ベースモデル（Mixin）モジュール。

全テーブルに共通するカラム（UUID主キー、タイムスタンプ）を提供する。
SQLAlchemy 2.0 の Mapped 型アノテーションを使用。
"""

import uuid
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:
    """
    タイムスタンプ Mixin。

    created_at: レコード作成時に自動設定（UTC）
    updated_at: レコード更新時に自動更新（UTC）
    """

    created_at: Mapped[datetime] = mapped_column(
        # サーバーサイドでデフォルト値を設定（INSERT時）
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        # サーバーサイドでデフォルト値を設定（INSERT時 & UPDATE時）
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class UUIDPrimaryKeyMixin:
    """
    UUID 主キー Mixin。

    全テーブルで UUID v4 を主キーとして使用する。
    データベース側ではなく Python 側で UUID を生成。
    """

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        # PostgreSQL の uuid 型を使用
    )
