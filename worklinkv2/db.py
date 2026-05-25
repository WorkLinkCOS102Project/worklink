"""
db.py  –  PostgreSQL connection pool and schema bootstrap.

All other modules import `get_conn()` from here.
Never import psycopg2 directly outside this file.
"""

import os
import sys
import psycopg2
from psycopg2 import pool, OperationalError

# ---------------------------------------------------------------------------
# Connection pool (created once at import time)
# ---------------------------------------------------------------------------

_pool: pool.SimpleConnectionPool | None = None


def _build_dsn() -> str:
    """
    Build the DSN from environment variables with sane defaults for local dev.

    Required env vars (or falls back to these defaults):
        WORKLINK_DB_HOST     (default: localhost)
        WORKLINK_DB_PORT     (default: 5432)
        WORKLINK_DB_NAME     (default: worklink)
        WORKLINK_DB_USER     (default: postgres)
        WORKLINK_DB_PASSWORD (default: postgres)
    """
    host = os.environ.get("WORKLINK_DB_HOST", "localhost")
    port = os.environ.get("WORKLINK_DB_PORT", "5432")
    name = os.environ.get("WORKLINK_DB_NAME", "worklink")
    user = os.environ.get("WORKLINK_DB_USER", "postgres")
    pwd  = os.environ.get("WORKLINK_DB_PASSWORD", "COS101")
    return f"host={host} port={port} dbname={name} user={user} password={pwd}"


def init_pool(minconn: int = 1, maxconn: int = 5) -> None:
    """
    Initialise the connection pool.  Called once from main.py on startup.
    Raises SystemExit with a friendly message if the DB is unreachable.
    """
    global _pool
    try:
        _pool = pool.SimpleConnectionPool(minconn, maxconn, dsn=_build_dsn())
    except OperationalError as exc:
        print(
            "\n[WorkLink] ❌  Could not connect to PostgreSQL.\n"
            f"           {exc}\n\n"
            "Make sure PostgreSQL is running and your WORKLINK_DB_* environment\n"
            "variables (or the defaults in db.py) match your local setup.\n",
            file=sys.stderr,
        )
        sys.exit(1)


def get_conn() -> psycopg2.extensions.connection:
    """
    Borrow a connection from the pool.
    Always pair with `release_conn(conn)` in a finally block,
    or use the `db_cursor()` context manager instead.
    """
    if _pool is None:
        raise RuntimeError("Connection pool has not been initialised. Call db.init_pool() first.")
    return _pool.getconn()


def release_conn(conn: psycopg2.extensions.connection) -> None:
    """Return a borrowed connection to the pool."""
    if _pool is not None:
        _pool.putconn(conn)


# ---------------------------------------------------------------------------
# Schema bootstrap
# ---------------------------------------------------------------------------

_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id         SERIAL PRIMARY KEY,
    name       VARCHAR(50)  NOT NULL,
    email      VARCHAR(255) NOT NULL UNIQUE,
    password   VARCHAR(255) NOT NULL,
    role       VARCHAR(20)  NOT NULL CHECK (role IN ('Employer', 'Employee')),
    skills     VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS jobs (
    id          SERIAL PRIMARY KEY,
    employer_id INTEGER      NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title       VARCHAR(60)  NOT NULL,
    description TEXT         NOT NULL,
    skills      VARCHAR(100) NOT NULL,
    experience  VARCHAR(30)  NOT NULL
);

CREATE TABLE IF NOT EXISTS applications (
    id          SERIAL PRIMARY KEY,
    job_id      INTEGER NOT NULL REFERENCES jobs(id)  ON DELETE CASCADE,
    employee_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE (job_id, employee_id)
);
"""


def initialise_schema() -> None:
    """
    Create tables if they don't already exist.
    Safe to call on every startup — uses CREATE TABLE IF NOT EXISTS.
    """
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(_SCHEMA_SQL)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        release_conn(conn)
