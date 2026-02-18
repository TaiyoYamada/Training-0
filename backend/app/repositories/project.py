"""
Project リポジトリ。

BaseRepository を継承し、Project モデル固有の
データベース操作を追加する。
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.repositories.base import BaseRepository


class ProjectRepository(BaseRepository[Project]):
    """
    Project モデル用リポジトリ。

    現時点では基底CRUDのみ。
    将来的に名前検索やフィルタリングなどの
    カスタムクエリを追加する場所。
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Project, session)
