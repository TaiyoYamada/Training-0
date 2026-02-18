"""
ヘルスチェック用スキーマ定義。
"""

from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    """
    ヘルスチェックエンドポイントのレスポンススキーマ。

    属性:
        status: アプリケーションの状態（"healthy" / "unhealthy"）
        database: データベース接続の状態（"connected" / "disconnected"）
        version: アプリケーションバージョン
    """

    status: str
    database: str
    version: str
