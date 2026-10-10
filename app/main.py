from __future__ import annotations

import asyncio
import json
import logging
import secrets
from datetime import datetime
from pathlib import Path
from typing import Any
import httpx
from fastapi import Body, Depends, FastAPI, Header, HTTPException, Query
from fastapi.responses import FileResponse, RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .config import get_settings
from .db import init_db
from .ixc_client import IXCClient
from .repository import (
    create_dashboard_filter_preset,
    delete_dashboard_filter_preset,
    fetch_order_by_os_id,
    list_dashboard_filter_presets,
    update_dashboard_filter_preset,
)
from .services.discovery_service import DiscoveryService
from .services.metrics_service import MetricsService
from .services.operations_board_service import OperationsBoardService
from .services.settings_service import SettingsService
from .services.sync_service import SyncService
from .services.weekly_vip_pdf_service import build_weekly_vip_pdf

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class DashboardFilterPresetPayload(BaseModel):
    name: str = Field(min_length=1)
    subject_group: str | None = None
    branch: str | None = None
    sector: str | None = None
    subjects: list[str] = Field(default_factory=list)
    technicians: list[str] = Field(default_factory=list)

    def cleaned(self) -> dict[str, Any]:
        return {
            "name": self.name.strip(),
            "subject_group": _clean_optional_filter(self.subject_group),
            "branch": _clean_optional_filter(self.branch),
            "sector": _clean_optional_filter(self.sector),
            "subjects": _clean_filter_list(self.subjects),
            "technicians": _clean_filter_list(self.technicians),
        }


class IXCAnalyzeOrderPayload(BaseModel):
    os_id: str = Field(min_length=1)
    id_setor: str = Field(min_length=1)
    id_tecnico: str = Field(min_length=1)
    mensagem: str = "Enviado para analise pelo Mapa Diario"
    data_inicio: str = Field(min_length=1)
    data_final: str = Field(min_length=1)

    def cleaned(self) -> dict[str, str]:
        return {
            "id_setor": self.id_setor.strip(),
            "id_chamado": self.os_id.strip(),
            "status": "AN",
            "id_tecnico": self.id_tecnico.strip(),
            "mensagem": self.mensagem.strip() or "Enviado para analise pelo Mapa Diario",
            "data_inicio": self.data_inicio.strip(),
            "data_final": self.data_final.strip(),
        }


app = FastAPI(title="Dashboard IXC", version="1.0.0")
app.state.dashboard_event_subscribers = set()

STATIC_DIR = Path(__file__).resolve().parent / "static"
REACT_DASHBOARD_DIR = STATIC_DIR / "react-dashboard"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.on_event("startup")
async def on_startup() -> None:
    init_db()
    await _apply_runtime_settings(get_settings(), run_sync_on_startup=True)


@app.on_event("shutdown")
async def on_shutdown() -> None:
    await _cancel_sync_task()


async def _cancel_sync_task() -> None:
    for attr_name in ("sync_task", "startup_sync_task"):
        task = getattr(app.state, attr_name, None)
        if task is None:
            continue
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
        setattr(app.state, attr_name, None)


async def _publish_dashboard_event(event_type: str, payload: dict[str, Any]) -> None:
    subscribers = getattr(app.state, "dashboard_event_subscribers", set())
    if not subscribers:
        return

    event = {"event": event_type, "payload": payload}
    stale_subscribers = []
    for queue in tuple(subscribers):
        try:
            queue.put_nowait(event)
        except asyncio.QueueFull:
            stale_subscribers.append(queue)

    for queue in stale_subscribers:
        subscribers.discard(queue)


def _sync_progress_callback(source: str):
    async def publish(payload: dict[str, Any]) -> None:
        await _publish_dashboard_event("sync_progress", {"source": source, **payload})

    return publish


def _format_sse_event(event_type: str, payload: dict[str, Any]) -> str:
    data = json.dumps(payload, ensure_ascii=False, default=str)
    return f"event: {event_type}\ndata: {data}\n\n"


async def _run_startup_sync() -> None:
    try:
        result = await app.state.sync_service.sync_now(
            progress_callback=_sync_progress_callback("startup"),
        )
        await _publish_dashboard_event("sync_finished", {"source": "startup", **result})
        logger.info("Sincronizacao inicial concluida.")
    except Exception as exc:
        await _publish_dashboard_event("sync_error", {"source": "startup", "message": str(exc)})
        logger.exception("Falha na sincronizacao inicial: %s", exc)


async def _apply_runtime_settings(settings, *, run_sync_on_startup: bool) -> None:
    await _cancel_sync_task()

    app.state.settings = settings
    app.state.sync_service = SyncService(settings)
    app.state.metrics_service = MetricsService(settings)
    app.state.operations_board_service = OperationsBoardService()
    app.state.discovery_service = DiscoveryService(settings)
    app.state.settings_service = SettingsService(settings)

    ixc_ready = _is_ixc_configuration_ready(settings.ixc_base_url, settings.ixc_token)
    if not ixc_ready:
        logger.warning(
            "IXC_BASE_URL/IXC_TOKEN ainda em valor de exemplo. "
            "Sincronizacao automatica desativada ate configurar."
        )

    if run_sync_on_startup and settings.ixc_sync_on_startup and ixc_ready:
        app.state.startup_sync_task = asyncio.create_task(_run_startup_sync())
        logger.info("Sincronizacao inicial iniciada em segundo plano.")

    if settings.ixc_auto_sync and ixc_ready:
        app.state.sync_task = asyncio.create_task(_periodic_sync())


async def _periodic_sync() -> None:
    while True:
        settings = app.state.settings
        await asyncio.sleep(max(5, settings.ixc_sync_interval_seconds))
        try:
            result = await app.state.sync_service.sync_now(
                progress_callback=_sync_progress_callback("auto"),
            )
            await _publish_dashboard_event("sync_finished", {"source": "auto", **result})
        except Exception as exc:
            await _publish_dashboard_event("sync_error", {"source": "auto", "message": str(exc)})
            logger.exception("Falha na sincronizacao automatica: %s", exc)


def _is_ixc_configuration_ready(base_url: str, token: str) -> bool:
    url = (base_url or "").strip().lower()
    raw_token = (token or "").strip()
    upper_token = raw_token.upper()
    placeholder_urls = {
        "https://seu-servidor-ixc.com.br",
        "http://seu-servidor-ixc.com.br",
    }
    placeholder_tokens = {
        "",
        "SEU_TOKEN_OU_BASIC_TOKEN",
        "BASIC SEU_TOKEN_OU_BASIC_TOKEN",
    }
    if url in placeholder_urls:
        return False
    if upper_token in placeholder_tokens:
        return False
    return True


def _require_admin(x_admin_password: str | None = Header(default=None)) -> None:
    expected_password = get_settings().app_admin_password.strip()
    if not expected_password:
        return
    provided_password = (x_admin_password or "").strip()
    if not secrets.compare_digest(provided_password, expected_password):
        raise HTTPException(status_code=401, detail="Senha administrativa invalida.")


@app.get("/", include_in_schema=False)
async def index() -> FileResponse:
    return await react_dashboard()


@app.get("/dashboard-legacy", include_in_schema=False)
async def legacy_dashboard(tab: str | None = None) -> FileResponse | RedirectResponse:
    if tab == "settings":
        return RedirectResponse(url="/settings", status_code=307)
    return FileResponse(
        STATIC_DIR / "index.html",
        headers={"Cache-Control": "no-store"},
    )


@app.get("/settings", include_in_schema=False)
async def settings_dashboard() -> FileResponse:
    return FileResponse(
        STATIC_DIR / "settings.html",
        headers={"Cache-Control": "no-store"},
    )


@app.get("/dashboard-react", include_in_schema=False)
async def react_dashboard() -> FileResponse:
    index_file = REACT_DASHBOARD_DIR / "index.html"
    if not index_file.exists():
        raise HTTPException(
            status_code=404,
            detail="Dashboard React ainda nao foi compilado. Execute npm run build.",
        )
    return FileResponse(index_file, headers={"Cache-Control": "no-store"})


@app.get("/api/health")
async def health() -> dict:
    return {"status": "ok"}


@app.get("/api/dashboard/filter-presets")
async def get_dashboard_filter_presets() -> dict[str, Any]:
    return {"presets": list_dashboard_filter_presets()}


@app.post("/api/dashboard/filter-presets")
async def create_filter_preset(
    payload: DashboardFilterPresetPayload,
    _: None = Depends(_require_admin),
) -> dict[str, Any]:
    try:
        return {"preset": create_dashboard_filter_preset(payload.cleaned())}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.put("/api/dashboard/filter-presets/{preset_id}")
async def update_filter_preset(
    preset_id: int,
    payload: DashboardFilterPresetPayload,
    _: None = Depends(_require_admin),
) -> dict[str, Any]:
    try:
        preset = update_dashboard_filter_preset(preset_id, payload.cleaned())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if preset is None:
        raise HTTPException(status_code=404, detail="Filtro salvo nao encontrado.")
    return {"preset": preset}


@app.delete("/api/dashboard/filter-presets/{preset_id}")
async def delete_filter_preset(
    preset_id: int,
    _: None = Depends(_require_admin),
) -> dict[str, Any]:
    if not delete_dashboard_filter_preset(preset_id):
        raise HTTPException(status_code=404, detail="Filtro salvo nao encontrado.")
    return {"status": "success"}


@app.get("/api/settings")
async def get_app_settings(_: None = Depends(_require_admin)) -> dict[str, Any]:
    return {"values": app.state.settings_service.current_values()}


@app.put("/api/settings")
async def update_app_settings(
    payload: dict[str, Any] = Body(...),
    _: None = Depends(_require_admin),
) -> dict[str, Any]:
    try:
        new_settings = app.state.settings_service.update(payload)
        await _apply_runtime_settings(new_settings, run_sync_on_startup=False)
        return {
            "status": "success",
            "message": "Configuracoes salvas e aplicadas com sucesso.",
            "values": app.state.settings_service.current_values(),
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/api/settings/test-connection")
async def test_connection(_: None = Depends(_require_admin)) -> dict[str, Any]:
    try:
        return await app.state.discovery_service.test_connection()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/api/events/dashboard")
async def dashboard_events() -> StreamingResponse:
    queue: asyncio.Queue[dict[str, Any]] = asyncio.Queue(maxsize=20)
    app.state.dashboard_event_subscribers.add(queue)

    async def event_stream():
        try:
            yield _format_sse_event("connected", {"status": "connected"})
            while True:
                try:
                    event = await asyncio.wait_for(queue.get(), timeout=25)
                    yield _format_sse_event(event["event"], event["payload"])
                except asyncio.TimeoutError:
                    yield ": ping\n\n"
        finally:
            app.state.dashboard_event_subscribers.discard(queue)

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@app.post("/api/sync")
async def run_sync(
    full: bool = Query(default=False),
    _: None = Depends(_require_admin),
) -> dict:
    try:
        await _publish_dashboard_event(
            "sync_progress",
            {
                "source": "manual",
                "percent": 0,
                "stage": "queued",
                "message": "Sincronizacao solicitada",
            },
        )
        result = await app.state.sync_service.sync_now(
            force_full=full,
            progress_callback=_sync_progress_callback("manual"),
        )
        await _publish_dashboard_event("sync_finished", {"source": "manual", **result})
        return result
    except Exception as exc:
        await _publish_dashboard_event("sync_error", {"source": "manual", "message": str(exc)})
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/api/metrics/overview")
async def metrics_overview(
    date: str | None = Query(default=None),
    start_date: str | None = Query(default=None),
    end_date: str | None = Query(default=None),
    weekly_start_date: str | None = Query(default=None),
    weekly_end_date: str | None = Query(default=None),
    subject: list[str] | None = Query(default=None),
    subject_group: str | None = Query(default=None),
    branch: str | None = Query(default=None),
    sector: str | None = Query(default=None),
    technician: list[str] | None = Query(default=None),
    status: str | None = Query(default=None),
) -> dict:
    parsed_date = _parse_date_param(date, "date")
    parsed_start = _parse_date_param(start_date, "start_date")
    parsed_end = _parse_date_param(end_date, "end_date")
    parsed_weekly_start = _parse_date_param(weekly_start_date, "weekly_start_date")
    parsed_weekly_end = _parse_date_param(weekly_end_date, "weekly_end_date")
    parsed_subjects = _parse_multi_filter_param(subject)
    parsed_technicians = _parse_multi_filter_param(technician)

    return app.state.metrics_service.build_overview(
        parsed_date,
        start_date=parsed_start,
        end_date=parsed_end,
        weekly_start_date=parsed_weekly_start,
        weekly_end_date=parsed_weekly_end,
        subject_names=parsed_subjects,
        subject_group_name=subject_group,
        branch_name=branch,
        sector_id=sector,
        technician_names=parsed_technicians,
        status_name=status,
    )


@app.get("/api/metrics/filter-options")
async def metrics_filter_options() -> dict:
    return app.state.metrics_service.build_filter_options()


@app.get("/api/metrics/card-orders")
async def metrics_card_orders(
    metric: str = Query(...),
    date: str | None = Query(default=None),
    start_date: str | None = Query(default=None),
    end_date: str | None = Query(default=None),
    subject: list[str] | None = Query(default=None),
    subject_group: str | None = Query(default=None),
    branch: str | None = Query(default=None),
    sector: str | None = Query(default=None),
    technician: list[str] | None = Query(default=None),
    limit: int = Query(default=200, ge=10, le=1000),
) -> dict[str, Any]:
    parsed_date = _parse_date_param(date, "date")
    parsed_start = _parse_date_param(start_date, "start_date")
    parsed_end = _parse_date_param(end_date, "end_date")
    parsed_subjects = _parse_multi_filter_param(subject)
    parsed_technicians = _parse_multi_filter_param(technician)
    try:
        return app.state.metrics_service.build_card_orders(
            metric=metric,
            selected_date=parsed_date,
            start_date=parsed_start,
            end_date=parsed_end,
            subject_names=parsed_subjects,
            subject_group_name=subject_group,
            branch_name=branch,
            sector_id=sector,
            technician_name=parsed_technicians,
            limit=limit,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/metrics/weekly-vip-report")
async def weekly_vip_report(
    start_date: str | None = Query(default=None),
    end_date: str | None = Query(default=None),
    subject: list[str] | None = Query(default=None),
    subject_group: str | None = Query(default=None),
    branch: str | None = Query(default=None),
    sector: str | None = Query(default=None),
    technician: list[str] | None = Query(default=None),
) -> dict[str, Any]:
    parsed_start = _parse_date_param(start_date, "start_date")
    parsed_end = _parse_date_param(end_date, "end_date")
    parsed_subjects = _parse_multi_filter_param(subject)
    parsed_technicians = _parse_multi_filter_param(technician)
    try:
        return app.state.metrics_service.build_weekly_vip_report(
            start_date=parsed_start,
            end_date=parsed_end,
            subject_names=parsed_subjects,
            subject_group_name=subject_group,
            branch_name=branch,
            sector_id=sector,
            technician_names=parsed_technicians,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/metrics/weekly-vip-report.pdf")
async def weekly_vip_report_pdf(
    start_date: str | None = Query(default=None),
    end_date: str | None = Query(default=None),
    subject: list[str] | None = Query(default=None),
    subject_group: str | None = Query(default=None),
    branch: str | None = Query(default=None),
    sector: str | None = Query(default=None),
    technician: list[str] | None = Query(default=None),
) -> StreamingResponse:
    parsed_start = _parse_date_param(start_date, "start_date")
    parsed_end = _parse_date_param(end_date, "end_date")
    parsed_subjects = _parse_multi_filter_param(subject)
    parsed_technicians = _parse_multi_filter_param(technician)
    try:
        report = app.state.metrics_service.build_weekly_vip_report(
            start_date=parsed_start,
            end_date=parsed_end,
            subject_names=parsed_subjects,
            subject_group_name=subject_group,
            branch_name=branch,
            sector_id=sector,
            technician_names=parsed_technicians,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    pdf_buffer, filename = build_weekly_vip_pdf(report)
    headers = {"Content-Disposition": f'attachment; filename="{filename}"'}
    return StreamingResponse(pdf_buffer, media_type="application/pdf", headers=headers)


@app.get("/api/metrics/technician-orders")
async def metrics_technician_orders(
    start_date: str | None = Query(default=None),
    end_date: str | None = Query(default=None),
    subject: list[str] | None = Query(default=None),
    subject_group: str | None = Query(default=None),
    branch: str | None = Query(default=None),
    sector: str | None = Query(default=None),
    technician: str | None = Query(default=None),
    status: str | None = Query(default=None),
) -> dict[str, Any]:
    parsed_start = _parse_date_param(start_date, "start_date")
    parsed_end = _parse_date_param(end_date, "end_date")
    parsed_subjects = _parse_multi_filter_param(subject)
    return app.state.metrics_service.build_technician_order_details(
        start_date=parsed_start,
        end_date=parsed_end,
        subject_names=parsed_subjects,
        subject_group_name=subject_group,
        branch_name=branch,
        sector_id=sector,
        technician_name=technician,
        status_name=status,
    )


@app.get("/api/orders/{os_id}")
async def order_details(os_id: str, include_raw: bool = Query(default=False)) -> dict[str, Any]:
    order = fetch_order_by_os_id(os_id)
    if order is None:
        raise HTTPException(status_code=404, detail=f"OS {os_id} nao encontrada na base sincronizada.")

    raw_payload = order.get("raw_payload") if isinstance(order.get("raw_payload"), dict) else {}
    opened_at, assumed_at, execution_started_at, closed_at, due_at, execution_source = (
        _resolve_order_datetimes(order, raw_payload)
    )
    now_local = datetime.now().replace(tzinfo=None)
    sla_status = _evaluate_sla_status(due_at=due_at, closed_at=closed_at, now_local=now_local)
    process_notes = _extract_process_notes(raw_payload)

    response: dict[str, Any] = {
        "os_id": str(order.get("os_id") or ""),
        "status": str(order.get("status") or ""),
        "subject": str(order.get("subject_name") or ""),
        "branch": str(order.get("branch_name") or ""),
        "customer_id": str(order.get("customer_id") or ""),
        "customer_name": str(order.get("customer_name") or ""),
        "technician_id": str(order.get("technician_id") or ""),
        "technician_name": str(order.get("technician_name") or ""),
        "opened_at": _datetime_to_text(opened_at),
        "assumed_at": _datetime_to_text(assumed_at),
        "execution_started_at": _datetime_to_text(execution_started_at),
        "execution_source": execution_source,
        "execution_source_label": _execution_source_label(execution_source),
        "closed_at": _datetime_to_text(closed_at),
        "due_at": _datetime_to_text(due_at),
        "updated_at": order.get("updated_at"),
        "sla": {
            "status": sla_status,
            "label": _sla_label(sla_status),
        },
        "durations": {
            "response_minutes": _diff_minutes(opened_at, execution_started_at),
            "execution_minutes": _diff_minutes(execution_started_at, closed_at),
            "total_minutes": _diff_minutes(opened_at, closed_at),
        },
        "raw_highlights": _extract_raw_highlights(raw_payload),
        "raw_payload_keys": sorted(raw_payload.keys()),
        "process_notes": process_notes,
        "process_summary": " | ".join(note["text"] for note in process_notes),
    }
    if include_raw:
        response["raw_payload"] = raw_payload
    return response


@app.get("/api/operations-board")
async def operations_board(
    date: str = Query(...),
    technician: list[str] | None = Query(default=None),
    status: list[str] | None = Query(default=None),
    subject: list[str] | None = Query(default=None),
    subject_group: str | None = Query(default=None),
    sector: str | None = Query(default=None),
    branch: str | None = Query(default=None),
    team_name: str | None = Query(default=None),
    team_key: str | None = Query(default=None),
) -> dict:
    parsed_date = _parse_date_param(date, "date")
    parsed_technicians = _parse_multi_filter_param(technician)
    if technician is not None and parsed_technicians is None:
        parsed_technicians = []
    parsed_statuses = _parse_multi_filter_param(status)
    if status is not None and parsed_statuses is None:
        parsed_statuses = []
    parsed_subjects = _parse_multi_filter_param(subject)
    if subject is not None and parsed_subjects is None:
        parsed_subjects = []
    return app.state.operations_board_service.get_board(
        parsed_date,
        selected_technicians=parsed_technicians,
        selected_statuses=parsed_statuses,
        subject_names=parsed_subjects,
        subject_group_name=subject_group,
        sector_id=sector,
        branch_name=branch,
        team_name=team_name,
        team_key=team_key,
    )


@app.put("/api/operations-board")
async def save_operations_board(
    date: str = Query(...),
    payload: dict[str, Any] | None = None,
    _: None = Depends(_require_admin),
) -> dict:
    parsed_date = _parse_date_param(date, "date")
    data = payload or {}
    selected_technicians = _parse_multi_filter_param(data.get("selected_technicians"))
    if "selected_technicians" in data and selected_technicians is None:
        selected_technicians = []
    try:
        return app.state.operations_board_service.save_board(
            parsed_date,
            responsible_name=data.get("responsible_name"),
            shift_label=data.get("shift_label"),
            general_notes=data.get("general_notes"),
            selected_technicians=selected_technicians,
            team_name=data.get("team_name"),
            team_key=data.get("team_key"),
            entries=data.get("entries", []),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/ixc/orders/analyze")
async def analyze_ixc_order(
    payload: IXCAnalyzeOrderPayload,
    _: None = Depends(_require_admin),
) -> dict[str, Any]:
    data = payload.cleaned()
    missing = [
        label
        for label, value in {
            "id_setor": data["id_setor"],
            "id_chamado": data["id_chamado"],
            "id_tecnico": data["id_tecnico"],
            "data_inicio": data["data_inicio"],
            "data_final": data["data_final"],
        }.items()
        if not value
    ]
    if missing:
        raise HTTPException(status_code=400, detail=f"Campos obrigatorios ausentes: {', '.join(missing)}.")
    try:
        response = await IXCClient(app.state.settings).post_action("su_oss_chamado_analisar", data)
    except httpx.HTTPStatusError as exc:
        detail = exc.response.text or str(exc)
        raise HTTPException(status_code=502, detail=f"IXC recusou a analise da OS: {detail}") from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return {"ok": True, "response": response}


@app.patch("/api/operations-board/entries/{entry_id}/comment")
async def save_operations_board_entry_comment(
    entry_id: int,
    payload: dict[str, Any] | None = None,
    _: None = Depends(_require_admin),
) -> dict[str, Any]:
    data = payload or {}
    entry = app.state.operations_board_service.save_entry_comment(
        entry_id,
        data.get("comment_note"),
    )
    if entry is None:
        raise HTTPException(status_code=404, detail="Linha do mapa diario nao encontrada.")
    return {"entry": entry}


@app.delete("/api/operations-board")
async def delete_operations_board(
    date: str = Query(...),
    team_name: str | None = Query(default=None),
    team_key: str | None = Query(default=None),
    _: None = Depends(_require_admin),
) -> dict[str, Any]:
    parsed_date = _parse_date_param(date, "date")
    if team_name is None and team_key is None:
        raise HTTPException(status_code=400, detail="Informe team_name ou team_key para exclusao.")
    return app.state.operations_board_service.delete_board(
        parsed_date,
        team_name=team_name,
        team_key=team_key,
    )


@app.get("/api/operations-board/lists")
async def list_operations_boards(
    date: str | None = Query(default=None),
    all_dates: bool = Query(default=False),
) -> dict[str, Any]:
    if all_dates:
        return {
            "date": None,
            "lists": app.state.operations_board_service.list_saved_lists(),
        }
    parsed_date = _parse_date_param(date, "date")
    if parsed_date is None:
        raise HTTPException(status_code=400, detail="Parametro date obrigatorio quando all_dates=false.")
    return {
        "date": str(parsed_date),
        "lists": app.state.operations_board_service.list_saved_lists(parsed_date),
    }


@app.post("/api/operations-board/delay-report")
async def operations_board_delay_report(
    date: str = Query(...),
    team_name: str | None = Query(default=None),
    team_key: str | None = Query(default=None),
    branch: str | None = Query(default=None),
    payload: dict[str, Any] | None = None,
    _: None = Depends(_require_admin),
) -> dict[str, Any]:
    parsed_date = _parse_date_param(date, "date")
    data = payload or {}
    payload_branch = data.get("branch")
    normalized_payload_branch = (
        str(payload_branch).strip() if payload_branch is not None else None
    )
    if normalized_payload_branch in {"", "__all__"}:
        normalized_payload_branch = None
    effective_branch = branch
    if effective_branch in {None, "", "__all__"}:
        effective_branch = normalized_payload_branch
    selected_technicians = _parse_multi_filter_param(data.get("selected_technicians"))
    if "selected_technicians" in data and selected_technicians is None:
        selected_technicians = []
    raw_entries = data.get("entries")
    entries_override = raw_entries if isinstance(raw_entries, list) else None
    return app.state.operations_board_service.build_delay_report(
        parsed_date,
        entries_override=entries_override,
        selected_technicians=selected_technicians,
        team_name=team_name,
        team_key=team_key,
        branch_name=effective_branch,
    )


@app.get("/api/discovery/os-fields")
async def discovery_os_fields(
    sample_size: int = Query(default=100, ge=10, le=1000),
    _: None = Depends(_require_admin),
) -> dict:
    try:
        return await app.state.discovery_service.inspect_os_table(sample_size=sample_size)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/api/discovery/subject-fields")
async def discovery_subject_fields(
    sample_size: int = Query(default=50, ge=10, le=1000),
    _: None = Depends(_require_admin),
) -> dict:
    settings = app.state.settings
    try:
        return await app.state.discovery_service.inspect_lookup_table(
            table=settings.ixc_subject_table,
            preferred_id_field=settings.ixc_subject_id_field,
            preferred_name_field=settings.ixc_subject_name_field,
            sample_size=sample_size,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/api/discovery/tech-fields")
async def discovery_tech_fields(
    sample_size: int = Query(default=50, ge=10, le=1000),
    _: None = Depends(_require_admin),
) -> dict:
    settings = app.state.settings
    try:
        return await app.state.discovery_service.inspect_lookup_table(
            table=settings.ixc_tech_table,
            preferred_id_field=settings.ixc_tech_id_field,
            preferred_name_field=settings.ixc_tech_name_field,
            sample_size=sample_size,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


def _clean_optional_filter(value: str | None) -> str | None:
    text = str(value or "").strip()
    if not text or text == "__all__":
        return None
    return text


def _clean_filter_list(values: list[str] | None) -> list[str]:
    normalized = _parse_multi_filter_param(values)
    return normalized or []


def _parse_date_param(value: str | None, param_name: str):
    if value is None:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise HTTPException(
            status_code=400, detail=f"Parametro {param_name} deve usar formato YYYY-MM-DD."
        ) from exc


def _parse_multi_filter_param(values: list[str] | None) -> list[str] | None:
    if not values:
        return None
    normalized: list[str] = []
    seen: set[str] = set()
    for value in values:
        for chunk in str(value or "").split(","):
            text = chunk.strip()
            if not text or text == "__all__":
                continue
            if text in seen:
                continue
            seen.add(text)
            normalized.append(text)
    return normalized or None


def _parse_local_datetime(value: str | None) -> datetime | None:
    if value is None:
        return None
    raw = str(value).strip()
    if not raw:
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(raw, fmt)
        except ValueError:
            continue
    try:
        parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed.replace(tzinfo=None)


def _diff_minutes(start: datetime | None, end: datetime | None) -> float | None:
    if start is None or end is None:
        return None
    diff = (end - start).total_seconds() / 60
    if diff < 0:
        return None
    return round(diff, 2)


def _datetime_to_text(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.strftime("%Y-%m-%d %H:%M:%S")


def _evaluate_sla_status(
    *,
    due_at: datetime | None,
    closed_at: datetime | None,
    now_local: datetime,
) -> str:
    if due_at is None:
        return "no_due"
    end_at = closed_at or now_local
    if end_at <= due_at:
        return "within"
    return "overdue"


def _sla_label(status: str) -> str:
    if status == "within":
        return "Dentro do SLA"
    if status == "overdue":
        return "Fora do SLA"
    return "Sem prazo"


def _extract_raw_highlights(raw_payload: dict[str, Any]) -> dict[str, Any]:
    if not raw_payload:
        return {}
    preferred_keys = [
        "id",
        "id_cliente",
        "cliente",
        "nome_cliente",
        "razao",
        "razao_social",
        "id_login",
        "id_assunto",
        "id_filial",
        "funcionario",
        "setor",
        "data_abertura",
        "data_hora_assumido",
        "data_hora_execucao",
        "data_inicio",
        "data_final",
        "data_fechamento",
        "data_prazo_limite",
        "data_agenda",
        "data_prev_final",
        "endereco",
        "bairro",
        "cidade",
        "complemento",
        "mensagem",
        "mensagem_resposta",
        "descricao",
        "obs",
        "observacao",
    ]
    highlights: dict[str, Any] = {}
    for key in preferred_keys:
        value = raw_payload.get(key)
        if value is None:
            continue
        text = str(value).strip()
        if not text:
            continue
        highlights[key] = text
    return highlights


def _resolve_order_datetimes(
    order: dict[str, Any],
    raw_payload: dict[str, Any],
) -> tuple[datetime | None, datetime | None, datetime | None, datetime | None, datetime | None, str | None]:
    opened_at = _parse_local_datetime(order.get("opened_at")) or _first_datetime_from_raw(
        raw_payload,
        [
            "data_abertura",
            "data_hora_abertura",
            "data_criacao",
            "abertura",
        ],
    )[0]
    assumed_at = _first_datetime_from_raw(
        raw_payload,
        [
            "data_hora_assumido",
            "data_assumido",
            "assumido_em",
        ],
    )[0]

    execution_started_at, execution_source = _extract_execution_datetime_with_source(
        order,
        raw_payload,
    )

    closed_at = _parse_local_datetime(order.get("closed_at")) or _first_datetime_from_raw(
        raw_payload,
        [
            "data_fechamento",
            "data_encerramento",
            "data_finalizacao",
            "data_final",
            "fechamento",
        ],
    )[0]
    due_at = _parse_local_datetime(order.get("due_at")) or _first_datetime_from_raw(
        raw_payload,
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
    )[0]
    return opened_at, assumed_at, execution_started_at, closed_at, due_at, execution_source


def _first_datetime_from_raw(
    raw_payload: dict[str, Any],
    keys: list[str],
) -> tuple[datetime | None, str | None]:
    if not raw_payload:
        return None, None
    for key in keys:
        parsed = _parse_local_datetime(raw_payload.get(key))
        if parsed is not None:
            return parsed, key
    return None, None


def _extract_execution_datetime_with_source(
    order: dict[str, Any],
    raw_payload: dict[str, Any],
) -> tuple[datetime | None, str | None]:
    normalized_status = str(order.get("status") or "").strip().upper()
    if normalized_status in {"AG", "AGENDA", "AGENDADA", "REAGENDADA", "REAGENDADO", "REAGENDAMENTO", "R", "PENDENTE"}:
        return None, None

    row_execution = _parse_local_datetime(order.get("execution_started_at"))
    if row_execution is not None:
        return row_execution, "service_orders.execution_started_at"

    for key in (
        "data_hora_execucao",
        "data_inicio_execucao",
        "inicio_execucao",
    ):
        parsed = _parse_local_datetime(raw_payload.get(key))
        if parsed is not None:
            return parsed, f"raw_payload.{key}"

    return None, None


def _extract_process_notes(raw_payload: dict[str, Any]) -> list[dict[str, str]]:
    if not raw_payload:
        return []
    preferred_keys: list[tuple[str, str]] = [
        ("mensagem_resposta", "Finalizacao"),
        ("resposta_tecnico", "Finalizacao"),
        ("mensagem_finalizacao", "Finalizacao"),
        ("relato_finalizacao", "Finalizacao"),
        ("descricao_final", "Finalizacao"),
        ("solucao", "Finalizacao"),
        ("relato_tecnico", "Relato tecnico"),
        ("mensagem_tecnico", "Relato tecnico"),
        ("relato", "Relato tecnico"),
        ("mensagem", "Relato tecnico"),
        ("descricao_ocorrencia", "Relato tecnico"),
        ("descricao_atividade", "Relato tecnico"),
        ("descricao", "Relato tecnico"),
        ("obs_tecnico", "Relato tecnico"),
        ("observacao", "Relato tecnico"),
        ("observacoes", "Relato tecnico"),
        ("obs", "Relato tecnico"),
        ("parecer", "Relato tecnico"),
        ("detalhes", "Relato tecnico"),
        ("historico", "Relato tecnico"),
        ("resposta", "Relato tecnico"),
    ]
    seen_values: set[str] = set()
    notes: list[dict[str, str]] = []
    for key, label in preferred_keys:
        value = raw_payload.get(key)
        if value is None:
            continue
        text = " ".join(str(value).split())
        if not text or text.lower() in {"null", "none"} or text in seen_values:
            continue
        seen_values.add(text)
        notes.append(
            {
                "key": key,
                "label": label,
                "text": f"{label}: {text}",
            }
        )
    return notes


def _execution_source_label(value: str | None) -> str | None:
    if not value:
        return None
    if value == "service_orders.execution_started_at":
        return "Campo sincronizado da OS"
    if value.startswith("raw_payload."):
        return f"Derivado de {value.removeprefix('raw_payload.')}"
    return value
