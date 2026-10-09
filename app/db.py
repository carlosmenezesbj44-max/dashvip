from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from .config import get_settings

DEFAULT_BOARD_TEAM_KEY = "__default__"


def init_db() -> None:
    settings = get_settings()
    db_path = Path(settings.db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS service_orders (
                os_id TEXT PRIMARY KEY,
                status TEXT,
                subject_id TEXT,
                subject_name TEXT,
                branch_id TEXT,
                branch_name TEXT,
                city_id TEXT,
                city_name TEXT,
                customer_id TEXT,
                customer_name TEXT,
                sector_id TEXT,
                sector_name TEXT,
                technician_id TEXT,
                technician_name TEXT,
                opened_at TEXT,
                execution_started_at TEXT,
                closed_at TEXT,
                due_at TEXT,
                raw_payload TEXT,
                updated_at TEXT NOT NULL
            );
            """
        )
        _ensure_column(conn, "service_orders", "branch_id", "TEXT")
        _ensure_column(conn, "service_orders", "branch_name", "TEXT")
        _ensure_column(conn, "service_orders", "city_id", "TEXT")
        _ensure_column(conn, "service_orders", "city_name", "TEXT")
        _ensure_column(conn, "service_orders", "customer_id", "TEXT")
        _ensure_column(conn, "service_orders", "customer_name", "TEXT")
        _ensure_column(conn, "service_orders", "sector_id", "TEXT")
        _ensure_column(conn, "service_orders", "sector_name", "TEXT")
        conn.execute(
            """
            UPDATE service_orders
            SET city_id = NULLIF(json_extract(raw_payload, '$.id_cidade'), '')
            WHERE (city_id IS NULL OR TRIM(city_id) = '')
              AND raw_payload IS NOT NULL
              AND raw_payload <> ''
            """
        )
        conn.execute(
            """
            UPDATE service_orders
            SET sector_id = NULLIF(json_extract(raw_payload, '$.setor'), '')
            WHERE (sector_id IS NULL OR TRIM(sector_id) = '')
              AND raw_payload IS NOT NULL
              AND raw_payload <> ''
            """
        )
        conn.execute(
            """
            UPDATE service_orders
            SET sector_name = NULLIF(json_extract(raw_payload, '$.setor_nome'), '')
            WHERE (sector_name IS NULL OR TRIM(sector_name) = '')
              AND raw_payload IS NOT NULL
              AND raw_payload <> ''
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS sync_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                started_at TEXT NOT NULL,
                finished_at TEXT,
                status TEXT NOT NULL,
                fetched_count INTEGER NOT NULL DEFAULT 0,
                error_message TEXT
            );
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS sync_state (
                state_key TEXT PRIMARY KEY,
                state_value TEXT,
                updated_at TEXT NOT NULL
            );
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS dashboard_filter_presets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                subject_group TEXT,
                branch TEXT,
                sector TEXT,
                subjects TEXT NOT NULL DEFAULT '[]',
                technicians TEXT NOT NULL DEFAULT '[]',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS operations_board_headers (
                entry_date TEXT NOT NULL,
                team_key TEXT NOT NULL,
                responsible_name TEXT,
                shift_label TEXT,
                general_notes TEXT,
                selected_technicians TEXT,
                team_name TEXT,
                updated_at TEXT NOT NULL,
                PRIMARY KEY (entry_date, team_key)
            );
            """
        )
        _ensure_column(conn, "operations_board_headers", "selected_technicians", "TEXT")
        _ensure_column(conn, "operations_board_headers", "team_name", "TEXT")
        _ensure_column(conn, "operations_board_headers", "team_key", "TEXT")
        _migrate_operations_board_headers_if_needed(conn)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS operations_board_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entry_date TEXT NOT NULL,
                team_key TEXT NOT NULL DEFAULT '__default__',
                slot_label TEXT NOT NULL,
                team_label TEXT,
                os_id TEXT,
                subject_name TEXT,
                branch_name TEXT,
                customer_name TEXT,
                technician_names TEXT,
                opening_note TEXT,
                occurrence_note TEXT,
                comment_note TEXT,
                start_at TEXT,
                displacement_at TEXT,
                executed_at TEXT,
                finalized_at TEXT,
                contact_at TEXT,
                status_label TEXT,
                sort_order INTEGER NOT NULL DEFAULT 0,
                updated_at TEXT NOT NULL
            );
            """
        )
        _ensure_column(conn, "operations_board_entries", "comment_note", "TEXT")
        _ensure_column(conn, "operations_board_entries", "customer_name", "TEXT")
        _ensure_column(conn, "operations_board_entries", "team_key", "TEXT")
        _backfill_operations_board_entry_team_keys(conn)
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_service_orders_closed_at ON service_orders (closed_at);"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_service_orders_status ON service_orders (status);"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_service_orders_subject_name ON service_orders (subject_name);"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_service_orders_branch_name ON service_orders (branch_name);"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_service_orders_city_id ON service_orders (city_id);"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_service_orders_city_name ON service_orders (city_name);"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_service_orders_customer_name ON service_orders (customer_name);"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_service_orders_sector_id ON service_orders (sector_id);"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_service_orders_sector_name ON service_orders (sector_name);"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_service_orders_technician_name ON service_orders (technician_name);"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_service_orders_due_at ON service_orders (due_at);"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_sync_runs_started_at ON sync_runs (started_at DESC);"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_dashboard_filter_presets_name ON dashboard_filter_presets (name COLLATE NOCASE);"
        )
        conn.execute("DROP INDEX IF EXISTS idx_operations_board_entries_date;")
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_operations_board_entries_date ON operations_board_entries (entry_date, team_key, sort_order, id);"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_operations_board_headers_date ON operations_board_headers (entry_date, updated_at DESC);"
        )
        conn.commit()


@contextmanager
def db_conn() -> Iterator[sqlite3.Connection]:
    conn = sqlite3.connect(get_settings().db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def _ensure_column(
    conn: sqlite3.Connection,
    table_name: str,
    column_name: str,
    column_type: str,
) -> None:
    rows = conn.execute(f"PRAGMA table_info({table_name});").fetchall()
    existing = {str(row[1]) for row in rows}
    if column_name in existing:
        return
    conn.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type};")


def _migrate_operations_board_headers_if_needed(conn: sqlite3.Connection) -> None:
    rows = conn.execute("PRAGMA table_info(operations_board_headers);").fetchall()
    if not rows:
        return
    pk_columns = [
        str(row[1])
        for row in sorted(rows, key=lambda item: int(item[5]))
        if int(row[5]) > 0
    ]
    if pk_columns == ["entry_date", "team_key"]:
        return
    if pk_columns != ["entry_date"]:
        return

    conn.execute("ALTER TABLE operations_board_headers RENAME TO operations_board_headers_legacy;")
    conn.execute(
        """
        CREATE TABLE operations_board_headers (
            entry_date TEXT NOT NULL,
            team_key TEXT NOT NULL,
            responsible_name TEXT,
            shift_label TEXT,
            general_notes TEXT,
            selected_technicians TEXT,
            team_name TEXT,
            updated_at TEXT NOT NULL,
            PRIMARY KEY (entry_date, team_key)
        );
        """
    )
    conn.execute(
        """
        INSERT INTO operations_board_headers (
            entry_date,
            team_key,
            responsible_name,
            shift_label,
            general_notes,
            selected_technicians,
            team_name,
            updated_at
        )
        SELECT
            entry_date,
            COALESCE(NULLIF(LOWER(TRIM(team_key)), ''), NULLIF(LOWER(TRIM(team_name)), ''), ?),
            responsible_name,
            shift_label,
            general_notes,
            selected_technicians,
            team_name,
            updated_at
        FROM operations_board_headers_legacy
        """,
        (DEFAULT_BOARD_TEAM_KEY,),
    )
    conn.execute("DROP TABLE operations_board_headers_legacy;")


def _backfill_operations_board_entry_team_keys(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        UPDATE operations_board_entries
        SET team_key = COALESCE(
            NULLIF(LOWER(TRIM(team_key)), ''),
            (
                SELECT h.team_key
                FROM operations_board_headers h
                WHERE h.entry_date = operations_board_entries.entry_date
                ORDER BY h.updated_at DESC
                LIMIT 1
            ),
            ?
        )
        WHERE team_key IS NULL OR TRIM(team_key) = ''
        """,
        (DEFAULT_BOARD_TEAM_KEY,),
    )
