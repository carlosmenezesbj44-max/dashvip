from __future__ import annotations

from typing import Any

import httpx

from .config import Settings, get_settings


SERVER_PUBLIC_IP = "45.186.99.204"


class IXCClient:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

    async def list_table(
        self,
        table: str,
        *,
        page_size: int | None = None,
        max_pages: int | None = None,
        extra_body: dict[str, Any] | None = None,
        allow_partial: bool = False,
    ) -> list[dict[str, Any]]:
        if not self.settings.ixc_token.strip():
            raise RuntimeError(
                "IXC_TOKEN nao definido. Configure o token no arquivo .env."
            )

        page_size = page_size or self.settings.ixc_page_size
        max_pages = max_pages or self.settings.ixc_max_pages
        headers = {
            "Authorization": self.settings.authorization_token,
            "ixcsoft": "listar",
            "Content-Type": "application/json",
        }
        base_payload: dict[str, Any] = {
            "qtype": "id",
            "query": "0",
            "oper": ">",
            "sortname": "id",
            "sortorder": "asc",
            "rp": str(page_size),
        }
        if extra_body:
            base_payload.update(extra_body)

        records: list[dict[str, Any]] = []
        async with httpx.AsyncClient(
            timeout=self.settings.http_timeout_seconds,
            verify=self.settings.ixc_verify_ssl,
        ) as client:
            for page in range(1, max_pages + 1):
                payload = dict(base_payload)
                payload["page"] = str(page)
                response = await client.post(
                    f"{self.settings.api_root}/{table}",
                    headers=headers,
                    json=payload,
                )
                _raise_for_status(response)
                data = response.json()
                if not isinstance(data, dict):
                    raise RuntimeError(f"Resposta inesperada do IXC: {data!r}")

                page_records = data.get("registros")
                if not page_records:
                    break
                if not isinstance(page_records, list):
                    raise RuntimeError(
                        f"'registros' invalido na resposta da tabela '{table}'."
                    )

                for item in page_records:
                    if isinstance(item, dict):
                        records.append(item)

                total = _to_int(data.get("total"))
                if total and len(records) >= total:
                    break
                if len(page_records) < page_size:
                    break
            else:
                if not allow_partial:
                    raise RuntimeError(
                        f"Limite de paginas atingido ({max_pages}) para tabela '{table}'. "
                        "Aumente IXC_MAX_PAGES se necessario."
                    )
        return records

    async def post_action(self, endpoint: str, payload: dict[str, Any]) -> Any:
        if not self.settings.ixc_token.strip():
            raise RuntimeError(
                "IXC_TOKEN nao definido. Configure o token no arquivo .env."
            )

        headers = {
            "Authorization": self.settings.authorization_token,
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient(
            timeout=self.settings.http_timeout_seconds,
            verify=self.settings.ixc_verify_ssl,
        ) as client:
            response = await client.post(
                f"{self.settings.api_root}/{endpoint}",
                headers=headers,
                json=payload,
            )
            _raise_for_status(response)
            try:
                return response.json()
            except ValueError:
                return {"raw": response.text}


def _to_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _raise_for_status(response: httpx.Response) -> None:
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        detail = _friendly_ixc_error(response)
        raise RuntimeError(detail) from exc


def _friendly_ixc_error(response: httpx.Response) -> str:
    status = response.status_code
    body = (response.text or '').strip().lower()

    if status == 401:
        challenge = (response.headers.get("www-authenticate") or "").lower()
        if challenge.startswith("basic"):
            return (
                "O servidor recusou a autenticacao Basic (HTTP 401). Compare o ID/token "
                "salvo neste painel com a credencial da aplicacao que conecta. "
                "Esta resposta nao confirma bloqueio de IP."
            )
        return (
            "O servico recusou a credencial configurada (HTTP 401). "
            "Confira o ID do usuario e o token da API."
        )

    if 'ip' in body and ('liberad' in body or 'permit' in body):
        return (
            'Erro de acesso no IXC. O servidor do painel precisa estar liberado no IXC. '
            f'Libere o IP {SERVER_PUBLIC_IP}.'
        )

    return f'Falha ao consultar o IXC (HTTP {status}).'
