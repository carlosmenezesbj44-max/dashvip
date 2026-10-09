from __future__ import annotations

import json
from datetime import datetime
from time import monotonic
from typing import Any

from .db import DEFAULT_BOARD_TEAM_KEY, db_conn


_PRIMARY_EVENT_DATE_SQL = "date(COALESCE(closed_at, execution_started_at, opened_at, updated_at))"
_SCHEDULE_DATE_SQL = """
date(
    COALESCE(
        NULLIF(json_extract(raw_payload, '$.data_agenda'), ''),
        NULLIF(json_extract(raw_payload, '$.data_agendamento'), ''),
        NULLIF(json_extract(raw_payload, '$.data_agenda_inicial'), ''),
        NULLIF(json_extract(raw_payload, '$.data_agenda_final'), ''),
        NULLIF(json_extract(raw_payload, '$.previsao_inicio'), ''),
        NULLIF(json_extract(raw_payload, '$.previsao_fim'), '')
    )
)
"""

_ALL_TECHNICIANS_CACHE_TTL_SECONDS = 300
_all_technicians_cache: tuple[float, list[str]] | None = None
_SECTOR_NAME_OVERRIDES: dict[str, str] = {
    "1": "Tecnico",
    "2": "Financeiro",
    "3": "Tecnico",
    "5": "Financeiro",
    "6": "Tecnico",
    "7": "Comercial",
    "8": "Comercial",
    "9": "Comercial",
    "10": "Tecnico",
    "11": "Tecnico",
    "12": "Tecnico",
    "13": "Tecnico",
    "14": "Financeiro",
    "15": "Tecnico",
}


def upsert_service_orders(rows: list[dict[str, Any]]) -> None:
    if not rows:
        return

    _write_service_orders(rows, replace_existing=False)


def replace_service_orders(rows: list[dict[str, Any]]) -> None:
    _write_service_orders(rows, replace_existing=True)


def update_service_order_city_names(city_lookup: dict[str, str]) -> None:
    if not city_lookup:
        return
    values = [
        (str(city_name or "").strip(), str(city_id or "").strip())
        for city_id, city_name in city_lookup.items()
        if str(city_id or "").strip() and str(city_name or "").strip()
    ]
    if not values:
        return
    with db_conn() as conn:
        conn.executemany(
            """
            UPDATE service_orders
            SET city_name = ?
            WHERE city_id = ?
              AND (city_name IS NULL OR TRIM(city_name) = '')
            """,
            values,
        )
        conn.commit()


def _write_service_orders(rows: list[dict[str, Any]], *, replace_existing: bool) -> None:
    query = """
        INSERT INTO service_orders (
            os_id,
            status,
            subject_id,
            subject_name,
            branch_id,
            branch_name,
            city_id,
            city_name,
            customer_id,
            customer_name,
            sector_id,
            sector_name,
            technician_id,
            technician_name,
            opened_at,
            execution_started_at,
            closed_at,
            due_at,
            raw_payload,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(os_id) DO UPDATE SET
            status=excluded.status,
            subject_id=excluded.subject_id,
            subject_name=excluded.subject_name,
            branch_id=excluded.branch_id,
            branch_name=excluded.branch_name,
            city_id=excluded.city_id,
            city_name=excluded.city_name,
            customer_id=excluded.customer_id,
            customer_name=excluded.customer_name,
            sector_id=excluded.sector_id,
            sector_name=excluded.sector_name,
            technician_id=excluded.technician_id,
            technician_name=excluded.technician_name,
            opened_at=excluded.opened_at,
            execution_started_at=excluded.execution_started_at,
            closed_at=excluded.closed_at,
            due_at=excluded.due_at,
            raw_payload=excluded.raw_payload,
            updated_at=excluded.updated_at;
    """
    values = [
        (
            row["os_id"],
            row.get("status"),
            row.get("subject_id"),
            row.get("subject_name"),
            row.get("branch_id"),
            row.get("branch_name"),
            row.get("city_id"),
            row.get("city_name"),
            row.get("customer_id"),
            row.get("customer_name"),
            row.get("sector_id"),
            row.get("sector_name"),
            row.get("technician_id"),
            row.get("technician_name"),
            row.get("opened_at"),
            row.get("execution_started_at"),
            row.get("closed_at"),
            row.get("due_at"),
            json.dumps(row.get("raw_payload", {}), ensure_ascii=True),
            row["updated_at"],
        )
        for row in rows
    ]

    with db_conn() as conn:
        if replace_existing:
            conn.execute("DELETE FROM service_orders")
        conn.executemany(query, values)
        conn.commit()
    _invalidate_reference_caches()


def _invalidate_reference_caches() -> None:
    global _all_technicians_cache
    _all_technicians_cache = None


def insert_sync_run(
    *,
    started_at: str,
    finished_at: str | None,
    status: str,
    fetched_count: int,
    error_message: str | None,
) -> None:
    with db_conn() as conn:
        conn.execute(
            """
            INSERT INTO sync_runs (started_at, finished_at, status, fetched_count, error_message)
            VALUES (?, ?, ?, ?, ?)
            """,
            (started_at, finished_at, status, fetched_count, error_message),
        )
        conn.commit()


def fetch_latest_sync() -> dict[str, Any] | None:
    with db_conn() as conn:
        row = conn.execute(
            """
            SELECT started_at, finished_at, status, fetched_count, error_message
            FROM sync_runs
            ORDER BY id DESC
            LIMIT 1
            """
        ).fetchone()
    if row is None:
        return None
    return dict(row)


def fetch_closed_orders_by_hour(
    target_date: str,
    *,
    start_date: str | None = None,
    end_date: str | None = None,
    subject_name: str | list[str] | None = None,
    branch_name: str | None = None,
    technician_name: str | None = None,
    status_name: str | None = None,
) -> dict[str, int]:
    where_clause, params = _build_metric_filters(
        start_date=start_date,
        end_date=end_date,
        subject_name=subject_name,
        branch_name=branch_name,
        sector_id=None,
        technician_name=technician_name,
        status_name=status_name,
    )
    params = [target_date] + params
    with db_conn() as conn:
        rows = conn.execute(
            f"""
            SELECT strftime('%H', closed_at) AS hour, COUNT(*) AS total
            FROM service_orders
            WHERE closed_at IS NOT NULL
              AND date(closed_at) = ?
              {where_clause}
            GROUP BY strftime('%H', closed_at)
            """,
            params,
        ).fetchall()

    result: dict[str, int] = {}
    for row in rows:
        hour = row["hour"]
        if hour is None:
            continue
        result[hour] = int(row["total"])
    return result


def fetch_active_orders(
    closed_statuses: list[str],
    *,
    start_date: str | None = None,
    end_date: str | None = None,
    subject_name: str | list[str] | None = None,
    branch_name: str | None = None,
    technician_name: str | None = None,
    status_name: str | None = None,
) -> list[dict[str, Any]]:
    params: list[Any] = []
    placeholders = ", ".join("?" for _ in closed_statuses)
    if placeholders:
        status_clause = (
            f"(status IS NULL OR status = '' OR UPPER(status) NOT IN ({placeholders}))"
        )
        params.extend([status.upper() for status in closed_statuses])
    else:
        status_clause = "1=1"

    where_clause, filter_params = _build_metric_filters(
        start_date=start_date,
        end_date=end_date,
        subject_name=subject_name,
        branch_name=branch_name,
        sector_id=None,
        technician_name=technician_name,
        status_name=status_name,
    )
    params.extend(filter_params)

    query = f"""
        SELECT
            os_id,
            status,
            subject_id,
            subject_name,
                branch_id,
                branch_name,
                sector_id,
                sector_name,
                customer_id,
                customer_name,
            technician_id,
            technician_name,
            opened_at,
            execution_started_at,
            closed_at,
            due_at
        FROM service_orders
        WHERE {status_clause}
          {where_clause}
    """
    with db_conn() as conn:
        rows = conn.execute(query, params).fetchall()
    return [dict(row) for row in rows]


def fetch_orders_for_metrics(
    *,
    start_date: str | None = None,
    end_date: str | None = None,
    subject_name: str | list[str] | None = None,
    branch_name: str | None = None,
    technician_name: str | None = None,
    status_name: str | None = None,
) -> list[dict[str, Any]]:
    where_clause, params = _build_metric_filters(
        start_date=start_date,
        end_date=end_date,
        subject_name=subject_name,
        branch_name=branch_name,
        sector_id=None,
        technician_name=technician_name,
        status_name=status_name,
    )
    query = f"""
        SELECT
            os_id,
            status,
            subject_id,
            subject_name,
            branch_id,
            branch_name,
            customer_id,
            customer_name,
            technician_id,
            technician_name,
            opened_at,
            execution_started_at,
            closed_at,
            due_at
        FROM service_orders
        WHERE 1=1
          {where_clause}
        ORDER BY COALESCE(closed_at, execution_started_at, opened_at, updated_at) DESC
    """
    with db_conn() as conn:
        rows = conn.execute(query, params).fetchall()
    return [dict(row) for row in rows]


def fetch_orders_for_technician_details(
    *,
    start_date: str | None = None,
    end_date: str | None = None,
    subject_name: str | list[str] | None = None,
    branch_name: str | None = None,
    sector_id: str | list[str] | None = None,
    technician_name: str | list[str] | None = None,
    city_id: str | None = None,
    status_name: str | None = None,
    include_raw_payload: bool = True,
) -> list[dict[str, Any]]:
    where_clause, params = _build_metric_filters(
        start_date=start_date,
        end_date=end_date,
        subject_name=subject_name,
        branch_name=branch_name,
        sector_id=sector_id,
        technician_name=technician_name,
        city_id=city_id,
        status_name=status_name,
    )
    raw_payload_select = ",\n            raw_payload" if include_raw_payload else ""
    query = f"""
        SELECT
            os_id,
            status,
            subject_name,
            branch_name,
            sector_id,
            sector_name,
            customer_id,
            customer_name,
            technician_id,
            technician_name,
            opened_at,
            execution_started_at,
            closed_at,
            due_at,
            updated_at{raw_payload_select}
        FROM service_orders
        WHERE 1=1
          {where_clause}
        ORDER BY COALESCE(closed_at, execution_started_at, opened_at, updated_at) DESC
    """
    with db_conn() as conn:
        rows = conn.execute(query, params).fetchall()

    result: list[dict[str, Any]] = []
    for row in rows:
        data = dict(row)
        if include_raw_payload:
            raw_payload = data.get("raw_payload")
            if isinstance(raw_payload, str) and raw_payload.strip():
                try:
                    data["raw_payload"] = json.loads(raw_payload)
                except json.JSONDecodeError:
                    data["raw_payload"] = {}
            else:
                data["raw_payload"] = {}
        else:
            data["raw_payload"] = {}
        result.append(data)
    return result


def fetch_order_by_os_id(os_id: str) -> dict[str, Any] | None:
    order_id = str(os_id or "").strip()
    if not order_id:
        return None
    with db_conn() as conn:
        row = conn.execute(
            """
            SELECT
                os_id,
                status,
                subject_id,
                subject_name,
                branch_id,
                branch_name,
                sector_id,
                sector_name,
                customer_id,
                customer_name,
                technician_id,
                technician_name,
                opened_at,
                execution_started_at,
                closed_at,
                due_at,
                raw_payload,
                updated_at
            FROM service_orders
            WHERE os_id = ?
            LIMIT 1
            """,
            (order_id,),
        ).fetchone()
    if row is None:
        return None
    data = dict(row)
    raw_payload = data.get("raw_payload")
    if isinstance(raw_payload, str) and raw_payload.strip():
        try:
            data["raw_payload"] = json.loads(raw_payload)
        except json.JSONDecodeError:
            data["raw_payload"] = {}
    else:
        data["raw_payload"] = {}
    if not str(data.get("customer_name") or "").strip() and str(data.get("customer_id") or "").strip():
        fallback_customer_name = fetch_customer_name_by_customer_id(str(data.get("customer_id") or ""))
        if fallback_customer_name:
            data["customer_name"] = fallback_customer_name
    return data


def fetch_customer_name_by_customer_id(customer_id: str) -> str | None:
    normalized_id = str(customer_id or "").strip()
    if not normalized_id:
        return None
    with db_conn() as conn:
        row = conn.execute(
            """
            SELECT customer_name
            FROM service_orders
            WHERE customer_id = ?
              AND customer_name IS NOT NULL
              AND TRIM(customer_name) <> ''
            ORDER BY COALESCE(updated_at, closed_at, execution_started_at, opened_at) DESC, os_id DESC
            LIMIT 1
            """,
            (normalized_id,),
        ).fetchone()
    if row is None:
        return None
    return str(row["customer_name"] or "").strip() or None


def fetch_filter_options() -> dict[str, Any]:
    with db_conn() as conn:
        subject_rows = conn.execute(
            """
            SELECT DISTINCT subject_name
            FROM service_orders
            WHERE subject_name IS NOT NULL
              AND TRIM(subject_name) <> ''
            ORDER BY subject_name ASC
            """
        ).fetchall()
        branch_rows = conn.execute(
            """
            SELECT DISTINCT branch_name
            FROM service_orders
            WHERE branch_name IS NOT NULL
              AND TRIM(branch_name) <> ''
            ORDER BY branch_name ASC
            """
        ).fetchall()
        technician_rows = conn.execute(
            """
            SELECT DISTINCT technician_name
            FROM service_orders
            WHERE technician_name IS NOT NULL
              AND TRIM(technician_name) <> ''
            ORDER BY technician_name ASC
            """
        ).fetchall()
        sector_rows = conn.execute(
            """
            SELECT
                sector_id,
                sector_name,
                subject_name,
                COUNT(*) AS total
            FROM service_orders
            WHERE sector_id IS NOT NULL
              AND TRIM(sector_id) <> ''
            GROUP BY sector_id, sector_name, subject_name
            ORDER BY sector_id ASC, total DESC
            """
        ).fetchall()
        status_rows = conn.execute(
            """
            SELECT DISTINCT status
            FROM service_orders
            WHERE status IS NOT NULL
              AND TRIM(status) <> ''
            ORDER BY status ASC
            """
        ).fetchall()
        city_rows = conn.execute(
            """
            SELECT DISTINCT city_id, city_name
            FROM service_orders
            WHERE city_id IS NOT NULL
              AND TRIM(city_id) <> ''
              AND city_id <> '0'
            ORDER BY COALESCE(NULLIF(city_name, ''), city_id) ASC
            """
        ).fetchall()

    sectors = _build_sector_options(sector_rows)

    return {
        "subjects": [str(row["subject_name"]) for row in subject_rows],
        "branches": [str(row["branch_name"]) for row in branch_rows],
        "technicians": [str(row["technician_name"]) for row in technician_rows],
        "sectors": sectors,
        "statuses": [str(row["status"]) for row in status_rows],
        "cities": [
            {
                "id": str(row["city_id"]),
                "name": str(row["city_name"] or ""),
            }
            for row in city_rows
        ],
    }


def list_dashboard_filter_presets() -> list[dict[str, Any]]:
    with db_conn() as conn:
        rows = conn.execute(
            """
            SELECT id, name, subject_group, branch, sector, subjects, technicians, created_at, updated_at
            FROM dashboard_filter_presets
            ORDER BY name COLLATE NOCASE ASC
            """
        ).fetchall()
    return [_parse_dashboard_filter_preset(row) for row in rows]


def create_dashboard_filter_preset(payload: dict[str, Any]) -> dict[str, Any]:
    now = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    name = _clean_preset_text(payload.get("name"))
    if not name:
        raise ValueError("Informe um nome para o filtro salvo.")
    subjects = _normalize_filter_values(payload.get("subjects"))
    technicians = _normalize_filter_values(payload.get("technicians"))
    try:
        with db_conn() as conn:
            cursor = conn.execute(
                """
                INSERT INTO dashboard_filter_presets (
                    name,
                    subject_group,
                    branch,
                    sector,
                    subjects,
                    technicians,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    name,
                    _clean_preset_text(payload.get("subject_group")),
                    _clean_preset_text(payload.get("branch")),
                    _clean_preset_text(payload.get("sector")),
                    json.dumps(subjects, ensure_ascii=True),
                    json.dumps(technicians, ensure_ascii=True),
                    now,
                    now,
                ),
            )
            preset_id = cursor.lastrowid
            conn.commit()
    except Exception as exc:
        if "UNIQUE" in str(exc).upper():
            raise ValueError("Ja existe um filtro salvo com esse nome.") from exc
        raise
    preset = fetch_dashboard_filter_preset(int(preset_id))
    if preset is None:
        raise ValueError("Falha ao salvar filtro.")
    return preset


def update_dashboard_filter_preset(preset_id: int, payload: dict[str, Any]) -> dict[str, Any] | None:
    now = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    name = _clean_preset_text(payload.get("name"))
    if not name:
        raise ValueError("Informe um nome para o filtro salvo.")
    subjects = _normalize_filter_values(payload.get("subjects"))
    technicians = _normalize_filter_values(payload.get("technicians"))
    try:
        with db_conn() as conn:
            result = conn.execute(
                """
                UPDATE dashboard_filter_presets
                SET name = ?,
                    subject_group = ?,
                    branch = ?,
                    sector = ?,
                    subjects = ?,
                    technicians = ?,
                    updated_at = ?
                WHERE id = ?
                """,
                (
                    name,
                    _clean_preset_text(payload.get("subject_group")),
                    _clean_preset_text(payload.get("branch")),
                    _clean_preset_text(payload.get("sector")),
                    json.dumps(subjects, ensure_ascii=True),
                    json.dumps(technicians, ensure_ascii=True),
                    now,
                    preset_id,
                ),
            )
            conn.commit()
    except Exception as exc:
        if "UNIQUE" in str(exc).upper():
            raise ValueError("Ja existe um filtro salvo com esse nome.") from exc
        raise
    if not result.rowcount:
        return None
    return fetch_dashboard_filter_preset(preset_id)


def delete_dashboard_filter_preset(preset_id: int) -> bool:
    with db_conn() as conn:
        result = conn.execute(
            """
            DELETE FROM dashboard_filter_presets
            WHERE id = ?
            """,
            (preset_id,),
        )
        conn.commit()
    return bool(result.rowcount)


def fetch_dashboard_filter_preset(preset_id: int) -> dict[str, Any] | None:
    with db_conn() as conn:
        row = conn.execute(
            """
            SELECT id, name, subject_group, branch, sector, subjects, technicians, created_at, updated_at
            FROM dashboard_filter_presets
            WHERE id = ?
            LIMIT 1
            """,
            (preset_id,),
        ).fetchone()
    if row is None:
        return None
    return _parse_dashboard_filter_preset(row)


def _parse_dashboard_filter_preset(row: Any) -> dict[str, Any]:
    return {
        "id": row["id"],
        "name": row["name"],
        "subject_group": row["subject_group"],
        "branch": row["branch"],
        "sector": row["sector"],
        "subjects": _parse_preset_list(row["subjects"]),
        "technicians": _parse_preset_list(row["technicians"]),
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


def _parse_preset_list(value: Any) -> list[str]:
    if not value:
        return []
    try:
        parsed = json.loads(str(value))
    except json.JSONDecodeError:
        return []
    return _normalize_filter_values(parsed if isinstance(parsed, list) else [])


def _clean_preset_text(value: Any) -> str | None:
    text = str(value or "").strip()
    if not text or text == "__all__":
        return None
    return text


def fetch_operation_board_header(
    entry_date: str,
    *,
    team_name: str | None = None,
    team_key: str | None = None,
) -> dict[str, Any] | None:
    explicit_team_request = team_name is not None or team_key is not None
    normalized_team_key = normalize_operation_board_team_key(team_name, team_key=team_key)
    with db_conn() as conn:
        row = None
        if explicit_team_request:
            row = conn.execute(
                """
                SELECT
                    entry_date,
                    team_key,
                    responsible_name,
                    shift_label,
                    general_notes,
                    selected_technicians,
                    team_name,
                    updated_at
                FROM operations_board_headers
                WHERE entry_date = ?
                  AND team_key = ?
                """,
                (entry_date, normalized_team_key),
            ).fetchone()
        else:
            row = conn.execute(
                """
                SELECT
                    entry_date,
                    team_key,
                    responsible_name,
                    shift_label,
                    general_notes,
                    selected_technicians,
                    team_name,
                    updated_at
                FROM operations_board_headers
                WHERE entry_date = ?
                  AND team_key = ?
                """,
                (entry_date, DEFAULT_BOARD_TEAM_KEY),
            ).fetchone()
    if row is None:
        return None
    return dict(row)


def fetch_operation_board_entries(
    entry_date: str,
    *,
    team_name: str | None = None,
    team_key: str | None = None,
) -> list[dict[str, Any]]:
    explicit_team_request = team_name is not None or team_key is not None
    normalized_team_key = normalize_operation_board_team_key(team_name, team_key=team_key)
    with db_conn() as conn:
        if explicit_team_request:
            rows = _fetch_operation_board_entries_by_key(conn, entry_date, normalized_team_key)
        else:
            rows = _fetch_operation_board_entries_by_key(conn, entry_date, DEFAULT_BOARD_TEAM_KEY)
    return [dict(row) for row in rows]


def upsert_operation_board_header(
    *,
    entry_date: str,
    responsible_name: str | None,
    shift_label: str | None,
    general_notes: str | None,
    selected_technicians: list[str] | None,
    team_name: str | None,
    team_key: str | None = None,
) -> None:
    now = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    normalized_technicians = _normalize_filter_values(selected_technicians)
    cleaned_team_name = _clean_board_team_name(team_name)
    normalized_team_key = normalize_operation_board_team_key(cleaned_team_name, team_key=team_key)
    selected_technicians_json = (
        json.dumps(normalized_technicians, ensure_ascii=True) if normalized_technicians else None
    )
    with db_conn() as conn:
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
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(entry_date, team_key) DO UPDATE SET
                responsible_name = excluded.responsible_name,
                shift_label = excluded.shift_label,
                general_notes = excluded.general_notes,
                selected_technicians = excluded.selected_technicians,
                team_name = excluded.team_name,
                updated_at = excluded.updated_at
            """,
            (
                entry_date,
                normalized_team_key,
                responsible_name,
                shift_label,
                general_notes,
                selected_technicians_json,
                cleaned_team_name,
                now,
            ),
        )
        conn.commit()


def replace_operation_board_entries(
    entry_date: str,
    entries: list[dict[str, Any]],
    *,
    team_name: str | None = None,
    team_key: str | None = None,
) -> None:
    now = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    normalized_team_key = normalize_operation_board_team_key(team_name, team_key=team_key)
    with db_conn() as conn:
        conn.execute(
            """
            DELETE FROM operations_board_entries
            WHERE entry_date = ?
              AND team_key = ?
            """,
            (entry_date, normalized_team_key),
        )
        if entries:
            conn.executemany(
                """
                INSERT INTO operations_board_entries (
                    entry_date,
                    team_key,
                    slot_label,
                    team_label,
                    os_id,
                    subject_name,
                    branch_name,
                    customer_name,
                    technician_names,
                    opening_note,
                    occurrence_note,
                    comment_note,
                    start_at,
                    displacement_at,
                    executed_at,
                    finalized_at,
                    contact_at,
                    status_label,
                    sort_order,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        entry_date,
                        normalized_team_key,
                        entry.get("slot_label"),
                        entry.get("team_label"),
                        entry.get("os_id"),
                        entry.get("subject_name"),
                        entry.get("branch_name"),
                        entry.get("customer_name"),
                        entry.get("technician_names"),
                        entry.get("opening_note"),
                        entry.get("occurrence_note"),
                        entry.get("comment_note"),
                        entry.get("start_at"),
                        entry.get("displacement_at"),
                        entry.get("executed_at"),
                        entry.get("finalized_at"),
                        entry.get("contact_at"),
                        entry.get("status_label"),
                        index,
                        now,
                    )
                    for index, entry in enumerate(entries)
                ],
            )
        conn.commit()


def update_operation_board_entry_comment(
    entry_id: int,
    comment_note: str | None,
) -> dict[str, Any] | None:
    now = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    with db_conn() as conn:
        existing = conn.execute(
            """
            SELECT entry_date, team_key
            FROM operations_board_entries
            WHERE id = ?
            """,
            (entry_id,),
        ).fetchone()
        if existing is None:
            return None

        conn.execute(
            """
            UPDATE operations_board_entries
            SET comment_note = ?,
                updated_at = ?
            WHERE id = ?
            """,
            (comment_note, now, entry_id),
        )
        conn.execute(
            """
            UPDATE operations_board_headers
            SET updated_at = ?
            WHERE entry_date = ?
              AND team_key = ?
            """,
            (now, existing["entry_date"], existing["team_key"]),
        )
        updated = conn.execute(
            """
            SELECT
                id,
                entry_date,
                team_key,
                slot_label,
                team_label,
                os_id,
                subject_name,
                branch_name,
                customer_name,
                technician_names,
                opening_note,
                occurrence_note,
                comment_note,
                start_at,
                displacement_at,
                executed_at,
                finalized_at,
                contact_at,
                status_label,
                sort_order,
                updated_at
            FROM operations_board_entries
            WHERE id = ?
            """,
            (entry_id,),
        ).fetchone()
        conn.commit()
    return dict(updated) if updated is not None else None


def list_operation_board_teams(entry_date: str | None = None) -> list[dict[str, Any]]:
    where_clause = "WHERE h.entry_date = ?" if entry_date else ""
    params: tuple[Any, ...] = (entry_date,) if entry_date else ()
    with db_conn() as conn:
        rows = conn.execute(
            f"""
            SELECT
                h.entry_date,
                h.team_key,
                h.team_name,
                h.responsible_name,
                h.shift_label,
                h.updated_at,
                COALESCE(e.entry_count, 0) AS entry_count
            FROM operations_board_headers h
            LEFT JOIN (
                SELECT entry_date, team_key, COUNT(*) AS entry_count
                FROM operations_board_entries
                GROUP BY entry_date, team_key
            ) e
                ON e.entry_date = h.entry_date
               AND e.team_key = h.team_key
            {where_clause}
            ORDER BY h.entry_date DESC, h.updated_at DESC
            """,
            params,
        ).fetchall()
    return [
        {
            "entry_date": row["entry_date"],
            "team_key": row["team_key"],
            "team_name": _clean_board_team_name(row["team_name"]),
            "responsible_name": row["responsible_name"],
            "shift_label": row["shift_label"],
            "updated_at": row["updated_at"],
            "entry_count": row["entry_count"],
        }
        for row in rows
    ]


def delete_operation_board(
    entry_date: str,
    *,
    team_name: str | None = None,
    team_key: str | None = None,
) -> bool:
    normalized_team_key = normalize_operation_board_team_key(team_name, team_key=team_key)
    with db_conn() as conn:
        entries_result = conn.execute(
            """
            DELETE FROM operations_board_entries
            WHERE entry_date = ?
              AND team_key = ?
            """,
            (entry_date, normalized_team_key),
        )
        headers_result = conn.execute(
            """
            DELETE FROM operations_board_headers
            WHERE entry_date = ?
              AND team_key = ?
            """,
            (entry_date, normalized_team_key),
        )
        conn.commit()
    removed_entries = entries_result.rowcount or 0
    removed_headers = headers_result.rowcount or 0
    return bool(removed_entries or removed_headers)


def normalize_operation_board_team_key(
    team_name: str | None = None,
    *,
    team_key: str | None = None,
) -> str:
    explicit_key = _clean_board_team_name(team_key)
    if explicit_key:
        return explicit_key.lower()
    cleaned_team_name = _clean_board_team_name(team_name)
    if cleaned_team_name:
        return cleaned_team_name.lower()
    return DEFAULT_BOARD_TEAM_KEY


def _fetch_operation_board_entries_by_key(
    conn: Any,
    entry_date: str,
    team_key: str,
) -> list[Any]:
    return conn.execute(
        """
        SELECT
            id,
            entry_date,
            team_key,
            slot_label,
            team_label,
            os_id,
            subject_name,
            branch_name,
            customer_name,
            technician_names,
            opening_note,
            occurrence_note,
            comment_note,
            start_at,
            displacement_at,
            executed_at,
            finalized_at,
            contact_at,
            status_label,
            sort_order,
            updated_at
        FROM operations_board_entries
        WHERE entry_date = ?
          AND team_key = ?
        ORDER BY sort_order ASC, id ASC
        """,
        (entry_date, team_key),
    ).fetchall()


def _clean_board_team_name(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def fetch_operation_board_references(
    entry_date: str,
    *,
    technician_names: list[str] | None = None,
    subject_name: str | list[str] | None = None,
    subject_group_name: str | None = None,
    sector_id: str | list[str] | None = None,
    branch_name: str | None = None,
) -> dict[str, Any]:
    date_match = f"({_PRIMARY_EVENT_DATE_SQL} = ? OR {_SCHEDULE_DATE_SQL} = ?)"
    normalized_technicians = _normalize_filter_values(technician_names)
    normalized_subjects = _normalize_filter_values(subject_name)
    normalized_sectors = _normalize_filter_values(sector_id)
    technician_clause = ""
    technician_params: list[Any] = []
    if normalized_technicians:
        placeholders = ", ".join("?" for _ in normalized_technicians)
        technician_clause = f" AND technician_name IN ({placeholders})"
        technician_params.extend(normalized_technicians)
    subject_clause = ""
    subject_params: list[Any] = []
    if normalized_subjects:
        placeholders = ", ".join("?" for _ in normalized_subjects)
        subject_clause = f" AND subject_name IN ({placeholders})"
        subject_params.extend(normalized_subjects)
    sector_clause = ""
    sector_params: list[Any] = []
    if normalized_sectors:
        placeholders = ", ".join("?" for _ in normalized_sectors)
        sector_clause = f" AND sector_id IN ({placeholders})"
        sector_params.extend(normalized_sectors)
    branch_clause = ""
    branch_params: list[Any] = []
    cleaned_branch_name = str(branch_name or "").strip()
    if cleaned_branch_name and cleaned_branch_name != "__all__":
        branch_clause = " AND branch_name = ?"
        branch_params.append(cleaned_branch_name)

    with db_conn() as conn:
        order_rows = conn.execute(
            """
            SELECT
                os_id,
                status,
                subject_name,
                branch_name,
                sector_id,
                sector_name,
                customer_id,
                customer_name,
                technician_id,
                technician_name,
                opened_at,
                execution_started_at,
                closed_at,
                raw_payload
            FROM service_orders
            WHERE """
            + date_match
            + technician_clause
            + subject_clause
            + sector_clause
            + branch_clause
            + """
            ORDER BY COALESCE(closed_at, execution_started_at, opened_at, updated_at) DESC
            """,
            [entry_date, entry_date, *technician_params, *subject_params, *sector_params, *branch_params],
        ).fetchall()
        all_technicians = _fetch_all_technicians_cached(conn)

    parsed_orders: list[dict[str, Any]] = []
    technicians_set: set[str] = set()
    branches_set: set[str] = set()
    for row in order_rows:
        data = dict(row)
        technician_name = str(data.get("technician_name") or "").strip()
        if technician_name:
            technicians_set.add(technician_name)
        branch_name = str(data.get("branch_name") or "").strip()
        if branch_name:
            branches_set.add(branch_name)
        raw_payload = data.get("raw_payload")
        if isinstance(raw_payload, str) and raw_payload.strip():
            try:
                data["raw_payload"] = json.loads(raw_payload)
            except json.JSONDecodeError:
                data["raw_payload"] = {}
        else:
            data["raw_payload"] = {}
        parsed_orders.append(data)

    if subject_group_name:
        from .config import get_settings
        from .services.metrics_service import _filter_rows_by_subject_group, _resolve_subject_group

        subject_group = _resolve_subject_group(
            get_settings().subject_groups,
            subject_group_name,
            sorted({str(row.get("subject_name") or "") for row in parsed_orders if row.get("subject_name")}),
        )
        parsed_orders = _filter_rows_by_subject_group(parsed_orders, subject_group)

    return {
        "orders": parsed_orders,
        "technicians": sorted(technicians_set),
        "all_technicians": all_technicians,
        "branches": sorted(branches_set),
    }


def _fetch_all_technicians_cached(conn: Any) -> list[str]:
    global _all_technicians_cache
    now = monotonic()
    cached = _all_technicians_cache
    if cached and (now - cached[0]) <= _ALL_TECHNICIANS_CACHE_TTL_SECONDS:
        return list(cached[1])

    rows = conn.execute(
        """
        SELECT DISTINCT technician_name
        FROM service_orders
        WHERE technician_name IS NOT NULL
          AND TRIM(technician_name) <> ''
        ORDER BY technician_name ASC
        """
    ).fetchall()
    values = [str(row["technician_name"]) for row in rows]
    _all_technicians_cache = (now, values)
    return list(values)


def fetch_max_numeric_os_id() -> int | None:
    with db_conn() as conn:
        row = conn.execute(
            """
            SELECT MAX(CAST(os_id AS INTEGER)) AS max_id
            FROM service_orders
            WHERE os_id IS NOT NULL
              AND os_id <> ''
              AND os_id NOT GLOB '*[^0-9]*'
            """
        ).fetchone()
    if row is None:
        return None
    max_id = row["max_id"]
    if max_id is None:
        return None
    try:
        return int(max_id)
    except (TypeError, ValueError):
        return None


def fetch_sync_state(state_key: str) -> str | None:
    with db_conn() as conn:
        row = conn.execute(
            """
            SELECT state_value
            FROM sync_state
            WHERE state_key = ?
            """,
            (state_key,),
        ).fetchone()
    if row is None:
        return None
    return row["state_value"]


def upsert_sync_state(state_key: str, state_value: str) -> None:
    now = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    with db_conn() as conn:
        conn.execute(
            """
            INSERT INTO sync_state (state_key, state_value, updated_at)
            VALUES (?, ?, ?)
            ON CONFLICT(state_key) DO UPDATE SET
                state_value = excluded.state_value,
                updated_at = excluded.updated_at
            """,
            (state_key, state_value, now),
        )
        conn.commit()


def _build_metric_filters(
    *,
    start_date: str | None,
    end_date: str | None,
    subject_name: str | list[str] | None,
    branch_name: str | None,
    sector_id: str | list[str] | None,
    technician_name: str | list[str] | None,
    city_id: str | None = None,
    status_name: str | None = None,
) -> tuple[str, list[Any]]:
    clauses: list[str] = []
    params: list[Any] = []
    if start_date and end_date:
        clauses.append(
            f"(({_PRIMARY_EVENT_DATE_SQL} BETWEEN ? AND ?) OR ({_SCHEDULE_DATE_SQL} BETWEEN ? AND ?))"
        )
        params.extend([start_date, end_date, start_date, end_date])
    elif start_date:
        clauses.append(f"(({_PRIMARY_EVENT_DATE_SQL} >= ?) OR ({_SCHEDULE_DATE_SQL} >= ?))")
        params.extend([start_date, start_date])
    elif end_date:
        clauses.append(f"(({_PRIMARY_EVENT_DATE_SQL} <= ?) OR ({_SCHEDULE_DATE_SQL} <= ?))")
        params.extend([end_date, end_date])
    subject_names = _normalize_filter_values(subject_name)
    if subject_names:
        if len(subject_names) == 1:
            clauses.append("subject_name = ?")
            params.append(subject_names[0])
        else:
            placeholders = ", ".join("?" for _ in subject_names)
            clauses.append(f"subject_name IN ({placeholders})")
            params.extend(subject_names)
    if branch_name:
        clauses.append("branch_name = ?")
        params.append(branch_name)
    sector_ids = _normalize_filter_values(sector_id)
    if sector_ids:
        if len(sector_ids) == 1:
            clauses.append("sector_id = ?")
            params.append(sector_ids[0])
        else:
            placeholders = ", ".join("?" for _ in sector_ids)
            clauses.append(f"sector_id IN ({placeholders})")
            params.extend(sector_ids)
    if city_id:
        clauses.append("city_id = ?")
        params.append(city_id)
    technician_names = _normalize_filter_values(technician_name)
    if technician_names:
        if len(technician_names) == 1:
            clauses.append("technician_name = ?")
            params.append(technician_names[0])
        else:
            placeholders = ", ".join("?" for _ in technician_names)
            clauses.append(f"technician_name IN ({placeholders})")
            params.extend(technician_names)
    if status_name:
        clauses.append("status = ?")
        params.append(status_name)

    if not clauses:
        return "", params
    return " AND " + " AND ".join(clauses), params


def _normalize_filter_values(value: str | list[str] | None) -> list[str]:
    if value is None:
        return []
    raw_values = value if isinstance(value, list) else [value]
    normalized: list[str] = []
    seen: set[str] = set()
    for raw in raw_values:
        for chunk in str(raw or "").split(","):
            text = chunk.strip()
            if not text or text == "__all__":
                continue
            if text in seen:
                continue
            seen.add(text)
            normalized.append(text)
    return normalized


def _build_sector_options(rows: list[Any]) -> list[dict[str, str]]:
    buckets: dict[str, dict[str, Any]] = {}
    for row in rows:
        sector_id = str(row["sector_id"] or "").strip()
        if not sector_id:
            continue
        bucket = buckets.setdefault(
            sector_id,
            {
                "id": sector_id,
                "name": str(row["sector_name"] or "").strip(),
                "subjects": [],
            },
        )
        if not bucket["name"]:
            bucket["name"] = str(row["sector_name"] or "").strip()
        subject_name = str(row["subject_name"] or "").strip()
        if subject_name:
            bucket["subjects"].append(subject_name)

    raw_options: list[dict[str, str]] = []
    for sector_id in sorted(buckets.keys(), key=_sector_sort_key):
        bucket = buckets[sector_id]
        mapped_name = _SECTOR_NAME_OVERRIDES.get(sector_id)
        explicit_name = str(bucket.get("name") or "").strip()
        if mapped_name:
            label = mapped_name
        elif explicit_name and explicit_name != sector_id:
            label = explicit_name
        else:
            inferred_area = _infer_sector_area(bucket.get("subjects") or [])
            if inferred_area:
                label = inferred_area
            else:
                label = f"Setor {sector_id}"
        raw_options.append({"id": sector_id, "name": label})

    grouped_ids_by_name: dict[str, list[str]] = {}
    for option in raw_options:
        group_name = str(option.get("name") or "").strip()
        group_id = str(option.get("id") or "").strip()
        if not group_name or not group_id:
            continue
        grouped_ids_by_name.setdefault(group_name, []).append(group_id)

    options: list[dict[str, str]] = []
    for group_name in sorted(grouped_ids_by_name.keys(), key=lambda value: value.lower()):
        ids = sorted(set(grouped_ids_by_name[group_name]), key=_sector_sort_key)
        options.append({"id": ",".join(ids), "name": group_name})
    return options


def _sector_sort_key(value: str) -> tuple[int, str]:
    text = str(value or "").strip()
    if text.isdigit():
        return (0, f"{int(text):06d}")
    return (1, text.lower())


def _infer_sector_area(subjects: list[str]) -> str | None:
    if not subjects:
        return None
    scored = {"Tecnico": 0, "Financeiro": 0, "Comercial": 0}
    for subject in subjects[:20]:
        normalized = _normalize_search_text(subject)
        if not normalized:
            continue
        if any(
            token in normalized
            for token in (
                "COBRANCA",
                "NEGOCI",
                "FINANCEIR",
                "INADIMPL",
                "FATUR",
                "CANCELAR CONTRATO C",
            )
        ):
            scored["Financeiro"] += 2
        if any(
            token in normalized
            for token in (
                "POS VENDA",
                "RETEN",
                "COMERCIAL",
                "CLIENTE DESIST",
                "ASSINATURA DO CONTRATO",
            )
        ):
            scored["Comercial"] += 2
        if any(
            token in normalized
            for token in (
                "SEM CONEX",
                "LOS",
                "VISITA TECN",
                "INSTALAC",
                "TROCA DE EQUIP",
                "MUDANCA",
                "SUPORTE",
                "AUDITORIA",
                "REDE EXTERNA",
            )
        ):
            scored["Tecnico"] += 2

    best_area = max(scored, key=lambda key: scored[key])
    return best_area if scored[best_area] > 0 else None


def _normalize_search_text(value: str | None) -> str:
    if value is None:
        return ""
    text = str(value).strip().upper()
    if not text:
        return ""
    replacements = str.maketrans(
        {
            "Á": "A",
            "À": "A",
            "Ã": "A",
            "Â": "A",
            "Ä": "A",
            "É": "E",
            "Ê": "E",
            "Ë": "E",
            "Í": "I",
            "Î": "I",
            "Ï": "I",
            "Ó": "O",
            "Ô": "O",
            "Õ": "O",
            "Ö": "O",
            "Ú": "U",
            "Û": "U",
            "Ü": "U",
            "Ç": "C",
        }
    )
    return text.translate(replacements)
