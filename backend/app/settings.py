import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


# Load repo-root .env if it exists (you already have .env / .env.example).
load_dotenv(Path(__file__).resolve().parents[2] / ".env", override=False)


@dataclass(frozen=True)
class Settings:
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str

    cors_allow_origins: list[str]
    auto_create_table: bool


def get_settings() -> Settings:
    cors_raw = os.getenv("CORS_ALLOW_ORIGINS", "*")
    cors_allow_origins = [x.strip() for x in cors_raw.split(",") if x.strip()]

    auto_create_table = os.getenv("AUTO_CREATE_TABLE", "true").lower() in ("1", "true", "yes")

    return Settings(
        db_host=os.getenv("DB_HOST", "127.0.0.1"),
        db_port=int(os.getenv("DB_PORT", "3306")),
        db_user=os.getenv("DB_USER", ""),
        db_password=os.getenv("DB_PASSWORD", ""),
        db_name=os.getenv("DB_NAME", "ysdclaw"),
        cors_allow_origins=cors_allow_origins,
        auto_create_table=auto_create_table,
    )

