from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
import unicodedata
from typing import Any

from ..config import Settings, SubjectGroup, get_settings, resolve_timezone
from ..repository import (
    fetch_filter_options,
    fetch_latest_sync,
    fetch_orders_for_technician_details,
)


class MetricsService:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self._tz = resolve_timezone(self.settings.app_timezone)

    def build_overview(
        self,
        selected_date: date | None = None,
        *,
        start_date: date | None = None,
        end_date: date | None = None,
        weekly_start_date: date | None = None,
        weekly_end_date: date | None = None,
        subject_names: list[str] | None = None,
        subject_group_name: str | None = None,
        branch_name: str | None = None,
        sector_id: str | None = None,
        technician_names: str | list[str] | None = None,
        status_name: str | None = None,
    ) -> dict[str, Any]:
        target_date = selected_date or datetime.now(self._tz).date()
        now_local = datetime.now(self._tz)
        now_local_naive = now_local.replace(tzinfo=None)
        subject_names = _normalize_filter_list(subject_names)
        subject_group_name = _normalize_filter(subject_group_name)
        branch_name = _normalize_filter(branch_name)
        sector_id = _normalize_filter(sector_id)
        technician_names = _normalize_filter_list(technician_names)
        status_name = _normalize_filter(status_name)

        rows = fetch_orders_for_technician_details(
            start_date=_date_to_str(start_date),
            end_date=_date_to_str(end_date),
            subject_name=subject_names,
            branch_name=branch_name,
            sector_id=sector_id,
            technician_name=technician_names,
            status_name=status_name,
            include_raw_payload=False,
        )
        available_subjects = _extract_available_subjects(rows)
        subject_group = _resolve_subject_group(
            self.settings.subject_groups,
            subject_group_name,
            available_subjects,
        )
        rows = _filter_rows_by_subject_group(rows, subject_group)

        open_by_subject: dict[str, int] = {}
        technician_sla_map: dict[str, dict[str, Any]] = {}
        hourly_grouped: dict[str, int] = {}
        active_total = 0
        within_sla_total = 0
        overdue_total = 0
        no_due_total = 0
        rescheduled_today = 0

        for row in rows:
            status = _normalize_status_text(row.get("status"))
            raw_payload = row.get("raw_payload") if isinstance(row.get("raw_payload"), dict) else {}
            opened_at, execution_started_at, closed_at, due_at = _resolve_order_datetimes(
                row,
                raw_payload,
            )
            rescheduled_at = _extract_rescheduled_datetime(raw_payload)
            scheduled_at = _extract_scheduled_datetime(raw_payload)
            is_closed = _is_closed(status=status, closed_at=closed_at, closed_statuses=self.settings.closed_status_set)
            in_execution = bool(
                _is_execution_status(status, self.settings.execution_status_set)
                or (execution_started_at is not None and not is_closed)
            )

            if is_closed and closed_at and closed_at.date() == target_date:
                hour = closed_at.strftime("%H")
                hourly_grouped[hour] = hourly_grouped.get(hour, 0) + 1

            if _is_rescheduled_on_date(
                status=status,
                rescheduled_at=rescheduled_at,
                scheduled_at=scheduled_at,
                target_date=target_date,
            ):
                rescheduled_today += 1

            if not is_closed:
                active_total += 1
                subject = (row.get("subject_name") or "Sem assunto").strip() or "Sem assunto"
                open_by_subject[subject] = open_by_subject.get(subject, 0) + 1

            sla_status = _evaluate_sla(
                due_at=due_at,
                closed_at=closed_at,
                now_local=now_local_naive,
            )
            if sla_status == "within":
                within_sla_total += 1
            elif sla_status == "overdue":
                overdue_total += 1
            else:
                no_due_total += 1

            tech_id = (row.get("technician_id") or "sem-id").strip() or "sem-id"
            tech_name = (row.get("technician_name") or "Sem tecnico").strip() or "Sem tecnico"
            bucket = technician_sla_map.setdefault(
                tech_id,
                {
                    "technician_id": tech_id,
                    "technician": tech_name,
                    "total_orders": 0,
                    "started_orders": 0,
                    "closed_orders": 0,
                    "in_execution": 0,
                    "within_sla": 0,
                    "overdue": 0,
                    "no_due": 0,
                    "_response_minutes": [],
                    "_execution_minutes": [],
                    "_total_minutes": [],
                    "_os_ids": [],
                },
            )
            bucket["total_orders"] += 1
            if execution_started_at is not None:
                bucket["started_orders"] += 1
            if is_closed:
                bucket["closed_orders"] += 1
            if in_execution:
                bucket["in_execution"] += 1
            if sla_status == "within":
                bucket["within_sla"] += 1
            elif sla_status == "overdue":
                bucket["overdue"] += 1
            else:
                bucket["no_due"] += 1

            response_minutes = _diff_minutes(opened_at, execution_started_at)
            execution_minutes = _diff_minutes(execution_started_at, closed_at)
            total_minutes = _diff_minutes(opened_at, closed_at)
            if response_minutes is not None:
                bucket["_response_minutes"].append(response_minutes)
            if execution_minutes is not None:
                bucket["_execution_minutes"].append(execution_minutes)
            if total_minutes is not None:
                bucket["_total_minutes"].append(total_minutes)
            if row.get("os_id") and len(bucket["_os_ids"]) < 15:
                bucket["_os_ids"].append(str(row["os_id"]))

        hourly_completed = []
        for hour in range(24):
            key = f"{hour:02d}"
            hourly_completed.append({"hour": f"{key}:00", "count": hourly_grouped.get(key, 0)})

        open_by_subject_list = [
            {"subject": name, "count": count}
            for name, count in sorted(
                open_by_subject.items(), key=lambda item: item[1], reverse=True
            )
        ]

        technician_sla = [_finalize_technician_metrics(bucket) for bucket in technician_sla_map.values()]
        technician_sla.sort(
            key=lambda item: (item["overdue"], item["sla_rate"], item["total_orders"]),
            reverse=True,
        )

        technicians_in_execution = [
            {
                "technician_id": item["technician_id"],
                "technician": item["technician"],
                "in_execution": item["in_execution"],
                "within_sla": item["within_sla"],
                "overdue": item["overdue"],
            }
            for item in technician_sla
            if item["in_execution"] > 0
        ]

        technician_movements = [
            {
                "technician_id": item["technician_id"],
                "technician": item["technician"],
                "handled_orders": item["total_orders"],
                "started_orders": item["started_orders"],
                "finished_orders": item["closed_orders"],
                "in_execution": item["in_execution"],
                "open_orders": item["open_orders"],
                "within_sla": item["within_sla"],
                "overdue": item["overdue"],
                "sla_rate": item["sla_rate"],
                "avg_response_minutes": item["avg_response_minutes"],
                "avg_execution_minutes": item["avg_execution_minutes"],
                "avg_total_minutes": item["avg_total_minutes"],
                "order_ids_sample": item["order_ids_sample"],
            }
            for item in technician_sla
        ]
        technician_movements.sort(
            key=lambda item: (
                item["finished_orders"],
                item["started_orders"],
                item["handled_orders"],
            ),
            reverse=True,
        )

        avg_execution_values = [
            float(item["avg_execution_minutes"])
            for item in technician_movements
            if item["avg_execution_minutes"] is not None
        ]
        avg_execution_overall = (
            round(sum(avg_execution_values) / len(avg_execution_values), 2)
            if avg_execution_values
            else None
        )

        sla_denominator = within_sla_total + overdue_total
        compliance_rate = round((within_sla_total / sla_denominator) * 100, 2) if sla_denominator else 100.0
        latest_sync = fetch_latest_sync()
        completed_today = sum(item["count"] for item in hourly_completed)
        same_primary_and_weekly_range = (
            _date_to_str(start_date) == _date_to_str(weekly_start_date)
            and _date_to_str(end_date) == _date_to_str(weekly_end_date)
        )
        if same_primary_and_weekly_range:
            weekly_rows = rows
        else:
            weekly_rows = fetch_orders_for_technician_details(
                start_date=_date_to_str(weekly_start_date),
                end_date=_date_to_str(weekly_end_date),
                subject_name=subject_names,
                branch_name=branch_name,
                sector_id=sector_id,
                technician_name=technician_names,
                status_name=status_name,
                include_raw_payload=False,
            )
            weekly_available_subjects = _extract_available_subjects(weekly_rows)
            weekly_subject_group = _resolve_subject_group(
                self.settings.subject_groups,
                subject_group_name,
                weekly_available_subjects,
            )
            weekly_rows = _filter_rows_by_subject_group(weekly_rows, weekly_subject_group)
        weekly_overview = _build_weekly_overview(
            weekly_rows,
            target_date=target_date,
            start_date=weekly_start_date,
            end_date=weekly_end_date,
            closed_statuses=self.settings.closed_status_set,
        )

        return {
            "as_of": now_local.replace(microsecond=0).isoformat(),
            "timezone": self.settings.app_timezone,
            "selected_date": str(target_date),
            "filters": {
                "start_date": _date_to_str(start_date),
                "end_date": _date_to_str(end_date),
                "subject": subject_names,
                "subject_group": subject_group.key if subject_group else None,
                "subject_group_label": subject_group.label if subject_group else None,
                "subject_group_subjects": subject_group.subjects if subject_group else [],
                "branch": branch_name,
                "sector": sector_id,
                "technician": technician_names,
                "status": status_name,
            },
            "completed_today": completed_today,
            "weekly_overview": weekly_overview,
            "rescheduled_today": rescheduled_today,
            "hourly_completed": hourly_completed,
            "open_by_subject": open_by_subject_list,
            "technicians_in_execution": technicians_in_execution,
            "technician_sla": technician_sla,
            "technician_movements": technician_movements,
            "movements_summary": {
                "technicians_total": len(technician_movements),
                "technicians_in_execution": len(technicians_in_execution),
                "orders_handled": sum(item["handled_orders"] for item in technician_movements),
                "orders_started": sum(item["started_orders"] for item in technician_movements),
                "orders_finished": sum(item["finished_orders"] for item in technician_movements),
                "avg_execution_minutes": avg_execution_overall,
            },
            "sla": {
                "total_orders": len(rows),
                "active_orders": active_total,
                "within_sla": within_sla_total,
                "overdue": overdue_total,
                "no_due": no_due_total,
                "compliance_rate": compliance_rate,
            },
            "last_sync": latest_sync,
        }

    def build_weekly_vip_report(
        self,
        *,
        start_date: date | None = None,
        end_date: date | None = None,
        subject_names: list[str] | None = None,
        subject_group_name: str | None = None,
        branch_name: str | None = None,
        sector_id: str | None = None,
        technician_names: str | list[str] | None = None,
    ) -> dict[str, Any]:
        today = datetime.now(self._tz).date()
        period_end = end_date or today
        period_start = start_date or (period_end - timedelta(days=6))
        if period_start > period_end:
            raise ValueError("start_date nao pode ser maior que end_date.")

        subject_names = _normalize_filter_list(subject_names)
        subject_group_name = _normalize_filter(subject_group_name)
        branch_name = _normalize_filter(branch_name)
        sector_id = _normalize_filter(sector_id)
        technician_names = _normalize_filter_list(technician_names)

        rows = fetch_orders_for_technician_details(
            start_date=_date_to_str(period_start),
            end_date=_date_to_str(period_end),
            subject_name=subject_names,
            branch_name=branch_name,
            sector_id=sector_id,
            technician_name=technician_names,
            status_name=None,
            include_raw_payload=False,
        )
        available_subjects = _extract_available_subjects(rows)
        subject_group = _resolve_subject_group(
            self.settings.subject_groups,
            subject_group_name,
            available_subjects,
        )
        rows = _filter_rows_by_subject_group(rows, subject_group)
        report = _build_weekly_vip_report_payload(
            rows,
            period_start=period_start,
            period_end=period_end,
            closed_statuses=self.settings.closed_status_set,
        )
        report["filters"] = {
            "start_date": _date_to_str(period_start),
            "end_date": _date_to_str(period_end),
            "subject": subject_names,
            "subject_group": subject_group.key if subject_group else None,
            "subject_group_label": subject_group.label if subject_group else None,
            "subject_group_subjects": subject_group.subjects if subject_group else [],
            "branch": branch_name,
            "sector": sector_id,
            "technician": technician_names,
        }
        report["as_of"] = datetime.now(self._tz).replace(microsecond=0).isoformat()
        report["timezone"] = self.settings.app_timezone
        return report

    def build_filter_options(self) -> dict[str, Any]:
        options = fetch_filter_options()
        subjects = options.get("subjects", [])
        return {
            **options,
            "subject_groups": _build_subject_group_options(self.settings.subject_groups, subjects),
        }

    def build_card_orders(
        self,
        metric: str,
        *,
        selected_date: date | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
        subject_names: list[str] | None = None,
        subject_group_name: str | None = None,
        branch_name: str | None = None,
        sector_id: str | None = None,
        technician_name: list[str] | None = None,
        limit: int = 200,
    ) -> dict[str, Any]:
        metric_key = _normalize_card_metric(metric)
        if metric_key is None:
            raise ValueError("Metric invalida para detalhamento.")

        target_date = selected_date or datetime.now(self._tz).date()
        now_local = datetime.now(self._tz)
        now_local_naive = now_local.replace(tzinfo=None)

        subject_names = _normalize_filter_list(subject_names)
        subject_group_name = _normalize_filter(subject_group_name)
        branch_name = _normalize_filter(branch_name)
        sector_id = _normalize_filter(sector_id)
        technician_name = _normalize_filter_list(technician_name)

        rows = fetch_orders_for_technician_details(
            start_date=_date_to_str(start_date),
            end_date=_date_to_str(end_date),
            subject_name=subject_names,
            branch_name=branch_name,
            sector_id=sector_id,
            technician_name=technician_name,
            status_name=None,
        )
        available_subjects = _extract_available_subjects(rows)
        subject_group = _resolve_subject_group(
            self.settings.subject_groups,
            subject_group_name,
            available_subjects,
        )
        rows = _filter_rows_by_subject_group(rows, subject_group)

        matched_orders: list[dict[str, Any]] = []
        for row in rows:
            status = _normalize_status_text(row.get("status"))
            raw_payload = row.get("raw_payload") if isinstance(row.get("raw_payload"), dict) else {}
            opened_at, execution_started_at, closed_at, due_at = _resolve_order_datetimes(
                row,
                raw_payload,
            )
            is_closed = _is_closed(
                status=status,
                closed_at=closed_at,
                closed_statuses=self.settings.closed_status_set,
            )
            in_execution = bool(
                _is_execution_status(status, self.settings.execution_status_set)
                or (execution_started_at is not None and not is_closed)
            )
            sla_status = _evaluate_sla(
                due_at=due_at,
                closed_at=closed_at,
                now_local=now_local_naive,
            )
            execution_minutes = _diff_minutes(execution_started_at, closed_at)
            rescheduled_at = _extract_rescheduled_datetime(raw_payload)
            scheduled_at = _extract_scheduled_datetime(raw_payload)
            displacement_at = _extract_displacement_datetime(raw_payload, row)
            technician_message = _extract_technician_message(raw_payload)
            customer_name = _extract_customer_name(raw_payload, row)

            if not _matches_card_metric(
                metric_key=metric_key,
                target_date=target_date,
                status=status,
                is_closed=is_closed,
                closed_at=closed_at,
                in_execution=in_execution,
                execution_started_at=execution_started_at,
                execution_minutes=execution_minutes,
                rescheduled_at=rescheduled_at,
                scheduled_at=scheduled_at,
                sla_status=sla_status,
            ):
                continue

            matched_orders.append(
                {
                    "os_id": str(row.get("os_id") or ""),
                    "status": str(row.get("status") or ""),
                    "subject_name": str(row.get("subject_name") or ""),
                    "branch_name": str(row.get("branch_name") or ""),
                    "customer_name": customer_name,
                    "technician_id": str(row.get("technician_id") or ""),
                    "technician_name": str(row.get("technician_name") or ""),
                    "opened_at": row.get("opened_at"),
                    "opened_time": _time_only(opened_at),
                    "displacement_at": _datetime_to_text(displacement_at),
                    "displacement_time": _time_only(displacement_at),
                    "execution_started_at": row.get("execution_started_at"),
                    "execution_time": _time_only(execution_started_at),
                    "rescheduled_at": _datetime_to_text(rescheduled_at or scheduled_at),
                    "rescheduled_time": _time_only(rescheduled_at or scheduled_at),
                    "closed_at": row.get("closed_at"),
                    "closed_time": _time_only(closed_at),
                    "due_at": row.get("due_at"),
                    "sla_status": sla_status,
                    "sla_label": _sla_label_text(
                        sla_status,
                        due_at=due_at,
                        closed_at=closed_at,
                        now_local=now_local_naive,
                        is_closed=is_closed,
                    ),
                    "response_minutes": _diff_minutes(opened_at, execution_started_at),
                    "execution_minutes": execution_minutes,
                    "total_minutes": _diff_minutes(opened_at, closed_at),
                    "technician_message": technician_message,
                }
            )

        matched_orders.sort(
            key=lambda row: (
                row.get("closed_at") or "",
                row.get("execution_started_at") or "",
                row.get("opened_at") or "",
            ),
            reverse=True,
        )
        if metric_key == "avg_execution":
            matched_orders.sort(
                key=lambda row: row.get("execution_minutes") or -1,
                reverse=True,
            )

        safe_limit = max(10, min(1000, int(limit)))
        total = len(matched_orders)
        limited_orders = matched_orders[:safe_limit]

        return {
            "metric": metric_key,
            "metric_label": _card_metric_label(metric_key),
            "total_orders": total,
            "returned_orders": len(limited_orders),
            "limit": safe_limit,
            "truncated": total > safe_limit,
            "selected_date": str(target_date),
            "filters": {
                "start_date": _date_to_str(start_date),
                "end_date": _date_to_str(end_date),
                "subject": subject_names,
                "subject_group": subject_group.key if subject_group else None,
                "subject_group_label": subject_group.label if subject_group else None,
                "subject_group_subjects": subject_group.subjects if subject_group else [],
                "branch": branch_name,
                "sector": sector_id,
            },
            "orders": limited_orders,
            "last_sync": fetch_latest_sync(),
        }

    def build_technician_order_details(
        self,
        *,
        start_date: date | None = None,
        end_date: date | None = None,
        subject_names: list[str] | None = None,
        subject_group_name: str | None = None,
        branch_name: str | None = None,
        sector_id: str | None = None,
        technician_name: str | None = None,
        status_name: str | None = None,
    ) -> dict[str, Any]:
        subject_names = _normalize_filter_list(subject_names)
        subject_group_name = _normalize_filter(subject_group_name)
        branch_name = _normalize_filter(branch_name)
        sector_id = _normalize_filter(sector_id)
        technician_name = _normalize_filter(technician_name)
        status_name = _normalize_filter(status_name)

        rows = fetch_orders_for_technician_details(
            start_date=_date_to_str(start_date),
            end_date=_date_to_str(end_date),
            subject_name=subject_names,
            branch_name=branch_name,
            sector_id=sector_id,
            technician_name=technician_name,
            status_name=status_name,
        )
        available_subjects = _extract_available_subjects(rows)
        subject_group = _resolve_subject_group(
            self.settings.subject_groups,
            subject_group_name,
            available_subjects,
        )
        rows = _filter_rows_by_subject_group(rows, subject_group)

        detailed_orders: list[dict[str, Any]] = []
        orders_with_execution = 0
        orders_with_closing = 0
        orders_with_displacement = 0
        orders_with_message = 0
        for row in rows:
            raw_payload = row.get("raw_payload") if isinstance(row.get("raw_payload"), dict) else {}
            opened_at, execution_started_at, closed_at, _due_at = _resolve_order_datetimes(
                row,
                raw_payload,
            )
            if execution_started_at is not None:
                orders_with_execution += 1
            if closed_at is not None:
                orders_with_closing += 1

            displacement_at = _extract_displacement_datetime(raw_payload, row)
            if displacement_at is not None:
                orders_with_displacement += 1

            technician_message = _extract_technician_message(raw_payload)
            if technician_message:
                orders_with_message += 1
            customer_name = _extract_customer_name(raw_payload, row)

            detailed_orders.append(
                {
                    "os_id": str(row.get("os_id") or ""),
                    "status": str(row.get("status") or ""),
                    "subject_name": str(row.get("subject_name") or ""),
                    "branch_name": str(row.get("branch_name") or ""),
                    "customer_name": customer_name,
                    "technician_id": str(row.get("technician_id") or ""),
                    "technician_name": str(row.get("technician_name") or ""),
                    "opened_at": row.get("opened_at"),
                    "opened_time": _time_only(opened_at),
                    "displacement_at": _datetime_to_text(displacement_at),
                    "displacement_time": _time_only(displacement_at),
                    "execution_started_at": row.get("execution_started_at"),
                    "execution_time": _time_only(execution_started_at),
                    "closed_at": row.get("closed_at"),
                    "closed_time": _time_only(closed_at),
                    "updated_at": row.get("updated_at"),
                    "technician_message": technician_message,
                }
            )

        return {
            "filters": {
                "start_date": _date_to_str(start_date),
                "end_date": _date_to_str(end_date),
                "subject": subject_names,
                "subject_group": subject_group.key if subject_group else None,
                "subject_group_label": subject_group.label if subject_group else None,
                "subject_group_subjects": subject_group.subjects if subject_group else [],
                "branch": branch_name,
                "sector": sector_id,
                "technician": technician_name,
                "status": status_name,
            },
            "summary": {
                "total_orders": len(detailed_orders),
                "with_displacement": orders_with_displacement,
                "with_execution": orders_with_execution,
                "with_closing": orders_with_closing,
                "with_message": orders_with_message,
            },
            "orders": detailed_orders,
            "last_sync": fetch_latest_sync(),
        }


@dataclass(frozen=True)
class SubjectGroupMatch:
    key: str
    label: str
    patterns: tuple[str, ...]
    subjects: tuple[str, ...]


def _normalize_filter(value: str | None) -> str | None:
    if value is None:
        return None
    text = value.strip()
    if not text or text == "__all__":
        return None
    return text


def _normalize_filter_list(values: str | list[str] | None) -> list[str] | None:
    if not values:
        return None
    source_values = [values] if isinstance(values, str) else values
    normalized: list[str] = []
    seen: set[str] = set()
    for value in source_values:
        for chunk in str(value or "").split(","):
            text = chunk.strip()
            if not text or text == "__all__":
                continue
            if text in seen:
                continue
            seen.add(text)
            normalized.append(text)
    return normalized or None


def _extract_available_subjects(rows: list[dict[str, Any]]) -> list[str]:
    subjects: list[str] = []
    seen: set[str] = set()
    for row in rows:
        text = _resolve_subject_name(row)
        if not text or text in seen:
            continue
        seen.add(text)
        subjects.append(text)
    return sorted(subjects, key=lambda value: _normalize_matching_text(value))


def _build_subject_group_options(
    configured_groups: list[SubjectGroup],
    available_subjects: list[str],
) -> list[dict[str, Any]]:
    options: list[dict[str, Any]] = []
    for group in configured_groups:
        matched_subjects = _resolve_group_subjects(group, available_subjects)
        options.append(
            {
                "key": group.key,
                "label": group.label,
                "patterns": list(group.patterns),
                "subjects_count": len(matched_subjects),
                "subjects": matched_subjects,
            }
        )
    return options


def _resolve_subject_group(
    configured_groups: list[SubjectGroup],
    requested_group_name: str | None,
    available_subjects: list[str],
) -> SubjectGroupMatch | None:
    requested = _normalize_filter(requested_group_name)
    if not requested:
        return None
    requested_key = _normalize_matching_text(requested).replace(" ", "_")
    for group in configured_groups:
        if group.key != requested_key:
            continue
        return SubjectGroupMatch(
            key=group.key,
            label=group.label,
            patterns=group.patterns,
            subjects=tuple(_resolve_group_subjects(group, available_subjects)),
        )
    return None


def _resolve_group_subjects(group: SubjectGroup, available_subjects: list[str]) -> list[str]:
    matched: list[str] = []
    seen: set[str] = set()
    normalized_patterns = [_normalize_matching_text(pattern) for pattern in group.patterns]
    for subject in available_subjects:
        normalized_subject = _normalize_matching_text(subject)
        if not normalized_subject:
            continue
        if not any(
            _subject_matches_pattern(normalized_subject, pattern)
            for pattern in normalized_patterns
        ):
            continue
        if subject in seen:
            continue
        seen.add(subject)
        matched.append(subject)
    return matched


def _filter_rows_by_subject_group(
    rows: list[dict[str, Any]],
    subject_group: SubjectGroupMatch | None,
) -> list[dict[str, Any]]:
    if subject_group is None:
        return rows
    matched_subjects = set(subject_group.subjects)
    if matched_subjects:
        return [row for row in rows if _resolve_subject_name(row) in matched_subjects]
    return []


def _build_weekly_overview(
    rows: list[dict[str, Any]],
    *,
    target_date: date,
    start_date: date | None,
    end_date: date | None,
    closed_statuses: set[str],
) -> dict[str, Any]:
    period_start = start_date or (target_date - timedelta(days=target_date.weekday()))
    period_end = end_date or target_date
    if period_end < period_start:
        period_start, period_end = period_end, period_start

    closed_orders: list[dict[str, Any]] = []
    by_branch: dict[str, dict[str, Any]] = {}
    by_day: dict[date, int] = {}
    by_shift: dict[str, int] = {"morning": 0, "afternoon": 0, "night": 0}
    installations_by_day: dict[date, int] = {}
    installations_by_technician: dict[str, dict[str, Any]] = {}
    productivity_by_technician: dict[str, dict[str, Any]] = {}
    median_execution_by_subject: dict[str, dict[str, Any]] = {}
    active_technicians: set[str] = set()

    for row in rows:
        status = _normalize_status_text(row.get("status"))
        raw_payload = row.get("raw_payload") if isinstance(row.get("raw_payload"), dict) else {}
        _opened_at, _execution_started_at, closed_at, _due_at = _resolve_order_datetimes(
            row,
            raw_payload,
        )
        if not _is_closed(status=status, closed_at=closed_at, closed_statuses=closed_statuses):
            continue
        if closed_at is None:
            continue
        closed_date = closed_at.date()
        if closed_date < period_start or closed_date > period_end:
            continue

        closed_orders.append(row)
        by_day[closed_date] = by_day.get(closed_date, 0) + 1
        by_shift[_resolve_shift_key(closed_at)] += 1

        subject_name = _resolve_subject_name(row)
        subject_label = subject_name or "Sem assunto"
        execution_minutes = _diff_minutes(_execution_started_at, closed_at)
        subject_bucket = median_execution_by_subject.setdefault(
            _normalize_matching_text(subject_label) or subject_label,
            {
                "subject": subject_label,
                "orders": 0,
                "_execution_minutes": [],
            },
        )
        subject_bucket["orders"] += 1
        if execution_minutes is not None:
            subject_bucket["_execution_minutes"].append(execution_minutes)
        is_installation = _is_installation_subject(subject_name)
        branch_name = str(row.get("branch_name") or "").strip() or "Sem unidade"
        branch_bucket = by_branch.setdefault(
            branch_name,
            {
                "branch": branch_name,
                "finished_orders": 0,
                "installations": 0,
                "_technicians": set(),
            },
        )
        branch_bucket["finished_orders"] += 1
        if is_installation:
            branch_bucket["installations"] += 1
            installations_by_day[closed_date] = installations_by_day.get(closed_date, 0) + 1

        tech_key = _resolve_technician_key(row)
        if tech_key:
            active_technicians.add(tech_key)
            branch_bucket["_technicians"].add(tech_key)
            tech_name = str(row.get("technician_name") or "").strip() or "Sem tecnico"
            productivity_bucket = productivity_by_technician.setdefault(
                tech_key,
                {
                    "technician": tech_name,
                    "total_orders": 0,
                    "installations": 0,
                    "_active_days": set(),
                    "_execution_minutes": [],
                },
            )
            productivity_bucket["total_orders"] += 1
            productivity_bucket["_active_days"].add(closed_date)
            if execution_minutes is not None:
                productivity_bucket["_execution_minutes"].append(execution_minutes)
            if is_installation:
                tech_bucket = installations_by_technician.setdefault(
                    tech_key,
                    {
                        "technician": tech_name,
                        "installations": 0,
                    },
                )
                tech_bucket["installations"] += 1
                productivity_bucket["installations"] += 1

    total_finished = len(closed_orders)
    total_installations = sum(
        1 for row in closed_orders if _is_installation_subject(_resolve_subject_name(row))
    )
    installation_percentage = (
        round((total_installations / total_finished) * 100, 2) if total_finished else 0.0
    )
    productive_day = _resolve_productive_day(by_day)

    branch_rows: list[dict[str, Any]] = []
    for bucket in by_branch.values():
        finished = int(bucket["finished_orders"])
        installations = int(bucket["installations"])
        branch_rows.append(
            {
                "branch": bucket["branch"],
                "finished_orders": finished,
                "installations": installations,
                "installation_percentage": round((installations / finished) * 100, 2)
                if finished
                else 0.0,
                "active_technicians": len(bucket["_technicians"]),
            }
        )
    branch_rows.sort(
        key=lambda item: (item["finished_orders"], item["installations"], item["branch"]),
        reverse=True,
    )

    return {
        "period_start": str(period_start),
        "period_end": str(period_end),
        "finished_orders": total_finished,
        "installations": total_installations,
        "installation_percentage": installation_percentage,
        "most_productive_day": productive_day,
        "active_technicians": len(active_technicians),
        "technician_order_count": sum(
            1 for row in closed_orders if _resolve_technician_key(row)
        ),
        "finished_by_day": _build_finished_by_day(period_start, period_end, by_day),
        "productivity_by_shift": _build_productivity_by_shift(by_shift, total_finished),
        "installations_by_day": _build_installations_by_day(
            period_start,
            period_end,
            installations_by_day,
        ),
        "installations_by_technician": _build_installations_by_technician(
            installations_by_technician,
        ),
        "technician_productivity_ranking": _build_technician_productivity_ranking(
            productivity_by_technician,
        ),
        "median_execution_by_subject": _build_median_execution_by_subject(
            median_execution_by_subject,
        ),
        "top_installation_day": _resolve_productive_day(installations_by_day),
        "branches": branch_rows,
    }


def _is_installation_subject(subject_name: str | None) -> bool:
    normalized = _normalize_matching_text(subject_name)
    if not normalized:
        return False
    installation_tokens = (
        "instalacao",
        "instalacoes",
        "instalar",
        "instal",
    )
    return any(token in normalized for token in installation_tokens)


def _resolve_technician_key(row: dict[str, Any]) -> str | None:
    tech_id = str(row.get("technician_id") or "").strip()
    tech_name = str(row.get("technician_name") or "").strip()
    if tech_id and tech_id.lower() not in {"sem-id", "none", "null"}:
        return f"id:{tech_id}"
    if tech_name and tech_name.lower() not in {"sem tecnico", "none", "null"}:
        return f"name:{_normalize_matching_text(tech_name)}"
    return None


def _resolve_productive_day(by_day: dict[date, int]) -> dict[str, Any] | None:
    if not by_day:
        return None
    target_day, count = max(by_day.items(), key=lambda item: (item[1], item[0]))
    return {
        "date": str(target_day),
        "weekday": _weekday_name_pt(target_day),
        "weekday_short": _weekday_short_name_pt(target_day),
        "finished_orders": int(count),
    }


def _build_finished_by_day(
    period_start: date,
    period_end: date,
    by_day: dict[date, int],
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    current = period_start
    while current <= period_end:
        result.append(
            {
                "date": str(current),
                "weekday": _weekday_name_pt(current),
                "weekday_short": _weekday_short_name_pt(current),
                "finished_orders": int(by_day.get(current, 0)),
            }
        )
        current += timedelta(days=1)
    return result


VIP_EXCLUDED_SUBJECTS = {
    "retirada de equipamento",
    "retirada de equipamento por inadimplencia",
}
VIP_EXCLUDED_TECHNICIANS = {"anne steffany - mundau"}
VIP_DAY_LABELS = ("Segunda", "Terca", "Quarta", "Quinta", "Sexta", "Sabado", "Domingo")
VIP_SHIFT_LABELS = {
    "morning": "Manha",
    "afternoon": "Tarde",
    "night": "Noite",
    "no_start": "Sem inicio",
}


def _build_weekly_vip_report_payload(
    rows: list[dict[str, Any]],
    *,
    period_start: date,
    period_end: date,
    closed_statuses: set[str],
) -> dict[str, Any]:
    filtered_rows: list[dict[str, Any]] = []
    by_day: dict[str, int] = {label: 0 for label in VIP_DAY_LABELS}
    installations_by_day: dict[str, int] = {label: 0 for label in VIP_DAY_LABELS}
    shift_counts: dict[str, int] = {key: 0 for key in VIP_SHIFT_LABELS}
    shift_by_day: dict[str, dict[str, int]] = {
        label: {"morning": 0, "afternoon": 0, "night": 0} for label in VIP_DAY_LABELS
    }
    technicians: dict[str, dict[str, Any]] = {}
    installation_technicians: dict[str, dict[str, Any]] = {}
    subject_times: dict[str, dict[str, Any]] = {}

    for row in rows:
        subject = _resolve_subject_name(row) or "Sem assunto"
        technician = str(row.get("technician_name") or "Sem tecnico").strip() or "Sem tecnico"
        if _normalize_matching_text(subject) in VIP_EXCLUDED_SUBJECTS:
            continue
        if _normalize_matching_text(technician) in VIP_EXCLUDED_TECHNICIANS:
            continue

        opened_at, execution_started_at, closed_at, _due_at = _resolve_order_datetimes(row, {})
        status = _normalize_status_text(row.get("status"))
        if not closed_at or not _is_closed(status=status, closed_at=closed_at, closed_statuses=closed_statuses):
            continue
        if closed_at.date() < period_start or closed_at.date() > period_end:
            continue

        execution_minutes = _diff_minutes(execution_started_at, closed_at)
        day_label = VIP_DAY_LABELS[closed_at.weekday()]
        shift_key = _vip_shift_key(execution_started_at)
        is_installation = _is_installation_subject(subject)

        filtered_rows.append(row)
        by_day[day_label] += 1
        if is_installation:
            installations_by_day[day_label] += 1
        shift_counts[shift_key] += 1
        if shift_key in shift_by_day[day_label]:
            shift_by_day[day_label][shift_key] += 1

        tech_bucket = technicians.setdefault(
            technician,
            {"technician": technician, "total": 0, "days": set(), "morning": 0, "execution_minutes": []},
        )
        tech_bucket["total"] += 1
        tech_bucket["days"].add(closed_at.date())
        if shift_key == "morning":
            tech_bucket["morning"] += 1
        if execution_minutes is not None:
            tech_bucket["execution_minutes"].append(execution_minutes)

        if is_installation:
            inst_bucket = installation_technicians.setdefault(
                technician,
                {"technician": technician, "total": 0, "days": set(), "morning": 0, "execution_minutes": []},
            )
            inst_bucket["total"] += 1
            inst_bucket["days"].add(closed_at.date())
            if shift_key == "morning":
                inst_bucket["morning"] += 1
            if execution_minutes is not None:
                inst_bucket["execution_minutes"].append(execution_minutes)

        if execution_minutes is not None:
            subject_bucket = subject_times.setdefault(
                subject,
                {"subject": subject, "count": 0, "execution_minutes": []},
            )
            subject_bucket["count"] += 1
            subject_bucket["execution_minutes"].append(execution_minutes)

    total_os = len(filtered_rows)
    total_installations = sum(installations_by_day.values())
    timed_orders = sum(1 for bucket in technicians.values() for _ in bucket["execution_minutes"])
    top_day, top_day_count = _top_key_value(by_day)
    top_installation_day, top_installation_day_count = _top_key_value(installations_by_day)
    technician_ranking = _build_vip_technician_ranking(technicians)
    installation_ranking = _build_vip_installation_ranking(installation_technicians)
    subject_execution_times = _build_vip_subject_times(subject_times)
    top_installer = installation_ranking[0] if installation_ranking else None
    fastest = next((row for row in technician_ranking if row.get("median_minutes") is not None), None)
    top_productivity = technician_ranking[0] if technician_ranking else None
    shift_rows = _vip_shift_rows(shift_counts, total_os)
    most_shift = max(shift_rows, key=lambda item: item["orders"], default=None)

    highlights = [
        {"label": "Tempo", "title": fastest["technician"] if fastest else "-", "text": f"Melhor mediana: {_format_minutes_value(fastest.get('median_minutes') if fastest else None)}"},
        {"label": "Prod", "title": top_productivity["technician"] if top_productivity else "-", "text": f"Maior score: {_format_score(top_productivity.get('score') if top_productivity else None)}"},
        {"label": "Inst", "title": top_installer["technician"] if top_installer else "-", "text": f"{int(top_installer['total']) if top_installer else 0} instalacoes"},
        {"label": "Dia", "title": top_day, "text": f"Pico semanal: {top_day_count} OS"},
        {"label": "Turno", "title": most_shift["label"] if most_shift else "-", "text": f"{most_shift['orders'] if most_shift else 0} OS ({most_shift['percentage'] if most_shift else 0:.0f}%)"},
    ]

    conclusions = _build_vip_conclusions(
        total_os=total_os,
        total_installations=total_installations,
        top_day=top_day,
        top_day_count=top_day_count,
        top_installation_day=top_installation_day,
        top_installation_day_count=top_installation_day_count,
        top_installer=top_installer,
        top_productivity=top_productivity,
        fastest=fastest,
        most_shift=most_shift,
        subject_execution_times=subject_execution_times,
    )

    return {
        "period": {
            "start_date": _date_to_str(period_start),
            "end_date": _date_to_str(period_end),
            "label": f"{period_start.strftime('%d/%m')} a {period_end.strftime('%d/%m/%Y')}",
            "filename_label": f"{period_start.strftime('%d-%m')}a{period_end.strftime('%d-%m-%Y')}",
        },
        "kpis": {
            "total_os": total_os,
            "total_installations": total_installations,
            "top_day": top_day,
            "top_day_orders": top_day_count,
            "active_technicians": len(technicians),
            "timed_orders": timed_orders,
            "top_installation_day": top_installation_day,
            "top_installation_day_orders": top_installation_day_count,
            "top_installer": top_installer["technician"] if top_installer else None,
            "top_installer_orders": top_installer["total"] if top_installer else 0,
            "fastest_technician": fastest["technician"] if fastest else None,
            "fastest_median_minutes": fastest.get("median_minutes") if fastest else None,
        },
        "per_day": _dict_to_rows(by_day, "day", "orders"),
        "installations_per_day": _dict_to_rows(installations_by_day, "day", "installations"),
        "shift_counts": shift_rows,
        "shift_by_day": [
            {"day": day, **shift_by_day[day], "total": sum(shift_by_day[day].values())}
            for day in VIP_DAY_LABELS
        ],
        "installation_ranking": installation_ranking,
        "technician_ranking": technician_ranking,
        "subject_execution_times": subject_execution_times,
        "highlights": highlights,
        "conclusions": conclusions,
    }


def _vip_shift_key(value: datetime | None) -> str:
    if value is None:
        return "no_start"
    if 6 <= value.hour < 12:
        return "morning"
    if 12 <= value.hour < 18:
        return "afternoon"
    return "night"


def _top_key_value(values: dict[str, int]) -> tuple[str, int]:
    if not values:
        return "-", 0
    key = max(values, key=lambda item: values[item])
    return key, int(values[key])


def _dict_to_rows(values: dict[str, int], key_name: str, value_name: str) -> list[dict[str, Any]]:
    return [{key_name: key, value_name: int(value)} for key, value in values.items()]


def _vip_shift_rows(shift_counts: dict[str, int], total: int) -> list[dict[str, Any]]:
    rows = []
    for key in ("morning", "afternoon", "night", "no_start"):
        count = int(shift_counts.get(key, 0))
        rows.append({
            "key": key,
            "label": VIP_SHIFT_LABELS[key],
            "orders": count,
            "percentage": round((count / total) * 100, 2) if total else 0.0,
        })
    return rows


def _build_vip_technician_ranking(buckets: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for bucket in buckets.values():
        total = int(bucket["total"])
        if total < 3:
            continue
        days = max(1, len(bucket["days"]))
        minutes = bucket["execution_minutes"]
        if len(minutes) < 3:
            median_minutes = None
            avg_minutes = _avg(minutes)
        else:
            median_minutes = _median(minutes)
            avg_minutes = _avg(minutes)
        rows.append({
            "technician": bucket["technician"],
            "total": total,
            "days": days,
            "orders_per_day": round(total / days, 2),
            "avg_minutes": avg_minutes,
            "median_minutes": median_minutes,
            "morning_percentage": round((bucket["morning"] / total) * 100, 2) if total else 0.0,
        })
    _apply_vip_score(rows, productivity_key="orders_per_day", median_key="median_minutes", score_key="score", weights=(0.5, 0.3, 0.2))
    rows.sort(key=lambda item: (item["score"], item["total"], item["technician"]), reverse=True)
    return rows


def _build_vip_installation_ranking(buckets: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for bucket in buckets.values():
        total = int(bucket["total"])
        if total < 1:
            continue
        days = max(1, len(bucket["days"]))
        minutes = bucket["execution_minutes"]
        rows.append({
            "technician": bucket["technician"],
            "total": total,
            "days": days,
            "installations_per_day": round(total / days, 2),
            "avg_minutes": _avg(minutes),
            "median_minutes": _median(minutes) if len(minutes) >= 2 else None,
            "morning_percentage": round((bucket["morning"] / total) * 100, 2) if total else 0.0,
        })
    _apply_vip_score(rows, productivity_key="installations_per_day", median_key="median_minutes", score_key="score", weights=(0.4, 0.4, 0.2))
    rows.sort(key=lambda item: (item["score"], item["total"], item["technician"]), reverse=True)
    return rows


def _apply_vip_score(
    rows: list[dict[str, Any]],
    *,
    productivity_key: str,
    median_key: str,
    score_key: str,
    weights: tuple[float, float, float],
) -> None:
    max_productivity = max((float(row.get(productivity_key) or 0) for row in rows), default=0) or 1
    medians = [float(row[median_key]) for row in rows if row.get(median_key)]
    min_median = min(medians) if medians else 1
    max_morning = max((float(row.get("morning_percentage") or 0) for row in rows), default=0) or 1
    for row in rows:
        productivity_score = float(row.get(productivity_key) or 0) / max_productivity
        median = row.get(median_key)
        time_score = (min_median / float(median)) if median else 0
        morning_score = float(row.get("morning_percentage") or 0) / max_morning
        row[score_key] = round(
            weights[0] * productivity_score + weights[1] * time_score + weights[2] * morning_score,
            3,
        )


def _build_vip_subject_times(buckets: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for bucket in buckets.values():
        minutes = bucket["execution_minutes"]
        if len(minutes) < 2:
            continue
        median_minutes = _median(minutes)
        rows.append({
            "subject": bucket["subject"],
            "count": int(bucket["count"]),
            "avg_minutes": _avg(minutes),
            "median_minutes": median_minutes,
            "range": _vip_time_range(median_minutes),
        })
    rows.sort(key=lambda item: (item["median_minutes"] or 0, item["subject"]))
    return rows


def _vip_time_range(value: float | None) -> str:
    if value is None:
        return "unknown"
    if value < 20:
        return "green"
    if value < 45:
        return "blue"
    if value < 75:
        return "orange"
    return "red"


def _format_minutes_value(value: float | None) -> str:
    if value is None:
        return "-"
    return f"{value:.0f} min"


def _format_score(value: float | None) -> str:
    if value is None:
        return "-"
    return f"{value:.3f}"


def _build_vip_conclusions(
    *,
    total_os: int,
    total_installations: int,
    top_day: str,
    top_day_count: int,
    top_installation_day: str,
    top_installation_day_count: int,
    top_installer: dict[str, Any] | None,
    top_productivity: dict[str, Any] | None,
    fastest: dict[str, Any] | None,
    most_shift: dict[str, Any] | None,
    subject_execution_times: list[dict[str, Any]],
) -> list[str]:
    conclusions = []
    if total_os:
        conclusions.append(f"Dia com mais OS finalizadas: {top_day} com {top_day_count} OS ({(top_day_count / total_os) * 100:.1f}% do periodo).")
    else:
        conclusions.append("Nenhuma OS finalizada encontrada para os filtros selecionados.")
    conclusions.append(f"Instalacoes no periodo: {total_installations}; pico em {top_installation_day} com {top_installation_day_count} instalacoes.")
    if top_installer:
        conclusions.append(f"Top instalador por score: {top_installer['technician']} com {top_installer['total']} instalacoes e score {_format_score(top_installer['score'])}.")
    if top_productivity:
        conclusions.append(f"Maior score geral: {top_productivity['technician']} com {top_productivity['orders_per_day']:.2f} OS/dia.")
    if fastest:
        conclusions.append(f"Melhor mediana de execucao: {fastest['technician']} com {_format_minutes_value(fastest.get('median_minutes'))}.")
    if most_shift:
        conclusions.append(f"Turno mais produtivo: {most_shift['label']} com {most_shift['orders']} OS ({most_shift['percentage']:.0f}%).")
    if subject_execution_times:
        fastest_subject = subject_execution_times[0]
        slowest_subject = subject_execution_times[-1]
        conclusions.append(f"Tipo de OS mais rapido: {fastest_subject['subject']} com mediana de {_format_minutes_value(fastest_subject['median_minutes'])}.")
        if slowest_subject != fastest_subject:
            conclusions.append(f"Tipo de OS mais demorado: {slowest_subject['subject']} com mediana de {_format_minutes_value(slowest_subject['median_minutes'])}.")
    return conclusions


def _resolve_shift_key(value: datetime) -> str:
    hour = value.hour
    if 6 <= hour < 12:
        return "morning"
    if 12 <= hour < 18:
        return "afternoon"
    return "night"


def _build_productivity_by_shift(
    by_shift: dict[str, int],
    total_finished: int,
) -> list[dict[str, Any]]:
    shifts = (
        ("morning", "Manha", "06h-12h"),
        ("afternoon", "Tarde", "12h-18h"),
        ("night", "Noite", "18h-00h"),
    )
    result: list[dict[str, Any]] = []
    for key, label, period in shifts:
        count = int(by_shift.get(key, 0))
        result.append(
            {
                "key": key,
                "label": label,
                "period": period,
                "finished_orders": count,
                "percentage": round((count / total_finished) * 100, 2)
                if total_finished
                else 0.0,
            }
        )
    return result


def _build_installations_by_day(
    period_start: date,
    period_end: date,
    by_day: dict[date, int],
) -> list[dict[str, Any]]:
    return _build_finished_by_day(period_start, period_end, by_day)


def _build_installations_by_technician(
    by_technician: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    rows = [
        {
            "technician": str(bucket["technician"]),
            "installations": int(bucket["installations"]),
        }
        for bucket in by_technician.values()
    ]
    rows.sort(key=lambda item: (item["installations"], item["technician"]), reverse=True)
    return rows


def _build_technician_productivity_ranking(
    by_technician: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for bucket in by_technician.values():
        total_orders = int(bucket["total_orders"])
        active_days = len(bucket["_active_days"])
        execution_values = list(bucket["_execution_minutes"])
        orders_per_day = round(total_orders / active_days, 2) if active_days else 0.0
        rows.append(
            {
                "technician": str(bucket["technician"]),
                "total_orders": total_orders,
                "installations": int(bucket["installations"]),
                "active_days": active_days,
                "orders_per_day": orders_per_day,
                "avg_execution_minutes": _avg(execution_values),
                "median_execution_minutes": _median(execution_values),
            }
        )
    rows.sort(
        key=lambda item: (
            item["orders_per_day"],
            item["total_orders"],
            item["installations"],
            -float(item["median_execution_minutes"] or 999999),
            item["technician"],
        ),
        reverse=True,
    )
    return rows


def _build_median_execution_by_subject(
    by_subject: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for bucket in by_subject.values():
        execution_values = list(bucket["_execution_minutes"])
        if not execution_values:
            continue
        rows.append(
            {
                "subject": str(bucket["subject"]),
                "orders": int(bucket["orders"]),
                "orders_with_execution": len(execution_values),
                "avg_execution_minutes": _avg(execution_values),
                "median_execution_minutes": _median(execution_values),
            }
        )
    rows.sort(
        key=lambda item: (
            float(item["median_execution_minutes"] or 0),
            item["orders_with_execution"],
            item["subject"],
        )
    )
    return rows


def _weekday_name_pt(value: date) -> str:
    names = (
        "Segunda",
        "Terca",
        "Quarta",
        "Quinta",
        "Sexta",
        "Sabado",
        "Domingo",
    )
    return names[value.weekday()]


def _weekday_short_name_pt(value: date) -> str:
    names = ("Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom")
    return names[value.weekday()]


def _resolve_subject_name(row: dict[str, Any]) -> str:
    text = str(row.get("subject_name") or "").strip()
    if text:
        return text
    raw_payload = row.get("raw_payload") if isinstance(row.get("raw_payload"), dict) else {}
    for key in ("assunto", "descricao_assunto", "descricao"):
        value = raw_payload.get(key)
        if value is None:
            continue
        candidate = " ".join(str(value).split()).strip()
        if candidate:
            return candidate
    return ""


def _normalize_matching_text(value: str | None) -> str:
    raw = str(value or "").strip().lower()
    normalized = unicodedata.normalize("NFKD", raw)
    ascii_only = "".join(char for char in normalized if not unicodedata.combining(char))
    return " ".join(ascii_only.split())


def _subject_matches_pattern(normalized_subject: str, normalized_pattern: str) -> bool:
    if not normalized_subject or not normalized_pattern:
        return False
    if normalized_subject == normalized_pattern:
        return True
    return len(normalized_pattern) >= 4 and normalized_pattern in normalized_subject


def _normalize_card_metric(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = str(value).strip().lower()
    allowed = {
        "completed_today",
        "active_orders",
        "within_sla",
        "overdue",
        "technicians_in_execution",
        "orders_started",
        "rescheduled_today",
        "avg_execution",
    }
    if normalized not in allowed:
        return None
    return normalized


def _card_metric_label(metric_key: str) -> str:
    labels = {
        "completed_today": "OS efetuadas no dia",
        "active_orders": "OS ativas",
        "within_sla": "Dentro do SLA",
        "overdue": "Fora do SLA",
        "technicians_in_execution": "Tecnicos em execucao",
        "orders_started": "OS iniciadas pelos tecnicos",
        "rescheduled_today": "OS reagendadas no dia",
        "avg_execution": "Tempo medio de execucao",
    }
    return labels.get(metric_key, metric_key)


def _date_to_str(value: date | None) -> str | None:
    return str(value) if value else None


def _normalize_status_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip().upper()


def _is_execution_status(status: str, configured_execution_set: set[str]) -> bool:
    normalized = _normalize_status_text(status)
    if not normalized:
        return False
    if normalized in configured_execution_set:
        return True
    fallback_statuses = {
        "EN",
        "EX",
        "ENCAMINHADO",
        "EM EXECUCAO",
        "EM-EXECUCAO",
        "EM_EXECUCAO",
        "EM ANDAMENTO",
        "EM_ANDAMENTO",
    }
    return normalized in fallback_statuses


def _resolve_order_datetimes(
    row: dict[str, Any],
    raw_payload: dict[str, Any],
) -> tuple[datetime | None, datetime | None, datetime | None, datetime | None]:
    opened_at = _parse_local_datetime(row.get("opened_at"))
    execution_started_at = _extract_execution_datetime(row, raw_payload)
    closed_at = _parse_local_datetime(row.get("closed_at"))
    due_at = _parse_local_datetime(row.get("due_at"))

    opened_at = opened_at or _extract_datetime_from_raw(
        raw_payload,
        [
            "data_abertura",
            "data_hora_abertura",
            "abertura",
        ],
    )
    closed_at = closed_at or _extract_datetime_from_raw(
        raw_payload,
        [
            "data_fechamento",
            "data_encerramento",
            "data_final",
            "fechamento",
        ],
    )
    due_at = due_at or _extract_datetime_from_raw(
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
    )

    return opened_at, execution_started_at, closed_at, due_at


def _extract_datetime_from_raw(raw_payload: dict[str, Any], keys: list[str]) -> datetime | None:
    if not raw_payload:
        return None
    for key in keys:
        parsed = _parse_flexible_datetime(raw_payload.get(key))
        if parsed is not None:
            return parsed
    return None


def _extract_rescheduled_datetime(raw_payload: dict[str, Any]) -> datetime | None:
    explicit = _extract_datetime_from_raw(
        raw_payload,
        [
            "data_reagendamento",
            "data_hora_reagendamento",
            "dt_reagendamento",
            "reagendada_para",
        ],
    )
    if explicit is not None:
        return explicit
    return _extract_message_event_datetime(
        raw_payload,
        status_tokens={"REAGENDADA"},
        text_patterns=("reagendada", "reagendado", "reagendamento"),
    )


def _extract_scheduled_datetime(raw_payload: dict[str, Any]) -> datetime | None:
    return _extract_datetime_from_raw(
        raw_payload,
        [
            "data_agenda",
            "data_agendamento",
            "data_agenda_inicial",
            "data_agendamento_inicial",
            "data_hora_agenda",
            "data_hora_agendamento",
            "data_agenda_final",
            "agendada_para",
            "previsao_inicio",
            "dt_agendamento",
        ],
    )


def _is_rescheduled_on_date(
    *,
    status: str,
    rescheduled_at: datetime | None,
    scheduled_at: datetime | None,
    target_date: date,
) -> bool:
    normalized_status = _normalize_status_text(status)
    rescheduled_statuses = {"AG", "AGENDA", "AGENDADA", "REAGENDADA", "REAGENDADO", "R", "PENDENTE"}
    if rescheduled_at is not None:
        return rescheduled_at.date() == target_date
    return normalized_status in rescheduled_statuses and scheduled_at is not None and scheduled_at.date() == target_date


def _extract_execution_datetime(
    row: dict[str, Any],
    raw_payload: dict[str, Any],
) -> datetime | None:
    normalized_status = _normalize_status_text(row.get("status"))
    if normalized_status in {"AG", "AGENDA", "AGENDADA", "REAGENDADA", "PENDENTE"}:
        return None

    row_execution = _parse_local_datetime(row.get("execution_started_at"))
    if row_execution is not None:
        return row_execution

    explicit_execution = _extract_datetime_from_raw(
        raw_payload,
        [
            "data_hora_execucao",
            "data_inicio_execucao",
            "inicio_execucao",
        ],
    )
    if explicit_execution is not None:
        return explicit_execution

    return _extract_message_event_datetime(
        raw_payload,
        status_tokens={"EX", "EXECUTADA", "EXECUTADO", "EXECUCAO", "EM_EXECUCAO", "EM_ANDAMENTO"},
        text_patterns=(
            "executada",
            "executado",
            "execucao",
            "execução",
            "o.s. executada pelo tecnico",
            "o.s. executada pelo técnico",
            "inmap service",
        ),
    )


def _is_closed(
    *,
    status: str,
    closed_at: datetime | None,
    closed_statuses: set[str],
) -> bool:
    return status in closed_statuses


def _evaluate_sla(
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


def _sla_label_text(
    value: str,
    *,
    due_at: datetime | None = None,
    closed_at: datetime | None = None,
    now_local: datetime | None = None,
    is_closed: bool | None = None,
) -> str:
    if value == "no_due":
        return "Sem prazo"
    order_closed = bool(closed_at is not None) if is_closed is None else is_closed
    if not order_closed and due_at is not None:
        reference = now_local or datetime.now()
        if due_at >= reference:
            remaining_minutes = int((due_at - reference).total_seconds() // 60)
            return f"Restam {_format_duration_minutes(remaining_minutes)}"
        overdue_minutes = int((reference - due_at).total_seconds() // 60)
        return f"Atrasada {_format_duration_minutes(overdue_minutes)}"
    if value == "within":
        return "Dentro do SLA"
    if value == "overdue":
        return "Fora do SLA"
    return "Sem prazo"


def _format_duration_minutes(value: int) -> str:
    total = max(0, int(value))
    days, remaining = divmod(total, 1440)
    hours, minutes = divmod(remaining, 60)
    if days:
        if hours:
            return f"{days}d {hours}h"
        return f"{days}d"
    if hours:
        if minutes:
            return f"{hours}h {minutes}min"
        return f"{hours}h"
    return f"{minutes}min"


def _matches_card_metric(
    *,
    metric_key: str,
    target_date: date,
    status: str,
    is_closed: bool,
    closed_at: datetime | None,
    in_execution: bool,
    execution_started_at: datetime | None,
    execution_minutes: float | None,
    rescheduled_at: datetime | None,
    scheduled_at: datetime | None,
    sla_status: str,
) -> bool:
    if metric_key == "completed_today":
        return bool(is_closed and closed_at and closed_at.date() == target_date)
    if metric_key == "active_orders":
        return not is_closed
    if metric_key == "within_sla":
        return sla_status == "within"
    if metric_key == "overdue":
        return sla_status == "overdue"
    if metric_key == "technicians_in_execution":
        return in_execution
    if metric_key == "orders_started":
        return execution_started_at is not None
    if metric_key == "rescheduled_today":
        return _is_rescheduled_on_date(
            status=_normalize_status_text(status),
            rescheduled_at=rescheduled_at,
            scheduled_at=scheduled_at,
            target_date=target_date,
        )
    if metric_key == "avg_execution":
        return execution_minutes is not None
    return False


def _parse_local_datetime(value: str | None) -> datetime | None:
    if value is None:
        return None
    raw = value.strip()
    if not raw:
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(raw, fmt)
        except ValueError:
            continue
    try:
        parsed = datetime.fromisoformat(raw)
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


def _avg(values: list[float]) -> float | None:
    if not values:
        return None
    return round(sum(values) / len(values), 2)


def _median(values: list[float]) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    midpoint = len(ordered) // 2
    if len(ordered) % 2:
        return round(ordered[midpoint], 2)
    return round((ordered[midpoint - 1] + ordered[midpoint]) / 2, 2)


def _time_only(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.strftime("%H:%M")


def _datetime_to_text(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.strftime("%Y-%m-%d %H:%M:%S")


def _parse_flexible_datetime(value: Any) -> datetime | None:
    if value is None:
        return None
    raw = str(value).strip()
    if not raw:
        return None

    variants = [
        raw,
        raw.replace("T", " ").replace("Z", ""),
        raw.replace("/", "-"),
    ]
    formats = (
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
        "%d-%m-%Y %H:%M:%S",
        "%d-%m-%Y %H:%M",
        "%d-%m-%Y",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y %H:%M",
        "%d/%m/%Y",
        "%H:%M:%S",
        "%H:%M",
    )
    for variant in variants:
        for fmt in formats:
            try:
                return datetime.strptime(variant, fmt)
            except ValueError:
                continue

    try:
        parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        return parsed.replace(tzinfo=None)
    except ValueError:
        return None


def _extract_displacement_datetime(
    raw_payload: dict[str, Any],
    row: dict[str, Any] | None = None,
) -> datetime | None:
    def _first_valid(keys: list[str]) -> datetime | None:
        for source in (raw_payload or {}, row or {}):
            for key in keys:
                parsed = _parse_flexible_datetime(source.get(key))
                if parsed is not None:
                    return parsed
        return None

    explicit_displacement_keys = [
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
    for item in messages:
        if not isinstance(item, dict):
            continue
        status = _normalize_status_text(item.get("status"))
        text = _normalize_matching_text(
            " ".join(
                str(item.get(key) or "").strip()
                for key in ("mensagem", "historico")
            )
        )
        if status not in status_tokens and not any(pattern in text for pattern in normalized_patterns):
            continue
        parsed = _parse_flexible_datetime(item.get("data"))
        if parsed is not None:
            return parsed
    return None


def _extract_technician_message(raw_payload: dict[str, Any]) -> str | None:
    if not raw_payload:
        return None
    preferred_keys: list[tuple[str, str | None]] = [
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
    messages: list[str] = []
    for key, label in preferred_keys:
        value = raw_payload.get(key)
        if value is None:
            continue
        text = " ".join(str(value).split())
        if not text or text in seen_values:
            continue
        seen_values.add(text)
        if label:
            messages.append(f"{label}: {text}")
        else:
            messages.append(text)
    if not messages:
        return None
    return " | ".join(messages)


def _extract_customer_name(raw_payload: dict[str, Any], row: dict[str, Any]) -> str:
    from_row = str(row.get("customer_name") or "").strip()
    if from_row:
        return from_row
    keys = [
        "cliente",
        "nome_cliente",
        "razao",
        "razao_social",
        "nome_razao",
        "assinante",
    ]
    for key in keys:
        value = raw_payload.get(key)
        if value is None:
            continue
        text = " ".join(str(value).split()).strip()
        if text and text.lower() not in {"null", "none"}:
            return text
    return ""


def _finalize_technician_metrics(bucket: dict[str, Any]) -> dict[str, Any]:
    within = int(bucket["within_sla"])
    overdue = int(bucket["overdue"])
    sla_denominator = within + overdue
    sla_rate = round((within / sla_denominator) * 100, 2) if sla_denominator else 100.0

    return {
        "technician_id": bucket["technician_id"],
        "technician": bucket["technician"],
        "total_orders": bucket["total_orders"],
        "started_orders": bucket["started_orders"],
        "closed_orders": bucket["closed_orders"],
        "open_orders": max(int(bucket["total_orders"]) - int(bucket["closed_orders"]), 0),
        "in_execution": bucket["in_execution"],
        "within_sla": within,
        "overdue": overdue,
        "no_due": bucket["no_due"],
        "sla_rate": sla_rate,
        "avg_response_minutes": _avg(bucket["_response_minutes"]),
        "avg_execution_minutes": _avg(bucket["_execution_minutes"]),
        "avg_total_minutes": _avg(bucket["_total_minutes"]),
        "order_ids_sample": bucket["_os_ids"],
    }
