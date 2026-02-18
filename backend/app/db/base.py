"""
SQLAlchemy DeclarativeBase 定義モジュール。

全モデルの基底クラスとなる Base を定義する。
SQLAlchemy 2.0 スタイルの DeclarativeBase を使用。
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    全モデルの基底クラス。

    SQLAlchemy 2.0 の DeclarativeBase を継承。
    Alembic がマイグレーション生成時にこの Base.metadata を参照する。
    """

    pass
