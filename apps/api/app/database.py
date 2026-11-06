from contextlib import asynccontextmanager

from fastapi import HTTPException
from psycopg_pool import ConnectionPool

from app.settings import get_settings

_pool: ConnectionPool | None = None


def open_pool() -> None:
    global _pool
    settings = get_settings()
    if settings.database_url and _pool is None:
        _pool = ConnectionPool(
            conninfo=settings.database_url,
            min_size=settings.db_pool_min_size,
            max_size=settings.db_pool_max_size,
            open=True,
            kwargs={'autocommit': False},
        )


def close_pool() -> None:
    global _pool
    if _pool is not None:
        _pool.close()
        _pool = None


def get_pool() -> ConnectionPool:
    if _pool is None:
        raise HTTPException(status_code=503, detail='Database is not configured')
    return _pool


def database_ready() -> bool:
    if _pool is None:
        return False
    try:
        with _pool.connection() as conn:
            conn.execute('SELECT 1')
        return True
    except Exception:
        return False
