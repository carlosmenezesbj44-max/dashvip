from __future__ import annotations

from collections import Counter
from typing import Any

from ..config import Settings, get_settings
from ..ixc_client import IXCClient


class DiscoveryService:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.client = IXCClient(self.settings)

    async def inspect_os_table(self, sample_size: int = 100) -> dict[str, Any]:
        page_size = max(10, min(sample_size, 1000))
        records = await self.client.list_table(
            self.settings.ixc_os_table,
            page_size=page_size,
            max_pages=1,
            allow_partial=True,
        )
        records = records[:sample_size]
        keys_counter: Counter[str] = Counter()
        status_counter: Counter[str] = Counter()

        for row in records:
            for key in row.keys():
                keys_counter[key] += 1
            status = _first_present(
                row,
                [
                    self.settings.ixc_os_status_field,
                    "status",
                    "status_os",
                    "situacao",
                ],
            )
            if status:
                status_counter[str(status).strip().upper()] += 1

        available_keys = sorted(keys_counter.keys())
        suggestions = {
            "IXC_OS_ID_FIELD": _suggest_key(
                available_keys,
                [
                    self.settings.ixc_os_id_field,
                    "id",
                    "id_os",
                    "id_chamado",
                    "id_oss",
                ],
            ),
            "IXC_OS_STATUS_FIELD": _suggest_key(
                available_keys,
                [
                    self.settings.ixc_os_status_field,
                    "status",
                    "status_os",
                    "situacao",
                ],
            ),
            "IXC_OS_SUBJECT_ID_FIELD": _suggest_key(
                available_keys,
                [
                    self.settings.ixc_os_subject_id_field,
                    "id_assunto",
                    "assunto_id",
                    "id_tipo_assunto",
                ],
            ),
            "IXC_OS_BRANCH_ID_FIELD": _suggest_key(
                available_keys,
                [
                    self.settings.ixc_os_branch_id_field,
                    "id_filial",
                    "filial_id",
                    "id_empresa",
                ],
            ),
            "IXC_OS_BRANCH_NAME_FIELD": _suggest_key(
                available_keys,
                [
                    self.settings.ixc_os_branch_name_field,
                    "filial",
                    "nome_filial",
                    "empresa",
                ],
            ),
            "IXC_OS_TECH_ID_FIELD": _suggest_key(
                available_keys,
                [
                    self.settings.ixc_os_tech_id_field,
                    "id_tecnico",
                    "id_funcionario",
                    "id_colaborador",
                    "id_usuario_execucao",
                ],
            ),
            "IXC_OS_OPENED_AT_FIELD": _suggest_key(
                available_keys,
                [
                    self.settings.ixc_os_opened_at_field,
                    "data_abertura",
                    "data_criacao",
                    "data_inicio",
                ],
            ),
            "IXC_OS_EXECUTION_AT_FIELD": _suggest_key(
                available_keys,
                [
                    self.settings.ixc_os_execution_at_field,
                    "data_hora_execucao",
                    "data_execucao",
                    "data_inicio_execucao",
                    "data_inicio",
                    "data_atendimento",
                ],
            ),
            "IXC_OS_CLOSED_AT_FIELD": _suggest_key(
                available_keys,
                [
                    self.settings.ixc_os_closed_at_field,
                    "data_fechamento",
                    "data_encerramento",
                    "data_finalizacao",
                ],
            ),
            "IXC_OS_DUE_AT_FIELD": _suggest_key(
                available_keys,
                [
                    self.settings.ixc_os_due_at_field,
                    "data_prazo_limite",
                    "data_previsao_finalizacao",
                    "data_final",
                    "prazo",
                ],
            ),
        }

        return {
            "table": self.settings.ixc_os_table,
            "sample_size": len(records),
            "available_keys": available_keys,
            "field_coverage": dict(keys_counter.most_common()),
            "status_samples": [
                {"status": status, "count": count}
                for status, count in status_counter.most_common(15)
            ],
            "env_suggestions": suggestions,
        }

    async def inspect_lookup_table(
        self,
        *,
        table: str,
        preferred_id_field: str,
        preferred_name_field: str,
        sample_size: int = 50,
    ) -> dict[str, Any]:
        page_size = max(10, min(sample_size, 1000))
        records = await self.client.list_table(
            table,
            page_size=page_size,
            max_pages=1,
        )
        records = records[:sample_size]
        keys_counter: Counter[str] = Counter()
        for row in records:
            for key in row.keys():
                keys_counter[key] += 1

        available_keys = sorted(keys_counter.keys())
        suggested_id = _suggest_key(available_keys, [preferred_id_field, "id"])
        suggested_name = _suggest_key(
            available_keys,
            [preferred_name_field, "nome", "descricao", "assunto", "funcionario", "login"],
        )

        return {
            "table": table,
            "sample_size": len(records),
            "available_keys": available_keys,
            "field_coverage": dict(keys_counter.most_common()),
            "suggested_id_field": suggested_id,
            "suggested_name_field": suggested_name,
        }

    async def test_connection(self) -> dict[str, Any]:
        records = await self.client.list_table(
            self.settings.ixc_os_table,
            page_size=1,
            max_pages=1,
            allow_partial=True,
        )
        sample_keys = sorted(records[0].keys()) if records else []
        return {
            "status": "ok",
            "table": self.settings.ixc_os_table,
            "records_sampled": len(records),
            "sample_keys": sample_keys,
        }


def _suggest_key(available_keys: list[str], candidates: list[str]) -> str | None:
    lowered = {key.lower(): key for key in available_keys}
    for candidate in candidates:
        if candidate.lower() in lowered:
            return lowered[candidate.lower()]
    for candidate in candidates:
        for key in available_keys:
            if candidate.lower() in key.lower():
                return key
    return None


def _first_present(row: dict[str, Any], keys: list[str]) -> Any:
    for key in keys:
        if key in row and row[key] not in (None, ""):
            return row[key]
    return None
