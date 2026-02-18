"""
共通スキーマ定義モジュール。

ページネーションなど、複数のエンドポイントで共通して使用する
レスポンススキーマを定義する。
"""

from typing import Generic, TypeVar

from pydantic import BaseModel, Field

# ジェネリック型パラメータ（ページネーションレスポンス用）
T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """
    ページネーション付きレスポンススキーマ。

    全てのリスト取得エンドポイントで使用する共通形式。

    属性:
        items: 現在のページのデータ一覧
        total: 全件数
        page: 現在のページ番号（1始まり）
        per_page: 1ページあたりの件数
        pages: 総ページ数
    """

    items: list[T]
    total: int = Field(ge=0, description="全件数")
    page: int = Field(ge=1, description="現在のページ番号")
    per_page: int = Field(ge=1, le=100, description="1ページあたりの件数")
    pages: int = Field(ge=0, description="総ページ数")
