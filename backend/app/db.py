import json
from typing import Any

import pymysql
from pymysql.cursors import DictCursor

from .settings import get_settings


def get_connection():
    s = get_settings()
    return pymysql.connect(
        host=s.db_host,
        port=s.db_port,
        user=s.db_user,
        password=s.db_password,
        database=s.db_name,
        cursorclass=DictCursor,
        autocommit=True,
        charset="utf8mb4",
    )


def json_dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def json_loads_maybe(raw: Any) -> Any:
    if raw is None:
        return None
    if isinstance(raw, (dict, list, int, float, bool)):
        return raw
    if isinstance(raw, str):
        return json.loads(raw)
    # Fallback: best-effort
    return json.loads(str(raw))

