from typing import Any, List, Optional

import pymysql
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel, Field

from ..db import get_connection, json_dumps, json_loads_maybe


router = APIRouter(prefix="/api/strategies", tags=["strategies"])


class StrategyCreateRequest(BaseModel):
    strategyid: str = Field(..., min_length=1)
    content: Any


class StrategyResponse(BaseModel):
    strategyid: str
    content: Any


class StrategyListResponse(BaseModel):
    items: List[StrategyResponse]


def _validate_content_jsonable(content: Any) -> None:
    # content comes from request JSON; this is just to guarantee it can be stored.
    try:
        json_dumps(content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"content is not JSON-serializable: {e}")


@router.get("", response_model=StrategyListResponse)
def list_strategies():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT strategyid, content FROM strategy ORDER BY id DESC;")
            rows = cur.fetchall() or []

        items: List[StrategyResponse] = []
        for r in rows:
            items.append(
                StrategyResponse(
                    strategyid=r["strategyid"],
                    content=json_loads_maybe(r.get("content")),
                )
            )
        return StrategyListResponse(items=items)
    finally:
        conn.close()


@router.post("", response_model=StrategyResponse, status_code=201)
def create_strategy(req: StrategyCreateRequest):
    _validate_content_jsonable(req.content)

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            try:
                cur.execute(
                    "INSERT INTO strategy (strategyid, content) VALUES (%s, %s);",
                    (req.strategyid, json_dumps(req.content)),
                )
            except pymysql.err.IntegrityError:
                raise HTTPException(status_code=409, detail="strategyid already exists")

        return StrategyResponse(strategyid=req.strategyid, content=req.content)
    finally:
        conn.close()


@router.get(
    "/{strategyid}",
    response_model=StrategyResponse,
)
def get_strategy(strategyid: str):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT strategyid, content FROM strategy WHERE strategyid=%s;",
                (strategyid,),
            )
            row = cur.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="strategy not found")

        return StrategyResponse(
            strategyid=row["strategyid"],
            content=json_loads_maybe(row.get("content")),
        )
    finally:
        conn.close()


@router.put(
    "/{strategyid}",
    response_model=StrategyResponse,
)
def update_strategy(strategyid: str, req: StrategyCreateRequest):
    _validate_content_jsonable(req.content)

    if req.strategyid != strategyid:
        # 保持契约简单：路径与 body 的 strategyid 必须一致。
        raise HTTPException(status_code=400, detail="strategyid mismatch between path and body")

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE strategy SET content=%s WHERE strategyid=%s;",
                (json_dumps(req.content), strategyid),
            )
            if cur.rowcount == 0:
                raise HTTPException(status_code=404, detail="strategy not found")

        return StrategyResponse(strategyid=strategyid, content=req.content)
    finally:
        conn.close()


@router.delete(
    "/{strategyid}",
    status_code=204,
)
def delete_strategy(strategyid: str):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM strategy WHERE strategyid=%s;",
                (strategyid,),
            )
            if cur.rowcount == 0:
                raise HTTPException(status_code=404, detail="strategy not found")
        return Response(status_code=204)
    finally:
        conn.close()

