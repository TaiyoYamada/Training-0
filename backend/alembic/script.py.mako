"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# リビジョン識別子（Alembic が自動管理）
revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    """マイグレーション: アップグレード（スキーマ変更の適用）"""
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    """マイグレーション: ダウングレード（スキーマ変更のロールバック）"""
    ${downgrades if downgrades else "pass"}
