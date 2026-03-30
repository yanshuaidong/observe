"""
数据库初始化脚本：用于一次性建表。

把 DDL/建表逻辑从后端运行时中隔离出来，避免每次启动后端都触发建表。
"""

from app.db import get_connection

STRATEGY_TABLE_DDL = """
CREATE TABLE IF NOT EXISTS strategy (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  strategyid VARCHAR(64) NOT NULL,
  content JSON NOT NULL,
  UNIQUE KEY uk_strategy_strategyid (strategyid)
);
"""


def create_tables() -> None:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(STRATEGY_TABLE_DDL)
    finally:
        conn.close()


if __name__ == "__main__":
    create_tables()
    print("db_init: tables ensured (strategy).")

