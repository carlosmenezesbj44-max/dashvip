from __future__ import annotations

import base64
import os
import re
from datetime import timezone, tzinfo
from dataclasses import dataclass
from functools import lru_cache
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from dotenv import load_dotenv

load_dotenv()


DEFAULT_SUBJECT_GROUPS_RAW = ""


def _env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on", "sim"}


def _env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def _env_list(name: str, default: list[str]) -> list[str]:
    raw = os.getenv(name)
    if raw is None:
        return default
    values = [chunk.strip() for chunk in raw.split(",")]
    return [value for value in values if value]


@dataclass(frozen=True)
class SubjectGroup:
    key: str
    label: str
    patterns: tuple[str, ...]


@dataclass(frozen=True)
class Settings:
    ixc_base_url: str
    ixc_token: str
    ixc_os_table: str
    ixc_os_id_field: str
    ixc_os_status_field: str
    ixc_os_subject_id_field: str
    ixc_os_branch_id_field: str
    ixc_os_branch_name_field: str
    ixc_os_tech_id_field: str
    ixc_os_opened_at_field: str
    ixc_os_execution_at_field: str
    ixc_os_closed_at_field: str
    ixc_os_due_at_field: str
    ixc_subject_table: str
    ixc_subject_id_field: str
    ixc_subject_name_field: str
    ixc_tech_table: str
    ixc_tech_id_field: str
    ixc_tech_name_field: str
    ixc_city_table: str
    ixc_city_id_field: str
    ixc_city_name_field: str
    ixc_status_closed: list[str]
    ixc_status_execution: list[str]
    ixc_page_size: int
    ixc_max_pages: int
    ixc_incremental_sync: bool
    ixc_full_sync_every_n_runs: int
    ixc_sync_on_startup: bool
    ixc_auto_sync: bool
    ixc_sync_interval_seconds: int
    ixc_verify_ssl: bool
    http_timeout_seconds: int
    app_timezone: str
    db_path: str
    app_dashboard_refresh_seconds: int
    app_filter_options_refresh_seconds: int
    app_subject_groups_raw: str
    app_admin_password: str

    @property
    def authorization_token(self) -> str:
        raw = self.ixc_token.strip()
        lowered = raw.lower()
        if lowered.startswith("basic ") or lowered.startswith("bearer ") or lowered.startswith(
            "token "
        ):
            return raw
        if ":" in raw and " " not in raw:
            encoded = base64.b64encode(raw.encode("utf-8")).decode("ascii")
            return f"Basic {encoded}"
        return f"Basic {raw}"

    @property
    def api_root(self) -> str:
        return f"{self.ixc_base_url}/webservice/v1"

    @property
    def closed_status_set(self) -> set[str]:
        return {value.upper() for value in self.ixc_status_closed}

    @property
    def execution_status_set(self) -> set[str]:
        return {value.upper() for value in self.ixc_status_execution}

    @property
    def subject_groups(self) -> list[SubjectGroup]:
        return _parse_subject_groups(self.app_subject_groups_raw)


def _normalize_base_url(value: str) -> str:
    cleaned = value.strip().strip("'\"").rstrip("/")
    lowered = cleaned.lower()

    if cleaned and not re.match(r"^https?://", lowered):
        cleaned = f"https://{cleaned}"
        lowered = cleaned.lower()

    api_idx = lowered.find("/webservice/v1")
    if api_idx >= 0:
        cleaned = cleaned[:api_idx].rstrip("/")
        lowered = cleaned.lower()

    known_suffixes = [
        "/adm.php",
        "/adm",
        "/central_assinante_web",
        "/central_assinante",
    ]
    for suffix in known_suffixes:
        if lowered.endswith(suffix):
            cleaned = cleaned[: -len(suffix)].rstrip("/")
            lowered = cleaned.lower()
    return cleaned


@lru_cache
def get_settings() -> Settings:
    load_dotenv(override=True)
    base_url = _normalize_base_url(
        os.getenv("IXC_BASE_URL", "https://seu-servidor-ixc.com.br")
    )
    return Settings(
        ixc_base_url=base_url,
        ixc_token=os.getenv("IXC_TOKEN", ""),
        ixc_os_table=os.getenv("IXC_OS_TABLE", "su_oss_chamado"),
        ixc_os_id_field=os.getenv("IXC_OS_ID_FIELD", "id"),
        ixc_os_status_field=os.getenv("IXC_OS_STATUS_FIELD", "status"),
        ixc_os_subject_id_field=os.getenv("IXC_OS_SUBJECT_ID_FIELD", "id_assunto"),
        ixc_os_branch_id_field=os.getenv("IXC_OS_BRANCH_ID_FIELD", "id_filial"),
        ixc_os_branch_name_field=os.getenv("IXC_OS_BRANCH_NAME_FIELD", "filial"),
        ixc_os_tech_id_field=os.getenv("IXC_OS_TECH_ID_FIELD", "id_tecnico"),
        ixc_os_opened_at_field=os.getenv("IXC_OS_OPENED_AT_FIELD", "data_abertura"),
        ixc_os_execution_at_field=os.getenv(
            "IXC_OS_EXECUTION_AT_FIELD", "data_hora_execucao"
        ),
        ixc_os_closed_at_field=os.getenv("IXC_OS_CLOSED_AT_FIELD", "data_fechamento"),
        ixc_os_due_at_field=os.getenv("IXC_OS_DUE_AT_FIELD", "data_prazo_limite"),
        ixc_subject_table=os.getenv("IXC_SUBJECT_TABLE", "su_oss_assunto"),
        ixc_subject_id_field=os.getenv("IXC_SUBJECT_ID_FIELD", "id"),
        ixc_subject_name_field=os.getenv("IXC_SUBJECT_NAME_FIELD", "assunto"),
        ixc_tech_table=os.getenv("IXC_TECH_TABLE", "funcionarios"),
        ixc_tech_id_field=os.getenv("IXC_TECH_ID_FIELD", "id"),
        ixc_tech_name_field=os.getenv("IXC_TECH_NAME_FIELD", "funcionario"),
        ixc_city_table=os.getenv("IXC_CITY_TABLE", "cidade"),
        ixc_city_id_field=os.getenv("IXC_CITY_ID_FIELD", "id"),
        ixc_city_name_field=os.getenv("IXC_CITY_NAME_FIELD", "nome"),
        ixc_status_closed=_env_list(
            "IXC_STATUS_CLOSED", ["F", "FINALIZADA", "CONCLUIDA"]
        ),
        ixc_status_execution=_env_list(
            "IXC_STATUS_EXECUTION", ["E", "EN", "EX", "EM_EXECUCAO", "EM_ANDAMENTO"]
        ),
        ixc_page_size=_env_int("IXC_PAGE_SIZE", 1000),
        ixc_max_pages=_env_int("IXC_MAX_PAGES", 500),
        ixc_incremental_sync=_env_bool("IXC_INCREMENTAL_SYNC", True),
        ixc_full_sync_every_n_runs=max(1, _env_int("IXC_FULL_SYNC_EVERY_N_RUNS", 12)),
        ixc_sync_on_startup=_env_bool("IXC_SYNC_ON_STARTUP", True),
        ixc_auto_sync=_env_bool("IXC_AUTO_SYNC", True),
        ixc_sync_interval_seconds=_env_int("IXC_SYNC_INTERVAL_SECONDS", 300),
        ixc_verify_ssl=_env_bool("IXC_VERIFY_SSL", True),
        http_timeout_seconds=_env_int("IXC_HTTP_TIMEOUT_SECONDS", 60),
        app_timezone=os.getenv("APP_TIMEZONE", "America/Sao_Paulo"),
        db_path=os.getenv("APP_DB_PATH", "./data/dashboard.db"),
        app_dashboard_refresh_seconds=max(5, _env_int("APP_DASHBOARD_REFRESH_SECONDS", 30)),
        app_filter_options_refresh_seconds=max(
            15, _env_int("APP_FILTER_OPTIONS_REFRESH_SECONDS", 180)
        ),
        app_subject_groups_raw=os.getenv("APP_SUBJECT_GROUPS", DEFAULT_SUBJECT_GROUPS_RAW),
        app_admin_password=os.getenv("APP_ADMIN_PASSWORD", ""),
    )


def reload_settings() -> Settings:
    load_dotenv(override=True)
    get_settings.cache_clear()
    return get_settings()


def resolve_timezone(name: str) -> tzinfo:
    try:
        return ZoneInfo(name)
    except ZoneInfoNotFoundError:
        try:
            return ZoneInfo("UTC")
        except ZoneInfoNotFoundError:
            return timezone.utc


def _parse_subject_groups(raw_value: str | None) -> list[SubjectGroup]:
    raw = str(raw_value or "").strip()
    if not raw:
        return []

    grouped_patterns: dict[str, list[str]] = {}
    labels: dict[str, str] = {}

    for chunk in raw.split(";"):
        item = chunk.strip()
        if not item:
            continue
        label_part, separator, patterns_part = item.partition("=")
        label = label_part.strip()
        if not label:
            continue

        key = _normalize_subject_group_key(label)
        if not key:
            continue

        labels.setdefault(key, label)
        grouped_patterns.setdefault(key, [])
        if not separator:
            continue

        for pattern in re.split(r"[|,]", patterns_part):
            text = pattern.strip()
            if text and text not in grouped_patterns[key]:
                grouped_patterns[key].append(text)

    result: list[SubjectGroup] = []
    for key, patterns in grouped_patterns.items():
        if not patterns:
            continue
        result.append(
            SubjectGroup(
                key=key,
                label=labels.get(key, key.title()),
                patterns=tuple(patterns),
            )
        )
    return result


def _normalize_subject_group_key(value: str) -> str:
    lowered = value.strip().lower()
    lowered = re.sub(r"\s+", "_", lowered)
    lowered = re.sub(r"[^a-z0-9_]+", "", lowered)
    return lowered.strip("_")
