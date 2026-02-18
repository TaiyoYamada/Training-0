"""
アプリケーション設定モジュール。

pydantic-settings を使用して環境変数からアプリケーション設定を読み込む。
.env ファイルからの自動読み込みにも対応。
環境モード (dev / staging / prod) に応じた設定切り替えをサポート。
"""

import logging
from enum import Enum
from typing import Literal

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    """実行環境を表す列挙型"""

    DEV = "dev"
    STAGING = "staging"
    PROD = "prod"


class Settings(BaseSettings):
    """
    アプリケーション全体の設定クラス。

    環境変数または .env ファイルから設定値を読み込む。
    DATABASE_URL は個別のDB接続パラメータから自動生成される。
    """

    # --- モデル設定 ---
    model_config = SettingsConfigDict(
        env_file=".env",          # .env ファイルから読み込み
        env_file_encoding="utf-8",
        case_sensitive=False,      # 環境変数名の大文字小文字を区別しない
        extra="ignore",            # 未定義の環境変数は無視
    )

    # --- アプリケーション基本設定 ---
    APP_NAME: str = "Training-0"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    # --- 環境モード（dev / staging / prod） ---
    ENVIRONMENT: Environment = Environment.DEV

    # --- ロギング設定 ---
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: Literal["json", "text"] = "text"

    # --- PostgreSQL 接続設定 ---
    POSTGRES_USER: str = "training0"
    POSTGRES_PASSWORD: str = "training0_password"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "training0_db"

    # --- サーバー設定 ---
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000

    # --- CORS 設定 ---
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173,http://localhost:8080"

    # --- 将来的なJWT設定（コメントアウト状態で予約） ---
    # JWT_SECRET_KEY: str = ""
    # JWT_ALGORITHM: str = "HS256"
    # JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @computed_field  # type: ignore[prop-decorator]
    @property
    def DATABASE_URL(self) -> str:
        """PostgreSQL の非同期接続URLを自動生成（asyncpg ドライバ）"""
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def DATABASE_URL_SYNC(self) -> str:
        """Alembic マイグレーション用の接続URL"""
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def cors_origins_list(self) -> list[str]:
        """CORS_ORIGINS をカンマ区切りでリストに変換"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    @property
    def is_production(self) -> bool:
        """本番環境かどうかを判定"""
        return self.ENVIRONMENT == Environment.PROD

    @property
    def log_level_int(self) -> int:
        """ログレベルを logging モジュールの定数に変換"""
        return getattr(logging, self.LOG_LEVEL.upper(), logging.INFO)


# シングルトンインスタンス（アプリケーション全体で共有）
settings = Settings()
