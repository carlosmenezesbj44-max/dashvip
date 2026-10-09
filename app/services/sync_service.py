from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, tzinfo
from time import monotonic
from typing import Any, Awaitable, Callable

from ..config import Settings, get_settings, resolve_timezone
from ..ixc_client import IXCClient
from ..repository import (
    fetch_customer_name_by_customer_id,
    fetch_latest_sync,
    fetch_max_numeric_os_id,
    fetch_sync_state,
    insert_sync_run,
    replace_service_orders,
    update_service_order_city_names,
    upsert_service_orders,
    upsert_sync_state,
)

RUNS_SINCE_FULL_STATE_KEY = "runs_since_full_sync"
LAST_UPDATE_CURSOR_STATE_KEY = "last_ixc_update_cursor"
UPDATE_CURSOR_GRACE_MINUTES = 240
UPDATE_SWEEP_PAGE_SIZE = 500
UPDATE_SWEEP_MAX_PAGES = 20
RECENT_CLOSED_SWEEP_DAYS = 7
CLOSED_STATUS_SWEEP_PAGE_SIZE = 500
CLOSED_STATUS_SWEEP_MAX_PAGES_PER_STATUS = 10
MESSAGE_HISTORY_TABLE = "su_oss_chamado_mensagem"
MESSAGE_HISTORY_MAX_ORDERS_PER_SYNC = 500
MESSAGE_HISTORY_CONCURRENCY = 8
LOOKUP_CACHE_TTL_SECONDS = 900


class SyncService:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.client = IXCClient(self.settings)
        self._lock = asyncio.Lock()
        self._tz = resolve_timezone(self.settings.app_timezone)
        self._customer_lookup_cache: dict[str, str] = {}
        self._customer_lookup_loaded = False
        self._lookup_cache: dict[
            tuple[str, str, str],
            tuple[float, dict[str, str]],
        ] = {}

    async def sync_now(
        self,
        *,
        force_full: bool = False,
        progress_callback: Callable[[dict[str, Any]], Awaitable[None]] | None = None,
    ) -> dict[str, Any]:
        async def publish_progress(
            percent: int,
            stage: str,
            message: str,
            **extra: Any,
        ) -> None:
            if progress_callback is None:
                return
            payload = {
                "percent": max(0, min(100, percent)),
                "stage": stage,
                "message": message,
                **extra,
            }
            try:
                await progress_callback(payload)
            except Exception:
                pass

        async with self._lock:
            started_at = _utc_now()
            fetched_count = 0
            mode = "full"
            try:
                await publish_progress(5, "starting", "Iniciando sincronizacao")
                max_known_id = fetch_max_numeric_os_id()
                runs_since_full = _to_int(fetch_sync_state(RUNS_SINCE_FULL_STATE_KEY))
                full_every = max(1, self.settings.ixc_full_sync_every_n_runs)
                should_full = (
                    force_full
                    or not self.settings.ixc_incremental_sync
                    or max_known_id is None
                    or runs_since_full >= full_every
                )
                await publish_progress(
                    15,
                    "mode",
                    "Definindo modo da sincronizacao",
                    sync_mode="full" if should_full else "incremental",
                )

                if should_full:
                    mode = "full"
                    orders = await self.client.list_table(self.settings.ixc_os_table)
                    next_runs_since_full = 0
                else:
                    mode = "incremental"
                    orders_new = await self.client.list_table(
                        self.settings.ixc_os_table,
                        extra_body={
                            "qtype": self.settings.ixc_os_id_field,
                            "query": str(max_known_id),
                            "oper": ">",
                            "sortname": self.settings.ixc_os_id_field,
                            "sortorder": "asc",
                        },
                    )
                    update_cursor = fetch_sync_state(LAST_UPDATE_CURSOR_STATE_KEY)
                    if not update_cursor:
                        latest_sync = fetch_latest_sync()
                        latest_sync_ref = None
                        if latest_sync:
                            latest_sync_ref = latest_sync.get("finished_at") or latest_sync.get(
                                "started_at"
                            )
                        update_cursor = _to_ixc_datetime(latest_sync_ref, self._tz)
                    if not update_cursor:
                        update_cursor = _subtract_minutes(_local_now(self._tz), 120)
                    orders_updated: list[dict[str, Any]] = []
                    if update_cursor:
                        updated_since = _subtract_minutes(
                            update_cursor,
                            UPDATE_CURSOR_GRACE_MINUTES,
                        )
                        try:
                            orders_updated = await self.client.list_table(
                                self.settings.ixc_os_table,
                                page_size=UPDATE_SWEEP_PAGE_SIZE,
                                max_pages=UPDATE_SWEEP_MAX_PAGES,
                                extra_body={
                                    "qtype": "ultima_atualizacao",
                                    "query": updated_since,
                                    "oper": ">=",
                                    "sortname": self.settings.ixc_os_id_field,
                                    "sortorder": "asc",
                                },
                            )
                        except Exception:
                            # If IXC cannot filter by ultima_atualizacao, an incremental
                            # sync cannot be trusted to mirror edited existing OS records.
                            mode = "full"
                            should_full = True
                            orders = await self.client.list_table(self.settings.ixc_os_table)
                            next_runs_since_full = 0
                        else:
                            recent_closed_orders, closed_status_orders = await asyncio.gather(
                                self._fetch_recent_closed_orders(),
                                self._fetch_closed_status_orders(),
                            )
                            orders = _merge_orders_by_os_id(
                                _merge_orders_by_os_id(
                                    _merge_orders_by_os_id(
                                        orders_new,
                                        orders_updated,
                                        self.settings.ixc_os_id_field,
                                    ),
                                    recent_closed_orders,
                                    self.settings.ixc_os_id_field,
                                ),
                                closed_status_orders,
                                self.settings.ixc_os_id_field,
                            )
                            next_runs_since_full = runs_since_full + 1
                    else:
                        recent_closed_orders, closed_status_orders = await asyncio.gather(
                            self._fetch_recent_closed_orders(),
                            self._fetch_closed_status_orders(),
                        )
                        orders = _merge_orders_by_os_id(
                            _merge_orders_by_os_id(
                                _merge_orders_by_os_id(
                                    orders_new,
                                    orders_updated,
                                    self.settings.ixc_os_id_field,
                                ),
                                recent_closed_orders,
                                self.settings.ixc_os_id_field,
                            ),
                            closed_status_orders,
                            self.settings.ixc_os_id_field,
                        )
                        next_runs_since_full = runs_since_full + 1

                await publish_progress(
                    35,
                    "orders_loaded",
                    "OS carregadas do IXC",
                    sync_mode=mode,
                    fetched_count=len(orders),
                )
                normalized_rows: list[dict[str, Any]] = []
                if orders:
                    orders_for_message_history = _filter_orders_for_message_history(
                        orders,
                        self.settings.ixc_os_id_field,
                        self.settings.ixc_os_status_field,
                        self.settings.ixc_os_execution_at_field,
                        self._tz,
                    )
                    message_history_by_os_id = await self._fetch_message_history_for_orders(
                        orders_for_message_history
                    )
                    await publish_progress(
                        50,
                        "messages_loaded",
                        "Historicos de OS carregados",
                        sync_mode=mode,
                        fetched_count=len(orders),
                    )
                    subject_lookup_task = self._build_lookup(
                        table=self.settings.ixc_subject_table,
                        id_field=self.settings.ixc_subject_id_field,
                        name_field=self.settings.ixc_subject_name_field,
                    )
                    tech_lookup_task = self._build_lookup(
                        table=self.settings.ixc_tech_table,
                        id_field=self.settings.ixc_tech_id_field,
                        name_field=self.settings.ixc_tech_name_field,
                    )
                    city_lookup_task = self._build_city_lookup()
                    sector_lookup_task = self._build_sector_lookup()
                    subject_lookup, tech_lookup, city_lookup, sector_lookup = await asyncio.gather(
                        subject_lookup_task,
                        tech_lookup_task,
                        city_lookup_task,
                        sector_lookup_task,
                    )
                    await publish_progress(
                        65,
                        "lookups_loaded",
                        "Tabelas auxiliares carregadas",
                        sync_mode=mode,
                        fetched_count=len(orders),
                    )
                    update_service_order_city_names(city_lookup)
                    customer_lookup: dict[str, str] = {}
                    if any(
                        _extract_customer_id(record)
                        and _extract_customer_name_from_record(record) is None
                        for record in orders
                    ):
                        customer_lookup = await self._get_customer_lookup()
                    customer_name_by_id: dict[str, str] = {}
                    for record in orders:
                        customer_id = _extract_customer_id(record)
                        customer_name = _extract_customer_name_from_record(record)
                        if customer_id and customer_name:
                            customer_name_by_id.setdefault(customer_id, customer_name)

                    now_local = _local_now(self._tz)
                    for record in orders:
                        os_id = _find_value(
                            record,
                            self.settings.ixc_os_id_field,
                            ["id", "id_os", "id_chamado"],
                        )
                        if os_id is None:
                            continue
                        raw_payload = dict(record)
                        messages = message_history_by_os_id.get(str(os_id))
                        if messages:
                            raw_payload["_ixc_messages"] = messages

                        status = _find_value(
                            record,
                            self.settings.ixc_os_status_field,
                            ["status", "status_os"],
                        )
                        normalized_status = _normalize_status(status)
                        subject_id = _find_value(
                            record,
                            self.settings.ixc_os_subject_id_field,
                            ["id_assunto", "assunto_id"],
                        )
                        branch_id = _find_value(
                            record,
                            self.settings.ixc_os_branch_id_field,
                            ["id_filial", "filial_id", "id_empresa"],
                        )
                        branch_name = _find_value(
                            record,
                            self.settings.ixc_os_branch_name_field,
                            ["filial", "nome_filial", "empresa"],
                        )
                        city_id = _find_value(record, "id_cidade", ["cidade_id", "id_municipio"])
                        city_name = None
                        if city_id is not None:
                            city_name = city_lookup.get(city_id)
                        if city_name is None:
                            city_name = _find_value(
                                record,
                                "cidade",
                                ["nome_cidade", "municipio", "nome_municipio"],
                            )
                        tech_id = _find_value(
                            record,
                            self.settings.ixc_os_tech_id_field,
                            ["id_tecnico", "id_funcionario", "id_colaborador"],
                        )

                        subject_name = None
                        if subject_id is not None:
                            subject_name = subject_lookup.get(subject_id)
                        if subject_name is None:
                            subject_name = _find_value(record, "assunto", ["descricao_assunto"])

                        technician_name = None
                        if tech_id is not None:
                            technician_name = tech_lookup.get(tech_id)
                        if technician_name is None:
                            technician_name = _find_value(
                                record, "funcionario", ["tecnico", "executor"]
                            )
                        customer_id = _extract_customer_id(record)
                        customer_name = _extract_customer_name_from_record(record)
                        if customer_name is None and customer_id:
                            customer_name = customer_lookup.get(customer_id)
                        if customer_name is None and customer_id:
                            customer_name = customer_name_by_id.get(customer_id)
                        if customer_name is None and customer_id:
                            customer_name = fetch_customer_name_by_customer_id(customer_id)
                        if customer_name is None and customer_id:
                            customer_name = customer_name_by_id.get(customer_id)
                        if customer_name is not None and customer_id:
                            customer_name_by_id.setdefault(customer_id, customer_name)
                        sector_id = _find_value(
                            record,
                            "setor",
                            ["id_setor", "setor_id", "id_departamento", "departamento_id"],
                        )
                        sector_name = None
                        if sector_id is not None:
                            sector_name = sector_lookup.get(sector_id)
                        if sector_name is None:
                            sector_name = _find_value(
                                record,
                                "setor_nome",
                                [
                                    "nome_setor",
                                    "departamento",
                                    "nome_departamento",
                                ],
                            )

                        normalized_rows.append(
                            {
                                "os_id": os_id,
                                "status": normalized_status,
                                "subject_id": subject_id,
                                "subject_name": subject_name,
                                "branch_id": branch_id,
                                "branch_name": branch_name or branch_id,
                                "city_id": city_id,
                                "city_name": city_name,
                                "customer_id": customer_id,
                                "customer_name": customer_name,
                                "sector_id": sector_id,
                                "sector_name": sector_name,
                                "technician_id": tech_id,
                                "technician_name": technician_name,
                                "opened_at": _find_datetime_value(
                                    record,
                                    self.settings.ixc_os_opened_at_field,
                                    [
                                        "data_abertura",
                                        "data_hora_abertura",
                                        "data_criacao",
                                        "abertura",
                                    ],
                                    self._tz,
                                ),
                                "execution_started_at": (
                                    None
                                    if _is_scheduled_status(normalized_status)
                                    else _find_datetime_value(
                                        record,
                                        self.settings.ixc_os_execution_at_field,
                                        [
                                            "data_hora_execucao",
                                            "data_inicio_execucao",
                                            "inicio_execucao",
                                            "data_inicio",
                                            "data_final",
                                            "data_fechamento",
                                        ],
                                        self._tz,
                                    )
                                ),
                                "closed_at": _find_datetime_value(
                                    record,
                                    self.settings.ixc_os_closed_at_field,
                                    [
                                        "data_fechamento",
                                        "data_encerramento",
                                        "data_finalizacao",
                                        "data_final",
                                        "fechamento",
                                    ],
                                    self._tz,
                                ),
                                "due_at": _find_datetime_value(
                                    record,
                                    self.settings.ixc_os_due_at_field,
                                    [
                                        "data_prazo_limite",
                                        "data_prev_final",
                                        "data_previsao_finalizacao",
                                        "data_agenda_final",
                                        "data_agendamento_final",
                                        "data_agenda",
                                        "data_agendamento",
                                        "data_agenda_inicial",
                                        "data_agendamento_inicial",
                                        "previsao_fim",
                                        "previsao_inicio",
                                        "dt_previsao",
                                        "dt_agendamento",
                                        "data_final",
                                    ],
                                    self._tz,
                                ),
                                "raw_payload": raw_payload,
                                "updated_at": now_local,
                            }
                        )

                fetched_count = len(normalized_rows)
                await publish_progress(
                    80,
                    "normalized",
                    "Registros normalizados",
                    sync_mode=mode,
                    fetched_count=fetched_count,
                )
                await publish_progress(
                    95,
                    "saving",
                    "Gravando dados no banco",
                    sync_mode=mode,
                    fetched_count=fetched_count,
                )
                if should_full:
                    replace_service_orders(normalized_rows)
                else:
                    upsert_service_orders(normalized_rows)
                upsert_sync_state(RUNS_SINCE_FULL_STATE_KEY, str(next_runs_since_full))
                upsert_sync_state(
                    LAST_UPDATE_CURSOR_STATE_KEY,
                    _local_now(self._tz),
                )

                finished_at = _utc_now()
                insert_sync_run(
                    started_at=started_at,
                    finished_at=finished_at,
                    status="success",
                    fetched_count=fetched_count,
                    error_message=None,
                )
                await publish_progress(
                    100,
                    "finished",
                    "Sincronizacao concluida",
                    sync_mode=mode,
                    fetched_count=fetched_count,
                )
                return {
                    "status": "success",
                    "fetched_count": fetched_count,
                    "sync_mode": mode,
                    "max_known_id": max_known_id,
                    "runs_since_full": next_runs_since_full,
                    "started_at": started_at,
                    "finished_at": finished_at,
                }
            except Exception as exc:
                finished_at = _utc_now()
                insert_sync_run(
                    started_at=started_at,
                    finished_at=finished_at,
                    status="error",
                    fetched_count=fetched_count,
                    error_message=str(exc),
                )
                raise

    async def _get_customer_lookup(self) -> dict[str, str]:
        if self._customer_lookup_loaded:
            return self._customer_lookup_cache
        self._customer_lookup_loaded = True
        lookup: dict[str, str] = {}
        candidate_name_fields = ("razao", "nome", "nome_fantasia", "fantasia", "apelido", "descricao")
        for table_name in ("cliente", "clientes"):
            for name_field in candidate_name_fields:
                try:
                    lookup = await self._build_lookup(
                        table=table_name,
                        id_field="id",
                        name_field=name_field,
                    )
                    if lookup:
                        break
                except Exception:
                    continue
            if lookup:
                break
        self._customer_lookup_cache = lookup
        return self._customer_lookup_cache

    async def _fetch_recent_closed_orders(self) -> list[dict[str, Any]]:
        closed_field = self.settings.ixc_os_closed_at_field
        if not closed_field:
            return []
        since = (datetime.now(self._tz) - timedelta(days=RECENT_CLOSED_SWEEP_DAYS)).strftime(
            "%Y-%m-%d"
        )
        return await self.client.list_table(
            self.settings.ixc_os_table,
            page_size=UPDATE_SWEEP_PAGE_SIZE,
            max_pages=UPDATE_SWEEP_MAX_PAGES,
            extra_body={
                "qtype": closed_field,
                "query": since,
                "oper": ">=",
                "sortname": closed_field,
                "sortorder": "desc",
            },
        )

    async def _fetch_closed_status_orders(self) -> list[dict[str, Any]]:
        status_field = self.settings.ixc_os_status_field
        if not status_field:
            return []
        closed_statuses = [
            status.strip().upper()
            for status in self.settings.ixc_status_closed
            if status.strip()
        ]
        if not closed_statuses:
            return []

        batches = await asyncio.gather(
            *(
                self._fetch_orders_by_status(status_field=status_field, status=status)
                for status in closed_statuses
            )
        )
        orders: list[dict[str, Any]] = []
        for batch in batches:
            orders = _merge_orders_by_os_id(
                orders,
                batch,
                self.settings.ixc_os_id_field,
            )
        return orders

    async def _fetch_orders_by_status(
        self,
        *,
        status_field: str,
        status: str,
    ) -> list[dict[str, Any]]:
        try:
            return await self.client.list_table(
                self.settings.ixc_os_table,
                page_size=CLOSED_STATUS_SWEEP_PAGE_SIZE,
                max_pages=CLOSED_STATUS_SWEEP_MAX_PAGES_PER_STATUS,
                allow_partial=True,
                extra_body={
                    "qtype": status_field,
                    "query": status,
                    "oper": "=",
                    "sortname": self.settings.ixc_os_id_field,
                    "sortorder": "desc",
                },
            )
        except Exception:
            return []

    async def _fetch_message_history_for_orders(
        self,
        orders: list[dict[str, Any]],
    ) -> dict[str, list[dict[str, Any]]]:
        order_ids: list[str] = []
        seen: set[str] = set()
        for record in orders:
            os_id = _find_value(
                record,
                self.settings.ixc_os_id_field,
                ["id", "id_os", "id_chamado"],
            )
            if os_id is None or os_id in seen:
                continue
            seen.add(os_id)
            order_ids.append(os_id)

        if not order_ids or len(order_ids) > MESSAGE_HISTORY_MAX_ORDERS_PER_SYNC:
            return {}

        semaphore = asyncio.Semaphore(MESSAGE_HISTORY_CONCURRENCY)

        async def _fetch_one(os_id: str) -> tuple[str, list[dict[str, Any]]]:
            async with semaphore:
                try:
                    records = await self.client.list_table(
                        MESSAGE_HISTORY_TABLE,
                        page_size=100,
                        max_pages=10,
                        extra_body={
                            "qtype": "id_chamado",
                            "query": os_id,
                            "oper": "=",
                            "sortname": "id",
                            "sortorder": "asc",
                        },
                    )
                except Exception:
                    return os_id, []
                return os_id, records

        pairs = await asyncio.gather(*(_fetch_one(os_id) for os_id in order_ids))
        return {os_id: records for os_id, records in pairs if records}

    async def _build_lookup(
        self,
        *,
        table: str,
        id_field: str,
        name_field: str,
    ) -> dict[str, str]:
        table_name = table.strip()
        id_name = id_field.strip()
        value_name = name_field.strip()
        if not table_name:
            return {}
        cache_key = (table_name.lower(), id_name.lower(), value_name.lower())
        cached = self._lookup_cache.get(cache_key)
        now = monotonic()
        if cached and (now - cached[0]) <= LOOKUP_CACHE_TTL_SECONDS:
            return cached[1]
        records = await self.client.list_table(table_name)
        if not records:
            alternate_table = _alternate_lookup_table(table_name)
            if alternate_table:
                records = await self.client.list_table(alternate_table)
        lookup: dict[str, str] = {}
        for item in records:
            row_id = _find_value(item, id_name, ["id"])
            row_name = _find_value(item, value_name, ["nome", "descricao"])
            if row_id is None or row_name is None:
                continue
            lookup[row_id] = row_name
        self._lookup_cache[cache_key] = (now, lookup)
        return lookup

    async def _build_city_lookup(self) -> dict[str, str]:
        candidates = [
            (
                self.settings.ixc_city_table,
                self.settings.ixc_city_id_field,
                self.settings.ixc_city_name_field,
            ),
            ("cidade", "id", "nome"),
            ("cidades", "id", "nome"),
            ("sis_cidade", "id", "nome"),
        ]
        seen: set[tuple[str, str, str]] = set()
        for table, id_field, name_field in candidates:
            key = (table.strip(), id_field.strip(), name_field.strip())
            if not key[0] or key in seen:
                continue
            seen.add(key)
            try:
                lookup = await self._build_lookup(
                    table=key[0],
                    id_field=key[1],
                    name_field=key[2],
                )
            except Exception:
                continue
            if lookup:
                return lookup
        return {}

    async def _build_sector_lookup(self) -> dict[str, str]:
        candidates = [
            ("setor", "id", "setor"),
            ("setor", "id", "nome"),
            ("setor", "id", "descricao"),
            ("setores", "id", "setor"),
            ("setores", "id", "nome"),
            ("setores", "id", "descricao"),
            ("departamento", "id", "nome"),
            ("departamento", "id", "descricao"),
            ("departamentos", "id", "nome"),
            ("departamentos", "id", "descricao"),
        ]
        seen: set[tuple[str, str, str]] = set()
        for table, id_field, name_field in candidates:
            key = (table.strip(), id_field.strip(), name_field.strip())
            if not key[0] or key in seen:
                continue
            seen.add(key)
            try:
                lookup = await self._build_lookup(
                    table=key[0],
                    id_field=key[1],
                    name_field=key[2],
                )
            except Exception:
                continue
            if lookup:
                return lookup
        return {}


def _filter_orders_for_message_history(
    orders: list[dict[str, Any]],
    os_id_field: str,
    status_field: str,
    execution_at_field: str,
    tz: tzinfo,
) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    seen: set[str] = set()
    scheduled_statuses = {"AG", "AGENDA", "AGENDADA", "REAGENDADA", "REAGENDADO", "R", "PENDENTE"}
    execution_statuses = {"F", "FINALIZADA", "FINALIZADO", "EX", "EXECUTADA", "EXECUTADO", "EM_EXECUCAO", "EM_ANDAMENTO"}
    for record in orders:
        os_id = _find_value(record, os_id_field, ["id", "id_os", "id_chamado"])
        if os_id is None or os_id in seen:
            continue
        seen.add(os_id)
        status = _normalize_status(_find_value(record, status_field, ["status", "status_os"]))
        if status in scheduled_statuses:
            candidates.append(record)
            continue

        execution_at = _find_datetime_value(
            record,
            execution_at_field,
            ["data_hora_execucao", "data_inicio_execucao", "inicio_execucao"],
            tz,
        )
        if execution_at is None and status in execution_statuses:
            candidates.append(record)

    if len(candidates) > MESSAGE_HISTORY_MAX_ORDERS_PER_SYNC:
        return candidates[:MESSAGE_HISTORY_MAX_ORDERS_PER_SYNC]
    return candidates


def _find_value(
    record: dict[str, Any], preferred: str, fallback_fields: list[str]
) -> str | None:
    keys = [preferred] + fallback_fields
    for key in keys:
        if key not in record:
            continue
        value = record.get(key)
        if value is None:
            continue
        text = str(value).strip()
        if text and text.lower() != "null":
            return text
    return None


def _find_datetime_value(
    record: dict[str, Any],
    preferred: str,
    fallback_fields: list[str],
    tz: tzinfo,
) -> str | None:
    keys = [preferred, *fallback_fields]
    for key in keys:
        if key not in record:
            continue
        value = record.get(key)
        if value is None:
            continue
        text = str(value).strip()
        if not text or text.lower() == "null":
            continue
        normalized = _normalize_datetime(text, tz)
        if normalized is not None:
            return normalized
    return None


def _normalize_status(value: str | None) -> str | None:
    if value is None:
        return None
    return value.strip().upper()


def _is_scheduled_status(value: str | None) -> bool:
    return _normalize_status(value) in {
        "AG",
        "AGENDA",
        "AGENDADA",
        "REAGENDADA",
        "REAGENDADO",
        "REAGENDAMENTO",
        "R",
        "PENDENTE",
    }


def _extract_customer_id(record: dict[str, Any]) -> str | None:
    return _find_value(
        record,
        "id_cliente",
        ["cliente_id", "id_pessoa", "id_contrato", "id_contrato_kit", "id_login"],
    )


def _extract_customer_name_from_record(record: dict[str, Any]) -> str | None:
    candidates = [
        "cliente",
        "nome_cliente",
        "cliente_nome",
        "razao",
        "razao_social",
        "nome_razao",
        "nome_fantasia",
        "fantasia",
        "apelido",
        "nome",
        "assinante",
    ]
    return _find_value(record, candidates[0], candidates[1:])


def _alternate_lookup_table(table: str) -> str | None:
    aliases = {
        "funcionario": "funcionarios",
        "usuario": "usuarios",
        "colaborador": "colaboradores",
        "tecnico": "tecnicos",
        "setor": "setores",
        "departamento": "departamentos",
    }
    normalized = table.strip().lower()
    if not normalized:
        return None
    return aliases.get(normalized)


def _normalize_datetime(value: str | None, tz: tzinfo) -> str | None:
    if value is None:
        return None

    raw = value.strip()
    if raw in {
        "",
        "0000-00-00",
        "0000-00-00 00:00:00",
        "0000-00-00T00:00:00",
    }:
        return None

    candidates = [
        ("%Y-%m-%d %H:%M:%S", raw),
        ("%Y-%m-%d %H:%M", raw),
        ("%Y-%m-%d", raw),
        ("%Y-%m-%dT%H:%M:%S", raw),
    ]
    for fmt, candidate in candidates:
        try:
            parsed = datetime.strptime(candidate, fmt).replace(tzinfo=tz)
            return parsed.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue

    try:
        iso = datetime.fromisoformat(raw)
    except ValueError:
        return None

    if iso.tzinfo is None:
        iso = iso.replace(tzinfo=tz)
    else:
        iso = iso.astimezone(tz)
    return iso.strftime("%Y-%m-%d %H:%M:%S")


def _utc_now() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _local_now(tz: tzinfo) -> str:
    return datetime.now(tz).replace(microsecond=0).strftime("%Y-%m-%d %H:%M:%S")


def _to_int(value: str | None) -> int:
    try:
        return int(value or "0")
    except (TypeError, ValueError):
        return 0


def _merge_orders_by_os_id(
    primary: list[dict[str, Any]],
    secondary: list[dict[str, Any]],
    preferred_id_field: str,
) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for record in [*primary, *secondary]:
        os_id = _find_value(record, preferred_id_field, ["id", "id_os", "id_chamado"])
        if os_id is None:
            continue
        merged[os_id] = record
    return list(merged.values())


def _subtract_minutes(value: str, minutes: int) -> str:
    raw = str(value or "").strip()
    if not raw:
        return raw
    parsed: datetime | None = None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            parsed = datetime.strptime(raw, fmt)
            break
        except ValueError:
            continue
    if parsed is None:
        try:
            parsed = datetime.fromisoformat(raw.replace("Z", "+00:00")).replace(tzinfo=None)
        except ValueError:
            return raw
    adjusted = parsed - timedelta(minutes=max(0, int(minutes)))
    return adjusted.strftime("%Y-%m-%d %H:%M:%S")


def _to_ixc_datetime(value: str | None, tz: tzinfo) -> str | None:
    raw = str(value or "").strip()
    if not raw:
        return None
    parsed: datetime | None = None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            parsed = datetime.strptime(raw, fmt).replace(tzinfo=tz)
            break
        except ValueError:
            continue
    if parsed is None:
        try:
            parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        except ValueError:
            return None
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=tz)
        else:
            parsed = parsed.astimezone(tz)
    return parsed.strftime("%Y-%m-%d %H:%M:%S")
