from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from shutil import copyfile
from typing import Any

from dotenv import set_key

from ..config import Settings, reload_settings


@dataclass(frozen=True)
class EnvField:
    env_name: str
    attr: str
    kind: str  # str | int | bool | list


ENV_FIELDS: list[EnvField] = [
    EnvField("IXC_BASE_URL", "ixc_base_url", "str"),
    EnvField("IXC_TOKEN", "ixc_token", "str"),
    EnvField("IXC_OS_TABLE", "ixc_os_table", "str"),
    EnvField("IXC_OS_ID_FIELD", "ixc_os_id_field", "str"),
    EnvField("IXC_OS_STATUS_FIELD", "ixc_os_status_field", "str"),
    EnvField("IXC_OS_SUBJECT_ID_FIELD", "ixc_os_subject_id_field", "str"),
    EnvField("IXC_OS_BRANCH_ID_FIELD", "ixc_os_branch_id_field", "str"),
    EnvField("IXC_OS_BRANCH_NAME_FIELD", "ixc_os_branch_name_field", "str"),
    EnvField("IXC_OS_TECH_ID_FIELD", "ixc_os_tech_id_field", "str"),
    EnvField("IXC_OS_OPENED_AT_FIELD", "ixc_os_opened_at_field", "str"),
    EnvField("IXC_OS_EXECUTION_AT_FIELD", "ixc_os_execution_at_field", "str"),
    EnvField("IXC_OS_CLOSED_AT_FIELD", "ixc_os_closed_at_field", "str"),
    EnvField("IXC_OS_DUE_AT_FIELD", "ixc_os_due_at_field", "str"),
    EnvField("IXC_SUBJECT_TABLE", "ixc_subject_table", "str"),
    EnvField("IXC_SUBJECT_ID_FIELD", "ixc_subject_id_field", "str"),
    EnvField("IXC_SUBJECT_NAME_FIELD", "ixc_subject_name_field", "str"),
    EnvField("IXC_TECH_TABLE", "ixc_tech_table", "str"),
    EnvField("IXC_TECH_ID_FIELD", "ixc_tech_id_field", "str"),
    EnvField("IXC_TECH_NAME_FIELD", "ixc_tech_name_field", "str"),
    EnvField("IXC_CITY_TABLE", "ixc_city_table", "str"),
    EnvField("IXC_CITY_ID_FIELD", "ixc_city_id_field", "str"),
    EnvField("IXC_CITY_NAME_FIELD", "ixc_city_name_field", "str"),
    EnvField("IXC_STATUS_CLOSED", "ixc_status_closed", "list"),
    EnvField("IXC_STATUS_EXECUTION", "ixc_status_execution", "list"),
    EnvField("IXC_PAGE_SIZE", "ixc_page_size", "int"),
    EnvField("IXC_MAX_PAGES", "ixc_max_pages", "int"),
    EnvField("IXC_INCREMENTAL_SYNC", "ixc_incremental_sync", "bool"),
    EnvField("IXC_FULL_SYNC_EVERY_N_RUNS", "ixc_full_sync_every_n_runs", "int"),
    EnvField("IXC_SYNC_ON_STARTUP", "ixc_sync_on_startup", "bool"),
    EnvField("IXC_AUTO_SYNC", "ixc_auto_sync", "bool"),
    EnvField("IXC_SYNC_INTERVAL_SECONDS", "ixc_sync_interval_seconds", "int"),
    EnvField("IXC_VERIFY_SSL", "ixc_verify_ssl", "bool"),
    EnvField("IXC_HTTP_TIMEOUT_SECONDS", "http_timeout_seconds", "int"),
    EnvField("APP_TIMEZONE", "app_timezone", "str"),
    EnvField("APP_DB_PATH", "db_path", "str"),
    EnvField("APP_DASHBOARD_REFRESH_SECONDS", "app_dashboard_refresh_seconds", "int"),
    EnvField(
        "APP_FILTER_OPTIONS_REFRESH_SECONDS",
        "app_filter_options_refresh_seconds",
        "int",
    ),
    EnvField("APP_SUBJECT_GROUPS", "app_subject_groups_raw", "str"),
    EnvField("APP_ADMIN_PASSWORD", "app_admin_password", "str"),
]


SENSITIVE_ENV_FIELDS = {"IXC_TOKEN", "APP_ADMIN_PASSWORD"}
MASKED_SECRET_VALUE = "********"


class SettingsService:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or reload_settings()
        self._env_path = Path(".env")
        self._example_path = Path(".env.example")

    def current_values(self) -> dict[str, Any]:
        values: dict[str, Any] = {}
        for field in ENV_FIELDS:
            raw = getattr(self.settings, field.attr)
            if field.env_name in SENSITIVE_ENV_FIELDS:
                values[field.env_name] = MASKED_SECRET_VALUE if str(raw or "").strip() else ""
            elif field.kind == "list":
                values[field.env_name] = ",".join(raw)
            else:
                values[field.env_name] = raw
        return values

    def update(self, incoming: dict[str, Any]) -> Settings:
        self._ensure_env_file()

        supported = {field.env_name: field for field in ENV_FIELDS}
        unknown = [key for key in incoming.keys() if key not in supported]
        if unknown:
            raise ValueError(f"Campos nao suportados: {', '.join(unknown)}")

        for env_name, raw in incoming.items():
            field = supported[env_name]
            if env_name in SENSITIVE_ENV_FIELDS and str(raw or "").strip() in {"", MASKED_SECRET_VALUE}:
                continue
            normalized = _normalize_value(raw, field.kind)
            set_key(
                str(self._env_path),
                env_name,
                normalized,
                quote_mode="auto",
            )

        new_settings = reload_settings()
        self.settings = new_settings
        return new_settings

    def _ensure_env_file(self) -> None:
        if self._env_path.exists():
            return
        if self._example_path.exists():
            copyfile(self._example_path, self._env_path)
            return
        self._env_path.write_text("", encoding="utf-8")


def _normalize_value(value: Any, kind: str) -> str:
    if kind == "bool":
        if isinstance(value, bool):
            return "true" if value else "false"
        text = str(value).strip().lower()
        return "true" if text in {"1", "true", "yes", "on", "sim"} else "false"

    if kind == "int":
        try:
            return str(int(value))
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Valor invalido para inteiro: {value}") from exc

    if kind == "list":
        if isinstance(value, list):
            chunks = [str(chunk).strip() for chunk in value if str(chunk).strip()]
            return ",".join(chunks)
        chunks = [chunk.strip() for chunk in str(value).split(",")]
        return ",".join([chunk for chunk in chunks if chunk])

    return str(value).strip()
