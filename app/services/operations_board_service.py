from __future__ import annotations

from datetime import date, datetime
import json
import re
from typing import Any
import unicodedata

from ..repository import (
    delete_operation_board,
    fetch_customer_name_by_customer_id,
    fetch_order_by_os_id,
    fetch_operation_board_entries,
    fetch_operation_board_header,
    fetch_operation_board_references,
    list_operation_board_teams,
    normalize_operation_board_team_key,
    replace_operation_board_entries,
    update_operation_board_entry_comment,
    upsert_operation_board_header,
)

DEFAULT_TIME_SLOTS = [
    "08:00 - 09:00",
    "09:00 - 10:00",
    "10:00 - 11:00",
    "11:00 - 12:00",
    "12:00 - 13:00",
    "13:00 - 14:00",
    "14:00 - 15:00",
    "15:00 - 16:00",
    "16:00 - 17:00",
    "17:00 - 18:00",
    "18:00 - 19:00",
    "19:00 - 20:00",
]
GAP_MINUTES_FOR_OCCURRENCE = 20

_STATUS_FILTER_LABELS = {
    "AGUARDANDO": "Aguardando",
    "ABERTA": "Aberta",
    "AGENDADA": "Agendada",
    "ENCAMINHADA": "Encaminhada",
    "REAGENDADA": "Reagendada",
    "DESLOCAMENTO": "Deslocamento",
    "EM_EXECUCAO": "Em execucao",
    "FINALIZADA": "Finalizada",
    "CANCELADA": "Cancelada",
}
_STATUS_FILTER_ORDER = [
    "AGUARDANDO",
    "ABERTA",
    "AGENDADA",
    "ENCAMINHADA",
    "REAGENDADA",
    "DESLOCAMENTO",
    "EM_EXECUCAO",
    "FINALIZADA",
    "CANCELADA",
]


class OperationsBoardService:
    def get_board(
        self,
        target_date: date,
        *,
        selected_technicians: list[str] | None = None,
        selected_statuses: list[str] | None = None,
        subject_names: list[str] | None = None,
        subject_group_name: str | None = None,
        sector_id: str | None = None,
        branch_name: str | None = None,
        team_name: str | None = None,
        team_key: str | None = None,
    ) -> dict[str, Any]:
        entry_date = str(target_date)
        requested_team_name = _clean_text(team_name)
        requested_team_key = _clean_text(team_key)
        cleaned_branch_name = _clean_text(branch_name)
        persisted_header = fetch_operation_board_header(
            entry_date,
            team_name=team_name if requested_team_key is None and team_name is not None else None,
            team_key=requested_team_key,
        ) or {
            "entry_date": entry_date,
            "team_key": normalize_operation_board_team_key(
                requested_team_name,
                team_key=requested_team_key,
            ),
            "responsible_name": "",
            "shift_label": "08:00 - 20:00",
            "general_notes": "",
            "selected_technicians": "[]",
            "team_name": requested_team_name or "",
            "updated_at": None,
        }
        stored_selected_technicians = _parse_selected_technicians(
            persisted_header.get("selected_technicians")
        )
        normalized_stored_selected_technicians = _normalize_selected_technicians(
            stored_selected_technicians
        )
        requested_selected_technicians = (
            _normalize_selected_technicians(selected_technicians)
            if selected_technicians is not None
            else None
        )
        if requested_selected_technicians is None:
            normalized_selected_technicians = normalized_stored_selected_technicians
        elif requested_selected_technicians:
            normalized_selected_technicians = requested_selected_technicians
        elif requested_team_key is not None or requested_team_name is not None:
            # Ao carregar uma lista salva especifica (por team_key/team_name),
            # preserva os tecnicos salvos no cabecalho quando o frontend envia "__all__".
            normalized_selected_technicians = normalized_stored_selected_technicians
        else:
            normalized_selected_technicians = []
        normalized_selected_statuses = _normalize_selected_status_filters(selected_statuses)
        selected_status_filter_set = _normalize_status_filter_set(normalized_selected_statuses)
        persisted_team_key = _clean_text(persisted_header.get("team_key"))
        effective_team_key = normalize_operation_board_team_key(
            persisted_header.get("team_name"),
            team_key=persisted_team_key or requested_team_key,
        )
        effective_team_name = _prefer_meaningful_value(
            requested_team_name,
            _clean_text(persisted_header.get("team_name")),
        ) or ""
        header = {
            **persisted_header,
            "team_key": effective_team_key,
            "selected_technicians": normalized_selected_technicians,
            "selected_statuses": normalized_selected_statuses,
            "team_name": effective_team_name,
        }
        raw_saved_entries = fetch_operation_board_entries(entry_date, team_key=effective_team_key)
        has_raw_saved_entries = bool(raw_saved_entries)
        if not normalized_selected_technicians and raw_saved_entries:
            inferred_selected = _infer_selected_technicians_from_entries(raw_saved_entries)
            if inferred_selected:
                normalized_selected_technicians = inferred_selected
                header["selected_technicians"] = normalized_selected_technicians
        references = fetch_operation_board_references(
            entry_date,
            technician_names=normalized_selected_technicians or None,
            subject_name=subject_names,
            subject_group_name=subject_group_name,
            sector_id=sector_id,
            branch_name=cleaned_branch_name,
        )
        all_reference_orders = list(references.get("orders", []))
        filtered_reference_orders = [
            order
            for order in all_reference_orders
            if _order_matches_selected_statuses(
                order,
                target_date=target_date,
                selected_statuses=selected_status_filter_set,
            )
        ]
        order_lookup = {
            str(item["os_id"]): item
            for item in all_reference_orders
            if item.get("os_id") is not None
        }
        global_lookup_cache: dict[str, dict[str, Any] | None] = {}
        saved_entries = [
            _hydrate_entry(entry, order_lookup, global_lookup_cache)
            for entry in raw_saved_entries
        ]
        if cleaned_branch_name and saved_entries:
            saved_entries = [
                entry
                for entry in saved_entries
                if _entry_matches_selected_branch(
                    entry,
                    cleaned_branch_name,
                    order_lookup,
                    global_lookup_cache,
                )
            ]
        selected_subject_names = [
            _clean_text(item)
            for item in (subject_names or [])
            if _clean_text(item)
        ]
        selected_subject_set = {
            _normalize_matching_text(item)
            for item in selected_subject_names
        }
        selected_subject_group = None
        if subject_group_name:
            selected_subject_group = {
                _normalize_matching_text(item.get("subject_name"))
                for item in references.get("orders", [])
                if item.get("subject_name")
            }
        if selected_subject_set and saved_entries:
            saved_entries = [
                entry
                for entry in saved_entries
                if _entry_matches_selected_subjects(
                    entry,
                    selected_subject_set,
                    order_lookup,
                    global_lookup_cache,
                )
            ]
        if selected_subject_group is not None and saved_entries:
            saved_entries = [
                entry
                for entry in saved_entries
                if _entry_matches_selected_subjects(
                    entry,
                    selected_subject_group,
                    order_lookup,
                    global_lookup_cache,
                )
            ]
        if normalized_selected_technicians and saved_entries:
            selected_set = _normalize_technician_name_set(normalized_selected_technicians)
            saved_entries = [
                entry
                for entry in saved_entries
                if _entry_matches_selected_technicians(
                    entry,
                    selected_set,
                    order_lookup,
                    global_lookup_cache,
                )
            ]
        if selected_status_filter_set and saved_entries:
            saved_entries = [
                entry
                for entry in saved_entries
                if _entry_matches_selected_statuses(
                    entry,
                    target_date=target_date,
                    selected_statuses=selected_status_filter_set,
                    order_lookup=order_lookup,
                    global_lookup_cache=global_lookup_cache,
                )
            ]
        generated = False
        entries = saved_entries
        # Quando ja existe mapa salvo para a equipe/data, ele deve prevalecer
        # mesmo que o filtro de tecnicos atual da tela esteja diferente.
        force_generated = bool(
            requested_selected_technicians is not None
            and not _same_selection(
                requested_selected_technicians,
                _normalize_selected_technicians(stored_selected_technicians),
            )
            and not saved_entries
        )
        if force_generated:
            entries = _build_suggested_entries(
                filtered_reference_orders,
                target_date=target_date,
                default_team_name=effective_team_name,
                selected_technicians=normalized_selected_technicians,
            )
            generated = bool(entries)
        elif not entries and not has_raw_saved_entries:
            entries = _build_suggested_entries(
                filtered_reference_orders,
                target_date=target_date,
                default_team_name=effective_team_name,
                selected_technicians=normalized_selected_technicians,
            )
            generated = bool(entries)

        return {
            "header": header,
            "entries": entries,
            "generated": generated,
            "summary": _build_board_summary(
                filtered_reference_orders,
                entries,
                target_date=target_date,
                has_saved_entries=bool(saved_entries) and not force_generated,
            ),
            "references": {
                **references,
                "orders": filtered_reference_orders,
                "statuses": _collect_available_status_filters(
                    all_reference_orders,
                    target_date=target_date,
                ),
                "time_slots": DEFAULT_TIME_SLOTS,
            },
            "saved_lists": self.list_saved_lists(),
        }

    def save_board(
        self,
        target_date: date,
        *,
        responsible_name: str | None,
        shift_label: str | None,
        general_notes: str | None,
        selected_technicians: list[str] | None,
        team_name: str | None,
        team_key: str | None = None,
        entries: list[dict[str, Any]],
    ) -> dict[str, Any]:
        entry_date = str(target_date)
        normalized_selected_technicians = _normalize_selected_technicians(selected_technicians)
        explicit_selected_technicians = list(normalized_selected_technicians)
        cleaned_team_name = _clean_text(team_name)
        cleaned_team_key = _clean_text(team_key)
        # Protege contra sobrescrita acidental: se o frontend enviar uma team_key
        # antiga para um novo team_name, prioriza a chave derivada do novo nome.
        if cleaned_team_name and cleaned_team_key:
            normalized_name_key = normalize_operation_board_team_key(cleaned_team_name)
            normalized_explicit_key = normalize_operation_board_team_key(
                team_key=cleaned_team_key
            )
            if normalized_name_key != normalized_explicit_key:
                cleaned_team_key = None
        references = fetch_operation_board_references(
            entry_date,
            technician_names=normalized_selected_technicians or None,
        )
        order_lookup = {
            str(item["os_id"]): item
            for item in references["orders"]
            if item.get("os_id") is not None
        }
        global_lookup_cache: dict[str, dict[str, Any] | None] = {}

        cleaned_entries: list[dict[str, Any]] = []
        for raw in entries:
            slot_label = _clean_text(raw.get("slot_label"))
            os_id = _clean_text(raw.get("os_id"))
            raw_team_label = _clean_text(raw.get("team_label"))
            raw_technician_names = _clean_text(raw.get("technician_names"))
            if not slot_label and not raw_team_label and not os_id:
                continue

            order_ref = _get_order_reference(os_id, order_lookup, global_lookup_cache)
            subject_name = _clean_text(raw.get("subject_name")) or _pick(order_ref, "subject_name")
            branch_name = _clean_text(raw.get("branch_name")) or _pick(order_ref, "branch_name")
            customer_name = (
                _clean_text(raw.get("customer_name"))
                or _pick(order_ref, "customer_name")
                or _extract_customer_name_from_raw(
                    order_ref.get("raw_payload")
                    if isinstance(order_ref, dict) and isinstance(order_ref.get("raw_payload"), dict)
                    else {}
                )
            )
            technician_display = _resolve_technician_display(order_ref)
            technician_names = _prefer_meaningful_value(
                raw_technician_names,
                raw_team_label,
                technician_display,
            )
            team_label = _prefer_meaningful_value(
                raw_team_label,
                cleaned_team_name,
                technician_names,
                technician_display,
            )

            cleaned_entries.append(
                {
                    "slot_label": slot_label,
                    "team_label": team_label,
                    "os_id": os_id,
                    "subject_name": subject_name,
                    "branch_name": branch_name,
                    "customer_name": customer_name,
                    "technician_names": technician_names,
                    "opening_note": _clean_text(raw.get("opening_note")),
                    "occurrence_note": _clean_text(raw.get("occurrence_note")),
                    "comment_note": _clean_text(raw.get("comment_note")),
                    "start_at": _clean_text(raw.get("start_at")),
                    "displacement_at": _clean_text(raw.get("displacement_at")),
                    "executed_at": _clean_text(raw.get("executed_at")),
                    "finalized_at": _clean_text(raw.get("finalized_at")),
                    "contact_at": _clean_text(raw.get("contact_at")),
                    "status_label": _clean_text(raw.get("status_label")),
                }
            )

        if explicit_selected_technicians and cleaned_entries:
            selected_set = _normalize_technician_name_set(explicit_selected_technicians)
            invalid_entries: list[dict[str, str]] = []
            for index, entry in enumerate(cleaned_entries, start=1):
                if _entry_matches_selected_technicians(
                    entry,
                    selected_set,
                    order_lookup,
                    global_lookup_cache,
                ):
                    continue
                os_id = _clean_text(entry.get("os_id")) or "-"
                technician_label = _prefer_meaningful_value(
                    _clean_text(entry.get("technician_names")),
                    _clean_text(entry.get("team_label")),
                )
                if not technician_label and os_id != "-":
                    order_ref = _get_order_reference(os_id, order_lookup, global_lookup_cache)
                    technician_label = _resolve_technician_display(order_ref)
                invalid_entries.append(
                    {
                        "line": str(index),
                        "os_id": os_id,
                        "technician": technician_label or "Sem tecnico informado",
                    }
                )
            if invalid_entries:
                raise ValueError(
                    _build_selected_technician_mismatch_error(
                        explicit_selected_technicians,
                        invalid_entries,
                    )
                )

        if not normalized_selected_technicians and cleaned_entries:
            normalized_selected_technicians = _infer_selected_technicians_from_entries(cleaned_entries)

        upsert_operation_board_header(
            entry_date=entry_date,
            responsible_name=_clean_text(responsible_name),
            shift_label=_clean_text(shift_label),
            general_notes=_clean_text(general_notes),
            selected_technicians=normalized_selected_technicians,
            team_name=cleaned_team_name,
            team_key=cleaned_team_key,
        )
        replace_operation_board_entries(
            entry_date,
            cleaned_entries,
            team_name=cleaned_team_name,
            team_key=cleaned_team_key,
        )
        return self.get_board(
            target_date,
            team_name=cleaned_team_name,
            team_key=cleaned_team_key,
        )

    def save_entry_comment(self, entry_id: int, comment_note: str | None) -> dict[str, Any] | None:
        return update_operation_board_entry_comment(
            entry_id,
            _clean_text(comment_note),
        )

    def build_delay_report(
        self,
        target_date: date,
        *,
        entries_override: list[dict[str, Any]] | None = None,
        selected_technicians: list[str] | None = None,
        team_name: str | None = None,
        team_key: str | None = None,
        branch_name: str | None = None,
    ) -> dict[str, Any]:
        entry_date = str(target_date)
        cleaned_team_name = _clean_text(team_name)
        cleaned_team_key = _clean_text(team_key)
        cleaned_branch_name = _clean_text(branch_name)
        has_entries_override = entries_override is not None
        persisted_header = fetch_operation_board_header(
            entry_date,
            team_name=team_name if cleaned_team_key is None and team_name is not None else None,
            team_key=cleaned_team_key,
        ) or {}
        effective_team_key = normalize_operation_board_team_key(
            persisted_header.get("team_name"),
            team_key=_clean_text(persisted_header.get("team_key")) or cleaned_team_key,
        )
        stored_selected_technicians = _parse_selected_technicians(
            persisted_header.get("selected_technicians")
        )
        requested_selected = (
            _normalize_selected_technicians(selected_technicians)
            if selected_technicians is not None
            else None
        )
        if has_entries_override:
            effective_selected: list[str] = []
        else:
            effective_selected = (
                requested_selected
                if requested_selected is not None
                else _normalize_selected_technicians(stored_selected_technicians)
            )
        order_lookup: dict[str, dict[str, Any]] = {}
        global_lookup_cache: dict[str, dict[str, Any] | None] = {}

        if has_entries_override:
            source_entries = [
                _normalize_delay_entry(entry)
                for entry in entries_override or []
                if _is_delay_entry_meaningful(entry)
            ]
        else:
            references = fetch_operation_board_references(
                entry_date,
                technician_names=effective_selected or None,
            )
            order_lookup = {
                str(item["os_id"]): item
                for item in references["orders"]
                if item.get("os_id") is not None
            }
            source_entries = [
                _normalize_delay_entry(
                    _hydrate_entry(entry, order_lookup, global_lookup_cache)
                )
                for entry in fetch_operation_board_entries(entry_date, team_key=effective_team_key)
            ]

        if cleaned_branch_name:
            source_entries = [
                entry
                for entry in source_entries
                if _entry_matches_selected_branch(
                    entry,
                    cleaned_branch_name,
                    order_lookup,
                    global_lookup_cache,
                )
            ]

        if has_entries_override:
            effective_selected = _infer_selected_technicians_from_entries(source_entries)
        elif not effective_selected and source_entries:
            effective_selected = _infer_selected_technicians_from_entries(source_entries)

        if effective_selected and not has_entries_override:
            source_entries = [
                entry
                for entry in source_entries
                if _resolve_selected_technician_bucket(
                    entry,
                    effective_selected,
                    order_lookup,
                    global_lookup_cache,
                )
            ]

        grouped_entries: dict[str, list[dict[str, Any]]] = {}
        if has_entries_override:
            for entry in source_entries:
                technician_key = _resolve_entry_technician(entry)
                grouped_entries.setdefault(technician_key, []).append(entry)
        elif effective_selected:
            grouped_entries = {technician: [] for technician in effective_selected}
            for entry in source_entries:
                technician_key = _resolve_selected_technician_bucket(
                    entry,
                    effective_selected,
                    order_lookup,
                    global_lookup_cache,
                )
                if technician_key is None:
                    continue
                grouped_entries.setdefault(technician_key, []).append(entry)
        else:
            for entry in source_entries:
                technician_key = _resolve_entry_technician(entry)
                grouped_entries.setdefault(technician_key, []).append(entry)

        ordered_technicians = _delay_report_ordered_technicians(
            grouped_entries.keys(), effective_selected
        )

        technician_reports: list[dict[str, Any]] = []
        total_orders = 0
        total_delay_rows = 0
        total_delay_minutes = 0
        total_delay_minutes_known = 0

        for technician_name in ordered_technicians:
            raw_rows = grouped_entries.get(technician_name, [])
            rows = sorted(raw_rows, key=_delay_entry_sort_key)
            report_rows: list[dict[str, Any]] = []
            order_rows = 0
            delay_rows = 0
            delay_minutes_sum = 0
            delay_minutes_known = 0

            for row in rows:
                os_id = _clean_text(row.get("os_id"))
                is_delay = not bool(os_id)
                delay_minutes = _extract_delay_minutes(row) if is_delay else None
                if is_delay:
                    delay_rows += 1
                    if delay_minutes is not None:
                        delay_minutes_sum += delay_minutes
                        delay_minutes_known += 1
                else:
                    order_rows += 1

                report_rows.append(
                    {
                        "type": "atraso" if is_delay else "os",
                        "slot_label": _clean_text(row.get("slot_label")) or "",
                "os_id": os_id or "",
                "subject_name": _clean_text(row.get("subject_name")) or "",
                "branch_name": _clean_text(row.get("branch_name")) or "",
                "customer_name": _clean_text(row.get("customer_name")) or "",
                "technician_names": _clean_text(row.get("technician_names")) or technician_name,
                "start_at": _clean_text(row.get("start_at")) or "",
                "displacement_at": _clean_text(row.get("displacement_at")) or "",
                        "executed_at": _clean_text(row.get("executed_at")) or "",
                        "finalized_at": _clean_text(row.get("finalized_at")) or "",
                        "status_label": _clean_text(row.get("status_label")) or "",
                        "opening_note": _clean_text(row.get("opening_note")) or "",
                        "occurrence_note": _clean_text(row.get("occurrence_note")) or "",
                        "comment_note": _clean_text(row.get("comment_note")) or "",
                        "delay_minutes": delay_minutes,
                    }
                )

            total_orders += order_rows
            total_delay_rows += delay_rows
            total_delay_minutes += delay_minutes_sum
            total_delay_minutes_known += delay_minutes_known

            technician_reports.append(
                {
                    "technician": technician_name,
                    "orders_count": order_rows,
                    "delay_rows_count": delay_rows,
                    "delay_minutes_total": delay_minutes_sum if delay_minutes_known else None,
                    "delay_minutes_known_rows": delay_minutes_known,
                    "rows": report_rows,
                }
            )

        return {
            "date": entry_date,
            "generated_at": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
            "responsible_name": _clean_text(persisted_header.get("responsible_name")) or "",
            "shift_label": _clean_text(persisted_header.get("shift_label")) or "",
            "team_name": _clean_text(persisted_header.get("team_name")) or "",
            "team_key": effective_team_key,
            "selected_branch": cleaned_branch_name or "",
            "selected_technicians": effective_selected,
            "summary": {
                "technicians_count": len(technician_reports),
                "orders_count": total_orders,
                "delay_rows_count": total_delay_rows,
                "delay_minutes_total": total_delay_minutes if total_delay_minutes_known else None,
                "delay_minutes_known_rows": total_delay_minutes_known,
            },
            "technicians": technician_reports,
        }

    def list_saved_lists(self, target_date: date | None = None) -> list[dict[str, Any]]:
        return list_operation_board_teams(str(target_date) if target_date else None)

    def delete_board(
        self,
        target_date: date,
        *,
        team_name: str | None = None,
        team_key: str | None = None,
    ) -> dict[str, Any]:
        deleted = delete_operation_board(
            str(target_date),
            team_name=_clean_text(team_name),
            team_key=_clean_text(team_key),
        )
        return {
            "deleted": deleted,
            "saved_lists": self.list_saved_lists(),
        }


def _clean_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _pick(row: dict[str, Any] | None, key: str) -> str | None:
    if row is None:
        return None
    value = row.get(key)
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _resolve_technician_display(row: dict[str, Any] | None) -> str | None:
    if row is None:
        return None
    technician_name = _clean_text(row.get("technician_name"))
    if technician_name:
        return technician_name
    technician_id = _clean_text(row.get("technician_id"))
    if technician_id:
        return f"Tecnico ID {technician_id}"
    return None


def _prefer_meaningful_value(*values: str | None) -> str | None:
    for value in values:
        text = _clean_text(value)
        if not text or _is_unknown_placeholder(text):
            continue
        return text
    return None


def _is_unknown_placeholder(value: str) -> bool:
    normalized = value.strip().lower()
    return normalized in {
        "equipe nao informada",
        "sem tecnico",
        "sem tecnico no ixc",
        "nao informado",
    }


def _hydrate_entry(
    entry: dict[str, Any],
    order_lookup: dict[str, dict[str, Any]],
    global_lookup_cache: dict[str, dict[str, Any] | None],
) -> dict[str, Any]:
    hydrated = dict(entry)
    os_id = str(hydrated.get("os_id") or "").strip()
    order_ref = _get_order_reference(os_id, order_lookup, global_lookup_cache)
    technician_display = _resolve_technician_display(order_ref)
    technician_names = _prefer_meaningful_value(
        _clean_text(hydrated.get("technician_names")),
        _clean_text(hydrated.get("team_label")),
        technician_display,
    )
    team_label = _prefer_meaningful_value(
        _clean_text(hydrated.get("team_label")),
        technician_names,
        technician_display,
    )
    hydrated["team_label"] = team_label
    hydrated["technician_names"] = technician_names
    if not _clean_text(hydrated.get("subject_name")) and order_ref is not None:
        hydrated["subject_name"] = _pick(order_ref, "subject_name")
    if not _clean_text(hydrated.get("branch_name")) and order_ref is not None:
        hydrated["branch_name"] = _pick(order_ref, "branch_name")
    if not _clean_text(hydrated.get("sector_id")) and order_ref is not None:
        hydrated["sector_id"] = _pick(order_ref, "sector_id")
    if not _clean_text(hydrated.get("sector_name")) and order_ref is not None:
        hydrated["sector_name"] = _pick(order_ref, "sector_name")
    if not _clean_text(hydrated.get("customer_name")) and order_ref is not None:
        hydrated["customer_name"] = _resolve_customer_name(order_ref)
    if order_ref is not None:
        raw_payload = (
            order_ref.get("raw_payload") if isinstance(order_ref.get("raw_payload"), dict) else {}
        )
        opened_dt = _as_clock(_extract_order_opened_datetime(order_ref))
        displacement_dt = _as_clock(_extract_displacement_datetime(raw_payload, order_ref))
        execution_dt = _as_clock(_extract_order_execution_datetime(order_ref))
        closed_dt = _as_clock(_extract_order_closed_datetime(order_ref))
        forwarded_dt = _as_clock(_extract_forwarded_datetime(raw_payload))
        scheduled_start_dt = _as_clock(_extract_order_scheduled_start_datetime(order_ref))
        scheduled_end_dt = _as_clock(_extract_order_scheduled_end_datetime(order_ref))
        scheduled_dt = scheduled_start_dt or scheduled_end_dt
        has_progress = any(
            value is not None
            for value in (displacement_dt, execution_dt, closed_dt, forwarded_dt)
        )
        if forwarded_dt is not None and not any(
            value is not None for value in (displacement_dt, execution_dt, closed_dt)
        ):
            display_start_dt = forwarded_dt
        else:
            display_start_dt = (
                scheduled_dt if scheduled_dt is not None and not has_progress else (opened_dt or scheduled_dt)
            )
        hydrated["start_at"] = _format_time(display_start_dt)
        hydrated["displacement_at"] = _format_time(displacement_dt)
        hydrated["executed_at"] = _format_time(execution_dt)
        hydrated["finalized_at"] = _format_time(closed_dt)
        hydrated["status_label"] = _resolve_status_label(
            status_code=_extract_order_status_code(order_ref),
            displacement_dt=displacement_dt,
            execution_dt=execution_dt,
            closed_dt=closed_dt,
            scheduled_dt=scheduled_start_dt or scheduled_end_dt,
        )
    hydrated["os_exists_in_ixc"] = not os_id or order_ref is not None
    hydrated["os_validation_message"] = (
        None
        if hydrated["os_exists_in_ixc"]
        else "OS nao encontrada na sincronizacao atual do IXC."
    )
    return hydrated


def _get_order_reference(
    os_id: str | None,
    order_lookup: dict[str, dict[str, Any]],
    global_lookup_cache: dict[str, dict[str, Any] | None],
) -> dict[str, Any] | None:
    normalized = str(os_id or "").strip()
    if not normalized:
        return None
    from_day = order_lookup.get(normalized)
    if from_day is not None:
        return from_day
    if normalized in global_lookup_cache:
        return global_lookup_cache[normalized]
    fetched = fetch_order_by_os_id(normalized)
    global_lookup_cache[normalized] = fetched
    return fetched


def _build_suggested_entries(
    orders: list[dict[str, Any]],
    *,
    target_date: date,
    default_team_name: str | None = None,
    selected_technicians: list[str] | None = None,
) -> list[dict[str, Any]]:
    timeline_rows: list[tuple[datetime, str, str, dict[str, Any]]] = []
    grouped_orders: dict[str, list[dict[str, Any]]] = {}
    for order in orders:
        day_context = _resolve_order_day_context(order, target_date)
        if not day_context["is_relevant"]:
            continue
        technician_key = _resolve_technician_display(order) or "Sem tecnico no IXC"
        grouped_orders.setdefault(technician_key, []).append(order)

    selected_sequence = _normalize_selected_technicians(selected_technicians)
    ordered_technicians = _ordered_technicians(
        grouped_orders,
        selected_sequence,
        target_date=target_date,
    )
    technician_rank = {
        technician: index
        for index, technician in enumerate(ordered_technicians)
    }

    for technician_key in ordered_technicians:
        technician_orders = sorted(
            grouped_orders.get(technician_key, []),
            key=lambda order: _sort_order_key(order, target_date),
        )
        team_display = (
            technician_key
            if selected_sequence
            else _prefer_meaningful_value(default_team_name, technician_key)
        )
        if not technician_orders:
            placeholder = {
                "slot_label": DEFAULT_TIME_SLOTS[0],
                "team_label": team_display,
                "os_id": "",
                "subject_name": "",
                "branch_name": "",
                "customer_name": "",
                "technician_names": technician_key,
                "opening_note": "Sem OS executada para este tecnico no periodo selecionado.",
                "occurrence_note": "Use esta linha para registrar plantao, deslocamento ou justificativa.",
                "comment_note": "",
                "start_at": "",
                "displacement_at": "",
                "executed_at": "",
                "finalized_at": "",
                "contact_at": "",
                "status_label": "Sem OS",
            }
            timeline_rows.append((datetime(1900, 1, 1, 8, 0), technician_key, "", placeholder))
            continue

        previous_end: datetime | None = None
        for order in technician_orders:
            day_context = _resolve_order_day_context(order, target_date)
            if not day_context["is_relevant"]:
                continue
            opened_dt = day_context["opened_dt"]
            execution_dt = day_context["execution_dt"]
            closed_dt = day_context["closed_dt"]
            displacement_dt = day_context["displacement_dt"]
            forwarded_dt = day_context["forwarded_dt"]
            scheduled_start_dt = day_context["scheduled_start_dt"]
            scheduled_end_dt = day_context["scheduled_end_dt"]
            occurrence_message = _extract_occurrence_message(
                order.get("raw_payload") if isinstance(order.get("raw_payload"), dict) else {}
            )
            start_dt = day_context["start_dt"]
            end_dt = day_context["end_dt"]
            if (
                previous_end is not None
                and start_dt is not None
                and start_dt > previous_end
            ):
                gap_minutes = int((start_dt - previous_end).total_seconds() // 60)
                if gap_minutes >= GAP_MINUTES_FOR_OCCURRENCE:
                    gap_entry = _build_gap_occurrence_entry(
                        start_dt=previous_end,
                        end_dt=start_dt,
                        technician_display=technician_key,
                        team_display=team_display,
                        branch_name=_clean_text(order.get("branch_name")),
                    )
                    timeline_rows.append((previous_end, technician_key, "", gap_entry))

            slot_label = _slot_for_datetime(day_context["slot_dt"])
            if slot_label is None:
                slot_label = DEFAULT_TIME_SLOTS[0]

            opened_at = _format_time(day_context["display_start_dt"])
            displacement_at = _format_time(displacement_dt)
            execution_at = _format_time(execution_dt)
            closed_at = _format_time(closed_dt)
            os_id = _clean_text(order.get("os_id"))
            subject_name = _clean_text(order.get("subject_name"))
            customer_name = _resolve_customer_name(order)

            opening_parts: list[str] = []
            if os_id:
                opening_parts.append(f"ID: {os_id}")
            if customer_name:
                opening_parts.append(f"Cliente: {customer_name}")
            if subject_name:
                opening_parts.append(subject_name)
            opening_note = (
                " / ".join(opening_parts)
                if opening_parts
                else "OS coletada automaticamente via IXC."
            )

            occurrence_parts: list[str] = []
            if day_context["use_schedule_context"]:
                scheduled_start = _format_time(scheduled_start_dt or scheduled_end_dt)
                scheduled_end = _format_time(scheduled_end_dt)
                if scheduled_start and scheduled_end and scheduled_start != scheduled_end:
                    occurrence_parts.append(
                        f"Agenda IXC prevista entre {scheduled_start} e {scheduled_end}."
                    )
                elif scheduled_start:
                    occurrence_parts.append(f"Agenda IXC prevista para {scheduled_start}.")
            else:
                if displacement_at:
                    occurrence_parts.append(f"Trajeto realizado/Deslocamento {displacement_at}.")
                if execution_at:
                    occurrence_parts.append(f"Executada {execution_at}.")
                if closed_at:
                    occurrence_parts.append(f"Finalizada {closed_at}.")
                if forwarded_dt:
                    occurrence_parts.append(f"Encaminhada {_format_time(forwarded_dt)}.")
            if occurrence_message:
                occurrence_parts.append(occurrence_message)
            if not occurrence_parts:
                if day_context["use_schedule_context"]:
                    occurrence_parts.append("OS aguardando janela agendada no IXC.")
                else:
                    occurrence_parts.append("Aguardando inicio do atendimento.")

            row_data = {
                "slot_label": slot_label,
                "team_label": team_display,
                "os_id": os_id,
                "subject_name": subject_name,
                "branch_name": _clean_text(order.get("branch_name")),
                "customer_name": customer_name,
                "technician_names": technician_key,
                "opening_note": opening_note,
                "occurrence_note": " ".join(occurrence_parts),
                "comment_note": "",
                "start_at": opened_at,
                "displacement_at": displacement_at,
                "executed_at": execution_at,
                "finalized_at": closed_at,
                "contact_at": "",
                "status_label": day_context["status_label"],
            }
            timeline_dt = day_context["timeline_dt"]
            timeline_rows.append((timeline_dt or datetime.max, technician_key, os_id or "", row_data))
            previous_end = end_dt or start_dt or previous_end

    timeline_rows.sort(
        key=lambda item: (
            item[0],
            0 if item[2] else 1,
            technician_rank.get(item[1], len(technician_rank)),
            item[1],
            item[2],
        )
    )
    return [row for _, _, _, row in timeline_rows]


def _build_board_summary(
    orders: list[dict[str, Any]],
    entries: list[dict[str, Any]],
    *,
    target_date: date,
    has_saved_entries: bool,
) -> dict[str, Any]:
    technicians: set[str] = set()
    open_count = 0
    execution_count = 0
    closed_count = 0
    relevant_orders_count = 0

    for order in orders:
        day_context = _resolve_order_day_context(order, target_date)
        if not day_context["is_relevant"]:
            continue
        relevant_orders_count += 1
        technician_display = _resolve_technician_display(order)
        if technician_display:
            technicians.add(technician_display)
        if day_context["status_label"] == "Finalizada":
            closed_count += 1
        elif day_context["status_label"] in {"Em execucao", "Deslocamento"}:
            execution_count += 1
        else:
            open_count += 1

    return {
        "total_orders": relevant_orders_count,
        "open_orders": open_count,
        "execution_orders": execution_count,
        "closed_orders": closed_count,
        "technicians_identified": len(technicians),
        "entry_count": len(entries),
        "invalid_os_count": sum(
            1 for entry in entries if entry.get("os_exists_in_ixc") is False
        ),
        "has_saved_entries": has_saved_entries,
    }


def _extract_order_opened_datetime(order: dict[str, Any] | None) -> datetime | None:
    return _extract_order_datetime(
        order,
        row_keys=["opened_at"],
        raw_keys=[
            "data_abertura",
            "data_hora_abertura",
            "data_criacao",
            "abertura",
        ],
    )


def _extract_order_execution_datetime(order: dict[str, Any] | None) -> datetime | None:
    if not isinstance(order, dict):
        return None
    normalized_status = _normalize_status_token(_extract_order_status_code(order))
    if _is_scheduled_or_rescheduled_status(normalized_status):
        return None

    raw_payload = order.get("raw_payload") if isinstance(order.get("raw_payload"), dict) else {}
    row_execution = _parse_timestamp(order.get("execution_started_at"))
    if row_execution is not None:
        return row_execution

    return _extract_raw_execution_datetime(raw_payload)


def _extract_raw_execution_datetime(raw_payload: dict[str, Any]) -> datetime | None:
    if not raw_payload:
        return None
    for key in (
        "data_hora_execucao",
        "data_inicio_execucao",
        "inicio_execucao",
        "data_inicio",
        "data_final",
        "data_fechamento",
    ):
        parsed = _parse_timestamp(raw_payload.get(key))
        if parsed is not None:
            return parsed
    return None


def _extract_order_completion_datetime(order: dict[str, Any] | None) -> datetime | None:
    return _extract_order_datetime(
        order,
        row_keys=[],
        raw_keys=[
            "data_final",
            "data_fechamento",
        ],
    )


def _extract_order_closed_datetime(order: dict[str, Any] | None) -> datetime | None:
    if not isinstance(order, dict):
        return None
    raw_payload = order.get("raw_payload") if isinstance(order.get("raw_payload"), dict) else {}
    candidates = [
        _parse_timestamp(order.get("closed_at")),
        _parse_timestamp(raw_payload.get("data_fechamento")),
        _parse_timestamp(raw_payload.get("data_encerramento")),
        _parse_timestamp(raw_payload.get("data_finalizacao")),
        _parse_timestamp(raw_payload.get("data_final")),
        _parse_timestamp(raw_payload.get("fechamento")),
        _extract_finalized_datetime(raw_payload),
    ]
    return _max_datetime(candidates)


def _extract_order_scheduled_start_datetime(order: dict[str, Any] | None) -> datetime | None:
    direct = _extract_order_datetime(
        order,
        row_keys=[],
        raw_keys=[
            "data_agenda",
            "data_agendamento",
            "data_agenda_inicial",
            "data_agendamento_inicial",
            "data_hora_agenda",
            "data_hora_agendamento",
            "data_reagendamento",
            "data_hora_reagendamento",
            "agendada_para",
            "previsao_inicio",
            "dt_agendamento",
        ],
    )
    if direct is not None:
        return direct
    raw_payload = order.get("raw_payload") if isinstance(order.get("raw_payload"), dict) else {}
    return _extract_scheduled_datetime_from_text(raw_payload)


def _extract_order_scheduled_end_datetime(order: dict[str, Any] | None) -> datetime | None:
    return _extract_order_datetime(
        order,
        row_keys=[],
        raw_keys=[
            "data_agenda_final",
            "data_agendamento_final",
            "data_hora_agenda_final",
            "data_hora_agendamento_final",
            "data_previsao_finalizacao",
            "previsao_fim",
            "dt_previsao",
        ],
    )


def _extract_order_datetime(
    order: dict[str, Any] | None,
    *,
    row_keys: list[str],
    raw_keys: list[str],
) -> datetime | None:
    if not isinstance(order, dict):
        return None
    for key in row_keys:
        parsed = _parse_timestamp(order.get(key))
        if parsed is not None:
            return parsed
    raw_payload = order.get("raw_payload") if isinstance(order.get("raw_payload"), dict) else {}
    for key in raw_keys:
        parsed = _parse_timestamp(raw_payload.get(key))
        if parsed is not None:
            return parsed
    return None


def _sort_order_key(order: dict[str, Any], target_date: date | None = None) -> tuple[datetime, str]:
    if target_date is not None:
        day_context = _resolve_order_day_context(order, target_date)
        base_dt = day_context["timeline_dt"]
    else:
        execution_dt = _as_clock(_extract_order_execution_datetime(order))
        opened_dt = _as_clock(_extract_order_opened_datetime(order))
        closed_dt = _as_clock(_extract_order_closed_datetime(order))
        base_dt = execution_dt or opened_dt or closed_dt or datetime.max
    return base_dt, str(order.get("os_id") or "")


def _slot_for_datetime(value: datetime | None) -> str | None:
    if value is None:
        return None
    hour = value.hour
    if hour < 8:
        return DEFAULT_TIME_SLOTS[0]
    if hour >= 19:
        return DEFAULT_TIME_SLOTS[-1]
    slot_index = max(0, min(len(DEFAULT_TIME_SLOTS) - 1, hour - 8))
    return DEFAULT_TIME_SLOTS[slot_index]


def _parse_timestamp(value: Any) -> datetime | None:
    text = _clean_text(value)
    if not text:
        return None
    normalized = text.replace("T", " ").replace("Z", "")
    for fmt in (
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S.%f",
        "%Y-%m-%d %H:%M",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y %H:%M",
        "%H:%M:%S",
        "%H:%M",
    ):
        try:
            return datetime.strptime(normalized, fmt)
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).replace(tzinfo=None)
    except ValueError:
        return None


def _as_clock(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    return datetime(1900, 1, 1, value.hour, value.minute, value.second, value.microsecond)


def _format_time(value: datetime | None) -> str:
    if value is None:
        return ""
    return value.strftime("%H:%M")


def _resolve_status_label(
    *,
    status_code: str | None = None,
    displacement_dt: datetime | None = None,
    execution_dt: datetime | None = None,
    closed_dt: datetime | None = None,
    scheduled_dt: datetime | None = None,
) -> str:
    normalized_status = _normalize_status_token(status_code)
    if closed_dt:
        return "Finalizada"
    if _is_rescheduled_status(normalized_status):
        return "Reagendada"
    if _is_forwarded_status(normalized_status):
        return "Encaminhada"
    if normalized_status in {"AG", "AGENDA", "AGENDADA", "PENDENTE"}:
        return "Agendada" if scheduled_dt else "Aberta"
    if execution_dt:
        return "Em execucao"
    if displacement_dt:
        return "Deslocamento"
    if normalized_status in {"DS", "DESLOCAMENTO", "EM_DESLOCAMENTO"}:
        return "Deslocamento"
    if normalized_status in {"EX", "EN", "E", "EM_EXECUCAO", "EM_ANDAMENTO"}:
        return "Em execucao"
    if normalized_status in {"F", "FINALIZADA", "CONCLUIDA"}:
        return "Finalizada"
    if normalized_status in {"C", "CA", "AN", "CANCELADA", "CANCELADO", "ANULADA"}:
        return "Cancelada"
    if scheduled_dt:
        return "Agendada"
    return "Aberta"


def _resolve_order_day_context(order: dict[str, Any], target_date: date) -> dict[str, Any]:
    raw_payload = order.get("raw_payload") if isinstance(order.get("raw_payload"), dict) else {}
    opened_full = _extract_order_opened_datetime(order)
    displacement_full = _extract_displacement_datetime(raw_payload, order)
    execution_full = _extract_order_execution_datetime(order)
    closed_full = _extract_order_closed_datetime(order)
    forwarded_full = _extract_forwarded_datetime(raw_payload)
    scheduled_start_full = _extract_order_scheduled_start_datetime(order)
    scheduled_end_full = _extract_order_scheduled_end_datetime(order)

    opened_dt = _as_clock(opened_full) if _matches_target_date(opened_full, target_date) else None
    displacement_dt = (
        _as_clock(displacement_full) if _matches_target_date(displacement_full, target_date) else None
    )
    execution_dt = (
        _as_clock(execution_full) if _matches_target_date(execution_full, target_date) else None
    )
    closed_dt = _as_clock(closed_full) if _matches_target_date(closed_full, target_date) else None
    if execution_dt is None and closed_dt is not None:
        completion_full = _extract_order_completion_datetime(order)
        execution_dt = (
            _as_clock(completion_full)
            if _matches_target_date(completion_full, target_date)
            else closed_dt
        )
    forwarded_dt = _as_clock(forwarded_full) if _matches_target_date(forwarded_full, target_date) else None
    if displacement_dt is None and forwarded_dt is not None:
        displacement_dt = forwarded_dt
    if execution_dt is None and closed_dt is None and forwarded_dt is not None:
        execution_dt = forwarded_dt
    scheduled_start_dt = (
        _as_clock(scheduled_start_full)
        if _matches_target_date(scheduled_start_full, target_date)
        else None
    )
    scheduled_end_dt = (
        _as_clock(scheduled_end_full)
        if _matches_target_date(scheduled_end_full, target_date)
        else None
    )
    if closed_full is not None and target_date > closed_full.date():
        # Quando a OS ja foi finalizada, nao deve reaparecer em dias posteriores
        # apenas por causa de janela de agenda residual no payload.
        scheduled_start_dt = None
        scheduled_end_dt = None

    has_schedule_window = scheduled_start_dt is not None or scheduled_end_dt is not None
    has_progress_activity = (
        displacement_dt is not None
        or execution_dt is not None
        or closed_dt is not None
        or forwarded_dt is not None
    )
    use_schedule_context = has_schedule_window and not has_progress_activity

    if use_schedule_context:
        start_dt, end_dt = _resolve_scheduled_window(
            scheduled_start_at=scheduled_start_dt,
            scheduled_end_at=scheduled_end_dt,
        )
        display_start_dt = scheduled_start_dt or scheduled_end_dt
    else:
        start_dt, end_dt = _resolve_order_window(
            opened_at=opened_dt,
            displacement_at=displacement_dt,
            execution_started_at=execution_dt,
            closed_at=closed_dt,
        )
        if start_dt is None and forwarded_dt is not None:
            start_dt = forwarded_dt
        if end_dt is None and forwarded_dt is not None:
            end_dt = forwarded_dt
        if start_dt is None and has_schedule_window:
            start_dt = scheduled_start_dt or scheduled_end_dt
            if end_dt is not None and start_dt is not None and end_dt < start_dt:
                start_dt = end_dt
        display_start_dt = (
            forwarded_dt
            or opened_dt
            or start_dt
            or scheduled_start_dt
            or scheduled_end_dt
        )

    slot_dt = (
        start_dt
        or execution_dt
        or displacement_dt
        or closed_dt
        or forwarded_dt
        or scheduled_start_dt
        or scheduled_end_dt
        or opened_dt
    )
    timeline_dt = slot_dt or end_dt or datetime.max
    status_label = _resolve_status_label(
        status_code=_extract_order_status_code(order),
        displacement_dt=None if use_schedule_context else displacement_dt,
        execution_dt=None if use_schedule_context else execution_dt,
        closed_dt=None if use_schedule_context else closed_dt,
        scheduled_dt=scheduled_start_dt or scheduled_end_dt,
    )
    is_relevant = any(
        value is not None
        for value in (
            opened_dt,
            displacement_dt,
            execution_dt,
            closed_dt,
            forwarded_dt,
            scheduled_start_dt,
            scheduled_end_dt,
        )
    )
    return {
        "is_relevant": is_relevant,
        "use_schedule_context": use_schedule_context,
        "opened_dt": opened_dt,
        "displacement_dt": displacement_dt,
        "execution_dt": execution_dt,
        "closed_dt": closed_dt,
        "forwarded_dt": forwarded_dt,
        "scheduled_start_dt": scheduled_start_dt,
        "scheduled_end_dt": scheduled_end_dt,
        "start_dt": start_dt,
        "end_dt": end_dt,
        "display_start_dt": display_start_dt,
        "slot_dt": slot_dt,
        "timeline_dt": timeline_dt,
        "status_label": status_label,
    }


def _extract_order_status_code(order: dict[str, Any] | None) -> str | None:
    if not isinstance(order, dict):
        return None
    raw_payload = order.get("raw_payload") if isinstance(order.get("raw_payload"), dict) else {}
    direct_status = _clean_text(order.get("status"))
    if direct_status:
        if (
            _normalize_status_token(direct_status) == "EN"
            and _extract_forwarded_datetime(raw_payload) is not None
        ):
            return "ENCAMINHADA"
        return direct_status
    for key in ("status", "status_os", "status_texto"):
        text = _clean_text(raw_payload.get(key))
        if text:
            if (
                _normalize_status_token(text) == "EN"
                and _extract_forwarded_datetime(raw_payload) is not None
            ):
                return "ENCAMINHADA"
            return text
    return None


def _normalize_status_token(value: Any) -> str:
    text = _clean_text(value)
    if not text:
        return ""
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = "".join(char for char in normalized if not unicodedata.combining(char))
    return re.sub(r"[^A-Z0-9]+", "_", ascii_text.upper()).strip("_")


def _is_rescheduled_status(token: str) -> bool:
    return token in {"R", "REAGENDADA", "REAGENDADO", "REAGENDAMENTO"}


def _is_forwarded_status(token: str) -> bool:
    return token in {"ENCAMINHADA", "ENCAMINHADO", "ENCAMINHAMENTO", "ENCAMINHAR"}


def _is_scheduled_or_rescheduled_status(token: str) -> bool:
    return (
        token in {"AG", "AGENDA", "AGENDADA", "PENDENTE"}
        or _is_rescheduled_status(token)
        or _is_forwarded_status(token)
    )


def _normalize_status_filter_key(value: Any) -> str:
    token = _normalize_status_token(value)
    if not token:
        return ""
    aliases = {
        "AGUARDANDO": "AGUARDANDO",
        "AGUARDANDO_RELATO": "AGUARDANDO",
        "ABERTA": "ABERTA",
        "ABERTO": "ABERTA",
        "PENDENTE": "ABERTA",
        "AGENDADA": "AGENDADA",
        "AGENDA": "AGENDADA",
        "AG": "AGENDADA",
        "ENCAMINHADA": "ENCAMINHADA",
        "ENCAMINHADO": "ENCAMINHADA",
        "ENCAMINHAMENTO": "ENCAMINHADA",
        "ENCAMINHAR": "ENCAMINHADA",
        "REAGENDADA": "REAGENDADA",
        "REAGENDADO": "REAGENDADA",
        "REAGENDAMENTO": "REAGENDADA",
        "R": "REAGENDADA",
        "DESLOCAMENTO": "DESLOCAMENTO",
        "EM_DESLOCAMENTO": "DESLOCAMENTO",
        "DS": "DESLOCAMENTO",
        "EM_EXECUCAO": "EM_EXECUCAO",
        "EM_ANDAMENTO": "EM_EXECUCAO",
        "EXECUCAO": "EM_EXECUCAO",
        "EX": "EM_EXECUCAO",
        "EN": "EM_EXECUCAO",
        "E": "EM_EXECUCAO",
        "FINALIZADA": "FINALIZADA",
        "CONCLUIDA": "FINALIZADA",
        "F": "FINALIZADA",
        "CANCELADA": "CANCELADA",
        "CANCELADO": "CANCELADA",
        "ANULADA": "CANCELADA",
        "AN": "CANCELADA",
        "C": "CANCELADA",
        "CA": "CANCELADA",
    }
    return aliases.get(token, "")


def _status_filter_display_label(key: str) -> str:
    return _STATUS_FILTER_LABELS.get(key, "")


def _normalize_selected_status_filters(values: list[str] | None) -> list[str]:
    if not values:
        return []
    normalized: list[str] = []
    seen_keys: set[str] = set()
    for raw in values:
        text = _clean_text(raw)
        if not text:
            continue
        key = _normalize_status_filter_key(text)
        if not key or key in seen_keys:
            continue
        label = _status_filter_display_label(key)
        if not label:
            continue
        seen_keys.add(key)
        normalized.append(label)
    return normalized


def _normalize_status_filter_set(values: list[str] | None) -> set[str]:
    if not values:
        return set()
    return {
        key
        for key in (_normalize_status_filter_key(value) for value in values)
        if key
    }


def _status_filter_keys_from_status_label(status_label: Any) -> set[str]:
    token = _normalize_status_token(status_label)
    keys: set[str] = set()
    if token in {"AGUARDANDO", "AGUARDANDO_RELATO"}:
        keys.add("AGUARDANDO")
    elif token in {"ABERTA", "PENDENTE"}:
        keys.update({"ABERTA", "AGUARDANDO"})
    elif token in {"AGENDADA", "AGENDA", "AG"}:
        keys.add("AGENDADA")
    elif _is_forwarded_status(token):
        keys.add("ENCAMINHADA")
    elif _is_rescheduled_status(token):
        keys.add("REAGENDADA")
    elif token in {"DESLOCAMENTO", "EM_DESLOCAMENTO", "DS"}:
        keys.add("DESLOCAMENTO")
    elif token in {"EM_EXECUCAO", "EM_ANDAMENTO", "EXECUCAO", "EX", "EN", "E"}:
        keys.add("EM_EXECUCAO")
    elif token in {"FINALIZADA", "CONCLUIDA", "F"}:
        keys.add("FINALIZADA")
    elif token in {"CANCELADA", "CANCELADO", "ANULADA", "C", "CA", "AN"}:
        keys.add("CANCELADA")
    return keys


def _status_filter_keys_from_status_code(status_code: Any) -> set[str]:
    token = _normalize_status_token(status_code)
    keys: set[str] = set()
    if token in {"AG", "AGENDA", "AGENDADA"}:
        keys.add("AGENDADA")
    elif _is_forwarded_status(token):
        keys.add("ENCAMINHADA")
    elif _is_rescheduled_status(token):
        keys.add("REAGENDADA")
    elif token in {"PENDENTE", "ABERTA", "ABERTO"}:
        keys.update({"ABERTA", "AGUARDANDO"})
    elif token in {"DS", "DESLOCAMENTO", "EM_DESLOCAMENTO"}:
        keys.add("DESLOCAMENTO")
    elif token in {"EX", "EN", "E", "EM_EXECUCAO", "EM_ANDAMENTO"}:
        keys.add("EM_EXECUCAO")
    elif token in {"F", "FINALIZADA", "CONCLUIDA"}:
        keys.add("FINALIZADA")
    elif token in {"C", "CA", "AN", "CANCELADA", "CANCELADO", "ANULADA"}:
        keys.add("CANCELADA")
    return keys


def _order_status_filter_keys(order: dict[str, Any], *, target_date: date) -> set[str]:
    day_context = _resolve_order_day_context(order, target_date)
    if not day_context.get("is_relevant"):
        return set()
    keys = _status_filter_keys_from_status_label(day_context.get("status_label"))
    keys.update(_status_filter_keys_from_status_code(_extract_order_status_code(order)))
    return keys


def _order_matches_selected_statuses(
    order: dict[str, Any],
    *,
    target_date: date,
    selected_statuses: set[str],
) -> bool:
    if not selected_statuses:
        return True
    return bool(_order_status_filter_keys(order, target_date=target_date) & selected_statuses)


def _entry_status_filter_keys(
    entry: dict[str, Any],
    *,
    target_date: date,
    order_lookup: dict[str, dict[str, Any]],
    global_lookup_cache: dict[str, dict[str, Any] | None],
) -> set[str]:
    keys = _status_filter_keys_from_status_label(entry.get("status_label"))
    os_id = _clean_text(entry.get("os_id"))
    if os_id:
        order_ref = _get_order_reference(os_id, order_lookup, global_lookup_cache)
        if order_ref:
            keys.update(_order_status_filter_keys(order_ref, target_date=target_date))
    if not keys:
        if _clean_text(entry.get("finalized_at")):
            keys.add("FINALIZADA")
        elif _clean_text(entry.get("executed_at")):
            keys.add("EM_EXECUCAO")
        elif _clean_text(entry.get("displacement_at")):
            keys.add("DESLOCAMENTO")
        elif _normalize_status_token(entry.get("status_label")) in {"ABERTA", "AGUARDANDO"}:
            keys.update({"ABERTA", "AGUARDANDO"})
    return keys


def _entry_matches_selected_statuses(
    entry: dict[str, Any],
    *,
    target_date: date,
    selected_statuses: set[str],
    order_lookup: dict[str, dict[str, Any]],
    global_lookup_cache: dict[str, dict[str, Any] | None],
) -> bool:
    if not selected_statuses:
        return True
    return bool(
        _entry_status_filter_keys(
            entry,
            target_date=target_date,
            order_lookup=order_lookup,
            global_lookup_cache=global_lookup_cache,
        )
        & selected_statuses
    )


def _collect_available_status_filters(
    orders: list[dict[str, Any]],
    *,
    target_date: date,
) -> list[str]:
    keys: set[str] = set()
    for order in orders:
        keys.update(_order_status_filter_keys(order, target_date=target_date))
    ordered: list[str] = []
    for key in _STATUS_FILTER_ORDER:
        if key in keys:
            label = _status_filter_display_label(key)
            if label:
                ordered.append(label)
    return ordered


def _matches_target_date(value: datetime | None, target_date: date) -> bool:
    return value is not None and value.date() == target_date


def _parse_selected_technicians(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        raw_values = value
    else:
        raw = str(value).strip()
        if not raw:
            return []
        try:
            parsed = json.loads(raw)
            raw_values = parsed if isinstance(parsed, list) else [raw]
        except json.JSONDecodeError:
            raw_values = raw.split(",")
    normalized: list[str] = []
    seen: set[str] = set()
    for item in raw_values:
        text = _clean_text(item)
        if not text or text == "__all__" or text in seen:
            continue
        seen.add(text)
        normalized.append(text)
    return normalized


def _normalize_selected_technicians(values: list[str] | None) -> list[str]:
    if not values:
        return []
    normalized: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = _clean_text(value)
        if not text or text == "__all__" or text in seen:
            continue
        seen.add(text)
        normalized.append(text)
    return normalized


def _same_selection(left: list[str], right: list[str]) -> bool:
    return sorted(set(left)) == sorted(set(right))


def _infer_selected_technicians_from_entries(entries: list[dict[str, Any]]) -> list[str]:
    inferred: list[str] = []
    seen: set[str] = set()
    for entry in entries:
        raw_value = _prefer_meaningful_value(
            _clean_text(entry.get("technician_names")),
            _clean_text(entry.get("team_label")),
        )
        if not raw_value:
            continue
        fragments = re.split(r"[,;/|]", raw_value)
        for fragment in fragments:
            text = _clean_text(fragment)
            if not text or _is_unknown_placeholder(text) or text in seen:
                continue
            seen.add(text)
            inferred.append(text)
    return inferred


def _extract_displacement_datetime(
    raw_payload: dict[str, Any],
    row: dict[str, Any] | None = None,
) -> datetime | None:
    if isinstance(row, dict):
        normalized_status = _normalize_status_token(_extract_order_status_code(row))
        if _is_scheduled_or_rescheduled_status(normalized_status):
            return None

    def _first_valid(keys: list[str]) -> datetime | None:
        for source in (raw_payload or {}, row or {}):
            for key in keys:
                parsed = _parse_timestamp(source.get(key))
                if parsed is not None:
                    return parsed
        return None

    explicit_displacement_keys = [
        "data_hora_encaminhado",
        "data_encaminhado",
        "data_hora_deslocamento",
        "data_deslocamento",
        "hora_deslocamento",
        "data_hora_saida",
        "data_saida",
        "hora_saida",
        "inicio_deslocamento",
    ]

    explicit_displacement = _first_valid(explicit_displacement_keys)
    if explicit_displacement is not None:
        return explicit_displacement

    message_displacement = _extract_message_event_datetime(
        raw_payload,
        status_tokens={"DS", "DESLOCAMENTO", "EM_DESLOCAMENTO"},
        text_patterns=("deslocamento", "trajeto realizado"),
    )
    if message_displacement is not None:
        return message_displacement

    # In some IXC bases, data_inicio represents "inicio de deslocamento".
    # Only infer displacement from this field when it is meaningfully earlier
    # than execution start; otherwise keep empty to avoid fictitious times.
    inferred_start = _first_valid(["data_inicio"])
    if inferred_start is None:
        return None

    execution_reference = _first_valid(
        [
            "data_hora_execucao",
            "data_inicio_execucao",
        ]
    )
    closed_reference = _first_valid(
        [
            "data_fechamento",
            "data_final",
            "data_finalizacao",
        ]
    )
    end_reference = execution_reference or closed_reference
    if end_reference is None:
        return inferred_start

    delta_minutes = (end_reference - inferred_start).total_seconds() / 60
    if 0 <= delta_minutes <= 12 * 60:
        return inferred_start

    return None


def _extract_message_event_datetime(
    raw_payload: dict[str, Any],
    *,
    status_tokens: set[str],
    text_patterns: tuple[str, ...],
) -> datetime | None:
    messages = raw_payload.get("_ixc_messages") if raw_payload else None
    if not isinstance(messages, list):
        return None
    normalized_patterns = tuple(_normalize_matching_text(pattern) for pattern in text_patterns)
    latest: datetime | None = None
    for item in messages:
        if not isinstance(item, dict):
            continue
        status = _normalize_status_token(item.get("status"))
        text = _normalize_matching_text(
            " ".join(
                _clean_text(item.get(key)) or ""
                for key in ("mensagem", "historico")
            )
        )
        if status not in status_tokens and not any(pattern in text for pattern in normalized_patterns):
            continue
        parsed = _parse_timestamp(item.get("data"))
        if parsed is None:
            continue
        if latest is None or parsed > latest:
            latest = parsed
    return latest


def _extract_forwarded_datetime(raw_payload: dict[str, Any]) -> datetime | None:
    if not raw_payload:
        return None
    direct_value = _extract_message_event_datetime(
        raw_payload,
        status_tokens={"EN", "ENCAMINHADA", "ENCAMINHADO"},
        text_patterns=("encaminh",),
    )
    return direct_value


def _extract_finalized_datetime(raw_payload: dict[str, Any]) -> datetime | None:
    if not raw_payload:
        return None
    return _extract_message_event_datetime(
        raw_payload,
        status_tokens={"F", "FINALIZADA", "CONCLUIDA"},
        text_patterns=("finaliz", "conclu"),
    )


def _max_datetime(values: list[datetime | None]) -> datetime | None:
    valid = [item for item in values if item is not None]
    if not valid:
        return None
    return max(valid)


def _extract_occurrence_message(raw_payload: dict[str, Any]) -> str | None:
    if not raw_payload:
        return None
    keys = [
        "mensagem_resposta",
        "relato_tecnico",
        "mensagem_tecnico",
        "relato",
        "mensagem",
        "descricao_ocorrencia",
        "descricao_final",
        "solucao",
        "observacao",
        "observacoes",
    ]
    for key in keys:
        value = raw_payload.get(key)
        text = _clean_text(value)
        if text:
            return text
    return None


def _extract_scheduled_datetime_from_text(raw_payload: dict[str, Any]) -> datetime | None:
    if not raw_payload:
        return None
    text_keys = [
        "mensagem_resposta",
        "relato_tecnico",
        "mensagem_tecnico",
        "relato",
        "mensagem",
        "descricao_ocorrencia",
        "descricao_final",
        "solucao",
        "observacao",
        "observacoes",
        "historico",
    ]
    patterns = [
        re.compile(
            r"agendad[ao].{0,50}?(\d{2}/\d{2}/\d{4}).{0,20}?(\d{2}:\d{2})",
            flags=re.IGNORECASE,
        ),
        re.compile(
            r"reagendad[ao].{0,50}?(\d{2}/\d{2}/\d{4}).{0,20}?(\d{2}:\d{2})",
            flags=re.IGNORECASE,
        ),
    ]
    for key in text_keys:
        text = _clean_text(raw_payload.get(key))
        if not text:
            continue
        for pattern in patterns:
            match = pattern.search(text)
            if not match:
                continue
            parsed = _parse_timestamp(f"{match.group(1)} {match.group(2)}")
            if parsed is not None:
                return parsed
    return None


def _extract_customer_name_from_raw(raw_payload: dict[str, Any]) -> str | None:
    if not raw_payload:
        return None
    keys = [
        "cliente",
        "nome_cliente",
        "cliente_nome",
        "razao",
        "razao_social",
        "nome_razao",
        "nome_fantasia",
        "fantasia",
        "apelido",
        "assinante",
    ]
    for key in keys:
        value = raw_payload.get(key)
        text = _clean_text(value)
        if text and text.lower() not in {"null", "none"}:
            return text
    return None


def _resolve_customer_name(order_ref: dict[str, Any] | None) -> str | None:
    if not isinstance(order_ref, dict):
        return None
    raw_payload = order_ref.get("raw_payload") if isinstance(order_ref.get("raw_payload"), dict) else {}
    return (
        _pick(order_ref, "customer_name")
        or _extract_customer_name_from_raw(raw_payload)
        or fetch_customer_name_by_customer_id(_pick(order_ref, "customer_id") or "")
    )


def _ordered_technicians(
    grouped_orders: dict[str, list[dict[str, Any]]],
    selected_sequence: list[str],
    *,
    target_date: date | None = None,
) -> list[str]:
    if selected_sequence:
        ordered: list[str] = []
        seen: set[str] = set()
        for name in selected_sequence:
            normalized = _clean_text(name)
            if not normalized or normalized in seen:
                continue
            seen.add(normalized)
            ordered.append(normalized)
        for key in grouped_orders.keys():
            normalized = _clean_text(key)
            if not normalized or normalized in seen:
                continue
            seen.add(normalized)
            ordered.append(normalized)
        return ordered

    def _first_order_dt(name: str) -> datetime:
        orders = grouped_orders.get(name, [])
        if not orders:
            return datetime.max
        first = min(orders, key=lambda order: _sort_order_key(order, target_date))
        return _sort_order_key(first, target_date)[0]

    return sorted(grouped_orders.keys(), key=lambda name: (_first_order_dt(name), name))


def _resolve_order_window(
    *,
    opened_at: datetime | None,
    displacement_at: datetime | None,
    execution_started_at: datetime | None,
    closed_at: datetime | None,
) -> tuple[datetime | None, datetime | None]:
    start_candidates = [opened_at, displacement_at, execution_started_at]
    end_candidates = [closed_at, execution_started_at, displacement_at, opened_at]
    start_dt = next((value for value in start_candidates if value is not None), None)
    end_dt = next((value for value in end_candidates if value is not None), None)
    if start_dt is not None and end_dt is not None and end_dt < start_dt:
        end_dt = start_dt
    return start_dt, end_dt


def _resolve_scheduled_window(
    *,
    scheduled_start_at: datetime | None,
    scheduled_end_at: datetime | None,
) -> tuple[datetime | None, datetime | None]:
    start_dt = scheduled_start_at or scheduled_end_at
    end_dt = scheduled_end_at or scheduled_start_at
    if start_dt is not None and end_dt is not None and end_dt < start_dt:
        end_dt = start_dt
    return start_dt, end_dt


def _build_gap_occurrence_entry(
    *,
    start_dt: datetime,
    end_dt: datetime,
    technician_display: str,
    team_display: str | None,
    branch_name: str | None,
) -> dict[str, Any]:
    gap_minutes = max(0, int((end_dt - start_dt).total_seconds() // 60))
    slot_label = _slot_for_datetime(start_dt) or DEFAULT_TIME_SLOTS[0]
    gap_start = _format_time(start_dt)
    gap_end = _format_time(end_dt)
    return {
        "slot_label": slot_label,
        "team_label": _prefer_meaningful_value(team_display, technician_display),
        "os_id": "",
        "subject_name": "",
        "branch_name": branch_name,
        "customer_name": "",
        "technician_names": technician_display,
        "opening_note": "Intervalo sem OS registrada.",
        "occurrence_note": (
            f"Janela sem execucao entre {gap_start} e {gap_end} "
            f"({gap_minutes} min). Registrar justificativa operacional."
        ),
        "comment_note": "",
        "start_at": gap_start,
        "displacement_at": "",
        "executed_at": "",
        "finalized_at": "",
        "contact_at": "",
        "status_label": "Aguardando relato",
    }


def _is_delay_entry_meaningful(entry: dict[str, Any]) -> bool:
    return any(
        _clean_text(entry.get(field))
        for field in (
            "slot_label",
            "team_label",
            "technician_names",
            "os_id",
            "opening_note",
            "occurrence_note",
            "comment_note",
            "start_at",
            "displacement_at",
            "executed_at",
            "finalized_at",
            "status_label",
        )
    )


def _normalize_delay_entry(entry: dict[str, Any]) -> dict[str, Any]:
    return {
        "slot_label": _clean_text(entry.get("slot_label")) or "",
        "team_label": _clean_text(entry.get("team_label")) or "",
        "os_id": _clean_text(entry.get("os_id")) or "",
        "subject_name": _clean_text(entry.get("subject_name")) or "",
        "branch_name": _clean_text(entry.get("branch_name")) or "",
        "customer_name": _clean_text(entry.get("customer_name")) or "",
        "technician_names": _clean_text(entry.get("technician_names")) or "",
        "opening_note": _clean_text(entry.get("opening_note")) or "",
        "occurrence_note": _clean_text(entry.get("occurrence_note")) or "",
        "comment_note": _clean_text(entry.get("comment_note")) or "",
        "start_at": _clean_text(entry.get("start_at")) or "",
        "displacement_at": _clean_text(entry.get("displacement_at")) or "",
        "executed_at": _clean_text(entry.get("executed_at")) or "",
        "finalized_at": _clean_text(entry.get("finalized_at")) or "",
        "status_label": _clean_text(entry.get("status_label")) or "",
    }


def _resolve_entry_technician(entry: dict[str, Any]) -> str:
    return (
        _prefer_meaningful_value(
            _clean_text(entry.get("technician_names")),
            _clean_text(entry.get("team_label")),
        )
        or "Sem tecnico informado"
    )


def _entry_matches_technician(entry: dict[str, Any], selected: list[str]) -> bool:
    technician = _resolve_entry_technician(entry)
    selected_set = {item.strip() for item in selected if item.strip()}
    return technician in selected_set


def _resolve_selected_technician_bucket(
    entry: dict[str, Any],
    selected: list[str],
    order_lookup: dict[str, dict[str, Any]],
    global_lookup_cache: dict[str, dict[str, Any] | None],
) -> str | None:
    selected_map = {
        _normalize_technician_name(name): name
        for name in selected
        if _normalize_technician_name(name)
    }
    if not selected_map:
        return None

    candidate_names: list[str] = []
    for field in ("technician_names", "team_label"):
        candidate_names.extend(
            _extract_technician_name_fragments(_clean_text(entry.get(field)))
        )

    os_id = _clean_text(entry.get("os_id"))
    if os_id:
        order_ref = _get_order_reference(os_id, order_lookup, global_lookup_cache)
        technician_display = _resolve_technician_display(order_ref)
        candidate_names.extend(_extract_technician_name_fragments(technician_display))

    for candidate in candidate_names:
        normalized = _normalize_technician_name(candidate)
        if normalized and normalized in selected_map:
            return selected_map[normalized]

    if not candidate_names and not os_id and len(selected) == 1:
        return selected[0]

    return None


def _normalize_technician_name(value: str | None) -> str:
    text = _clean_text(value)
    if not text:
        return ""
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = "".join(char for char in normalized if not unicodedata.combining(char))
    cleaned = re.sub(r"\s+", " ", ascii_text).strip().upper()
    return cleaned


def _normalize_matching_text(value: str | None) -> str:
    text = _clean_text(value)
    if not text:
        return ""
    normalized = unicodedata.normalize("NFKD", text.strip().lower())
    ascii_text = "".join(char for char in normalized if not unicodedata.combining(char))
    return re.sub(r"\s+", " ", ascii_text).strip()


def _normalize_technician_name_set(values: list[str]) -> set[str]:
    return {
        normalized
        for normalized in (_normalize_technician_name(value) for value in values)
        if normalized
    }


def _extract_technician_name_fragments(value: str | None) -> list[str]:
    text = _clean_text(value)
    if not text:
        return []
    fragments = re.split(r"[,;/|+]", text)
    normalized_fragments: list[str] = []
    for fragment in fragments:
        normalized = _normalize_technician_name(fragment)
        if normalized:
            normalized_fragments.append(normalized)
    return normalized_fragments


def _entry_matches_selected_technicians(
    entry: dict[str, Any],
    selected_set: set[str],
    order_lookup: dict[str, dict[str, Any]],
    global_lookup_cache: dict[str, dict[str, Any] | None],
) -> bool:
    if not selected_set:
        return True

    os_id = _clean_text(entry.get("os_id"))
    candidate_names: set[str] = set()
    for field in ("technician_names", "team_label"):
        for fragment in _extract_technician_name_fragments(_clean_text(entry.get(field))):
            candidate_names.add(fragment)

    if os_id:
        order_ref = _get_order_reference(os_id, order_lookup, global_lookup_cache)
        technician_display = _resolve_technician_display(order_ref)
        for fragment in _extract_technician_name_fragments(technician_display):
            candidate_names.add(fragment)

    if not candidate_names:
        # Keeps purely manual rows without OS association.
        return not bool(os_id)

    return bool(candidate_names & selected_set)


def _entry_matches_selected_subjects(
    entry: dict[str, Any],
    selected_subjects: set[str],
    order_lookup: dict[str, dict[str, Any]],
    global_lookup_cache: dict[str, dict[str, Any] | None],
) -> bool:
    if not selected_subjects:
        return True

    candidate_values: list[str] = [
        _clean_text(entry.get("subject_name")) or "",
    ]

    os_id = _clean_text(entry.get("os_id"))
    if os_id:
        order_ref = _get_order_reference(os_id, order_lookup, global_lookup_cache)
        if order_ref is not None:
            candidate_values.append(_clean_text(order_ref.get("subject_name")) or "")

    for candidate in candidate_values:
        if _normalize_matching_text(candidate) in selected_subjects:
            return True

    return False


def _entry_matches_selected_branch(
    entry: dict[str, Any],
    selected_branch: str,
    order_lookup: dict[str, dict[str, Any]],
    global_lookup_cache: dict[str, dict[str, Any] | None],
) -> bool:
    selected_normalized = _normalize_matching_text(selected_branch)
    if not selected_normalized:
        return True

    candidate_values: list[str] = []
    entry_branch = _clean_text(entry.get("branch_name"))
    if entry_branch:
        candidate_values.append(entry_branch)

    os_id = _clean_text(entry.get("os_id"))
    if os_id:
        order_ref = _get_order_reference(os_id, order_lookup, global_lookup_cache)
        if order_ref is not None:
            order_branch = _clean_text(order_ref.get("branch_name"))
            if order_branch:
                candidate_values.append(order_branch)

    if not candidate_values:
        return not bool(os_id)

    return any(_normalize_matching_text(candidate) == selected_normalized for candidate in candidate_values)


def _build_selected_technician_mismatch_error(
    selected_technicians: list[str],
    invalid_entries: list[dict[str, str]],
) -> str:
    selected_label = ", ".join(selected_technicians) if selected_technicians else "nenhum"
    preview_limit = 5
    preview_parts = [
        f"linha {item['line']} (OS {item['os_id']}, tecnico {item['technician']})"
        for item in invalid_entries[:preview_limit]
    ]
    preview_text = "; ".join(preview_parts)
    remaining = len(invalid_entries) - preview_limit
    if remaining > 0:
        preview_text = f"{preview_text}; e mais {remaining} linha(s)"
    return (
        "Nao foi possivel salvar o mapa: existem linhas com tecnico fora do filtro selecionado. "
        f"Tecnicos permitidos: {selected_label}. "
        f"Corrija/remova as linhas: {preview_text}."
    )

def _delay_report_ordered_technicians(
    technician_keys: Any,
    selected_sequence: list[str],
) -> list[str]:
    keys = [
        _clean_text(item)
        for item in technician_keys
        if _clean_text(item)
    ]
    if selected_sequence:
        ordered: list[str] = []
        seen: set[str] = set()
        for name in selected_sequence:
            normalized = _clean_text(name)
            if not normalized or normalized in seen:
                continue
            seen.add(normalized)
            ordered.append(normalized)
        for name in keys:
            if name in seen:
                continue
            seen.add(name)
            ordered.append(name)
        return ordered
    return sorted(keys, key=lambda value: value.lower())


def _delay_entry_sort_key(entry: dict[str, Any]) -> tuple[datetime, str, str]:
    parsed_candidates = [
        _as_clock(_parse_timestamp(entry.get("start_at"))),
        _as_clock(_parse_timestamp(entry.get("displacement_at"))),
        _as_clock(_parse_timestamp(entry.get("executed_at"))),
        _as_clock(_parse_timestamp(entry.get("finalized_at"))),
    ]
    parsed_candidates = [value for value in parsed_candidates if value is not None]
    start_slot, _ = _parse_slot_bounds(entry.get("slot_label"))
    primary_dt = parsed_candidates[0] if parsed_candidates else start_slot or datetime.max
    os_id = _clean_text(entry.get("os_id")) or ""
    return (
        primary_dt,
        _resolve_entry_technician(entry).lower(),
        os_id,
    )


def _parse_slot_bounds(slot_label: Any) -> tuple[datetime | None, datetime | None]:
    text = _clean_text(slot_label)
    if not text:
        return None, None
    match = re.search(r"(\d{2}:\d{2})\s*-\s*(\d{2}:\d{2})", text)
    if not match:
        return None, None
    start_dt = _as_clock(_parse_timestamp(match.group(1)))
    end_dt = _as_clock(_parse_timestamp(match.group(2)))
    return start_dt, end_dt


def _extract_delay_minutes(entry: dict[str, Any]) -> int | None:
    for field in ("occurrence_note", "opening_note", "comment_note", "status_label"):
        text = _clean_text(entry.get(field))
        if not text:
            continue
        match = re.search(r"\((\d+)\s*min\)", text, flags=re.IGNORECASE)
        if match:
            return int(match.group(1))

    start_dt = _as_clock(_parse_timestamp(entry.get("start_at")))
    end_candidates = [
        _as_clock(_parse_timestamp(entry.get("finalized_at"))),
        _as_clock(_parse_timestamp(entry.get("executed_at"))),
        _as_clock(_parse_timestamp(entry.get("displacement_at"))),
    ]
    end_dt = next((value for value in end_candidates if value is not None), None)
    if start_dt and end_dt and end_dt >= start_dt:
        minutes = int((end_dt - start_dt).total_seconds() // 60)
        if 0 <= minutes <= 24 * 60:
            return minutes

    slot_start, slot_end = _parse_slot_bounds(entry.get("slot_label"))
    if slot_start and slot_end and slot_end >= slot_start:
        minutes = int((slot_end - slot_start).total_seconds() // 60)
        if 0 <= minutes <= 24 * 60:
            return minutes

    return None
