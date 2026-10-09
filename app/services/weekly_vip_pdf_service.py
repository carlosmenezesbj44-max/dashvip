from __future__ import annotations

from io import BytesIO
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np

VIP_PRIMARY = "#1B6B72"
VIP_DARK = "#124D52"
VIP_MEDIUM = "#2A8A92"
NAVY = "#0F2A44"
CARD_GREEN = "#22C55E"
CARD_BLUE = "#3B82F6"
CARD_ORANGE = "#F59E0B"
CARD_PURPLE = "#8B5CF6"
CARD_RED = "#EF4444"
TEXT_DARK = "#1F2937"
TEXT_MED = "#6B7280"

plt.rcParams["font.family"] = "DejaVu Sans"


def build_weekly_vip_pdf(report: dict[str, Any]) -> tuple[BytesIO, str]:
    buffer = BytesIO()
    with PdfPages(buffer) as pdf:
        _page_overview(pdf, report)
        _page_installations(pdf, report)
        _page_ranking(pdf, report)
        _page_times(pdf, report)
    buffer.seek(0)
    filename_label = report.get("period", {}).get("filename_label") or "periodo"
    return buffer, f"Relatorio_Semanal_VIP_{filename_label}.pdf"


def _add_header(fig, title: str, subtitle: str) -> None:
    ax = fig.add_axes([0, 0.92, 1, 0.08])
    ax.axis("off")
    ax.add_patch(Rectangle((0, 0), 1, 1, facecolor=NAVY, transform=ax.transAxes))
    ax.add_patch(Rectangle((0, 0), 1, 0.06, facecolor=VIP_PRIMARY, transform=ax.transAxes))
    ax.text(0.025, 0.62, "VIP TELECOM", fontsize=11, fontweight="bold", color="#9DCBD0", transform=ax.transAxes)
    ax.text(0.025, 0.25, title, fontsize=18, fontweight="bold", color="white", transform=ax.transAxes)
    ax.text(0.975, 0.4, subtitle, fontsize=10, color="#B8D4D8", ha="right", transform=ax.transAxes)


def _add_footer(fig, page_num: int, total_pages: int = 4) -> None:
    ax = fig.add_axes([0, 0, 1, 0.03])
    ax.axis("off")
    ax.text(0.025, 0.5, "Relatorio Operacional Semanal  •  VIP Telecom", fontsize=8, color=TEXT_MED, transform=ax.transAxes)
    ax.text(0.975, 0.5, f"Pagina {page_num} de {total_pages}", fontsize=8, color=TEXT_MED, ha="right", transform=ax.transAxes)


def _kpi_card(ax, x, y, w, h, color, value, label, sublabel="") -> None:
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.005,rounding_size=0.01", facecolor=color, edgecolor="none", transform=ax.transAxes))
    ax.add_patch(Rectangle((x, y), 0.005, h, facecolor="white", alpha=0.3, transform=ax.transAxes))
    ax.text(x + w / 2, y + h * 0.62, str(value), fontsize=22, fontweight="bold", color="white", ha="center", va="center", transform=ax.transAxes)
    ax.text(x + w / 2, y + h * 0.28, label, fontsize=9, color="white", ha="center", va="center", transform=ax.transAxes, fontweight="bold")
    if sublabel:
        ax.text(x + w / 2, y + h * 0.12, sublabel, fontsize=7.5, color="white", alpha=0.9, ha="center", va="center", transform=ax.transAxes)


def _short_name(value: str | None) -> str:
    text = str(value or "-").strip() or "-"
    parts = text.split()
    if len(parts) > 1:
        return f"{parts[0]} {parts[1][0]}."
    return text


def _format_minutes(value: Any) -> str:
    try:
        if value is None:
            return "-"
        return f"{float(value):.0f} min"
    except (TypeError, ValueError):
        return "-"


def _page_overview(pdf, report: dict[str, Any]) -> None:
    period = report.get("period", {})
    kpis = report.get("kpis", {})
    fig = plt.figure(figsize=(11.69, 8.27), facecolor="white")
    _add_header(fig, "Analise Semanal de Produtividade", f"Periodo: {period.get('label', '-')}")

    total_os = int(kpis.get("total_os") or 0)
    total_inst = int(kpis.get("total_installations") or 0)
    pct_inst = f"{(total_inst / total_os * 100):.1f}% do total" if total_os else "-"
    ax_kpi = fig.add_axes([0, 0.77, 1, 0.12]); ax_kpi.axis("off")
    _kpi_card(ax_kpi, 0.025, 0.1, 0.22, 0.85, CARD_GREEN, total_os, "OS FINALIZADAS", "Total do periodo")
    _kpi_card(ax_kpi, 0.26, 0.1, 0.22, 0.85, CARD_BLUE, total_inst, "INSTALACOES", pct_inst)
    _kpi_card(ax_kpi, 0.495, 0.1, 0.22, 0.85, CARD_ORANGE, kpis.get("top_day") or "-", "DIA MAIS PRODUTIVO", f"{kpis.get('top_day_orders') or 0} OS finalizadas")
    _kpi_card(ax_kpi, 0.73, 0.1, 0.245, 0.85, CARD_PURPLE, kpis.get("active_technicians") or 0, "TECNICOS ATIVOS", f"{kpis.get('timed_orders') or 0} OS cronometradas")

    per_day = report.get("per_day") or []
    days = [row["day"] for row in per_day]
    day_values = [int(row.get("orders") or 0) for row in per_day]
    ax1 = fig.add_axes([0.05, 0.42, 0.43, 0.30])
    colors = [VIP_PRIMARY if day == kpis.get("top_day") else "#9DCBD0" for day in days]
    bars = ax1.bar(days, day_values, color=colors, edgecolor="none", width=0.65)
    for bar, value in zip(bars, day_values):
        ax1.text(bar.get_x() + bar.get_width() / 2, value + 0.5, str(value), ha="center", va="bottom", fontsize=10, fontweight="bold", color=TEXT_DARK)
    _style_axis(ax1, "OS Finalizadas por Dia", "Quantidade de OS", max(day_values, default=0))

    shifts = [row for row in (report.get("shift_counts") or []) if row.get("key") != "no_start" and row.get("orders")]
    ax2 = fig.add_axes([0.55, 0.42, 0.43, 0.30])
    if shifts:
        labels = [row["label"] for row in shifts]
        values = [int(row["orders"]) for row in shifts]
        colors_map = {"Manha": CARD_ORANGE, "Tarde": CARD_BLUE, "Noite": CARD_PURPLE}
        wedges, _, _ = ax2.pie(values, labels=None, colors=[colors_map.get(label, VIP_MEDIUM) for label in labels], autopct="%1.1f%%", startangle=90, wedgeprops=dict(width=0.38, edgecolor="white", linewidth=3), pctdistance=0.82, textprops={"fontsize": 10, "fontweight": "bold", "color": "white"})
        ax2.text(0, 0.05, f"{sum(values)}", ha="center", va="center", fontsize=22, fontweight="bold", color=TEXT_DARK)
        ax2.text(0, -0.15, "OS", ha="center", va="center", fontsize=10, color=TEXT_MED)
        ax2.legend(wedges, [f"{label}: {value} OS" for label, value in zip(labels, values)], loc="center left", bbox_to_anchor=(1.0, 0.5), frameon=False, fontsize=9)
    ax2.set_title("Produtividade por Turno", fontsize=12, fontweight="bold", color=TEXT_DARK, loc="left", pad=10)

    shift_by_day = report.get("shift_by_day") or []
    ax3 = fig.add_axes([0.05, 0.06, 0.9, 0.27])
    day_labels = [row["day"] for row in shift_by_day]
    x = np.arange(len(day_labels))
    morning = np.array([int(row.get("morning") or 0) for row in shift_by_day])
    afternoon = np.array([int(row.get("afternoon") or 0) for row in shift_by_day])
    night = np.array([int(row.get("night") or 0) for row in shift_by_day])
    ax3.bar(x, morning, color=CARD_ORANGE, label="Manha", width=0.6)
    ax3.bar(x, afternoon, bottom=morning, color=CARD_BLUE, label="Tarde", width=0.6)
    ax3.bar(x, night, bottom=morning + afternoon, color=CARD_PURPLE, label="Noite", width=0.6)
    for i, total in enumerate(morning + afternoon + night):
        ax3.text(i, total + 0.5, str(int(total)), ha="center", va="bottom", fontsize=10, fontweight="bold", color=TEXT_DARK)
    ax3.set_xticks(x); ax3.set_xticklabels(day_labels)
    _style_axis(ax3, "Distribuicao Diaria por Turno", "Quantidade de OS", int(max(morning + afternoon + night, default=0)))
    ax3.legend(loc="upper right", frameon=False, fontsize=9, ncol=3)

    _add_footer(fig, 1)
    pdf.savefig(fig, dpi=150); plt.close(fig)


def _page_installations(pdf, report: dict[str, Any]) -> None:
    period = report.get("period", {})
    kpis = report.get("kpis", {})
    ranking = report.get("installation_ranking") or []
    fig = plt.figure(figsize=(11.69, 8.27), facecolor="white")
    _add_header(fig, "Ranking de Instalacoes", f"Periodo: {period.get('label', '-')}")
    ax_hl = fig.add_axes([0, 0.77, 1, 0.12]); ax_hl.axis("off")
    _kpi_card(ax_hl, 0.025, 0.1, 0.18, 0.85, VIP_PRIMARY, kpis.get("total_installations") or 0, "INSTALACOES", "Periodo")
    _kpi_card(ax_hl, 0.215, 0.1, 0.18, 0.85, CARD_GREEN, kpis.get("top_installation_day") or "-", "DIA + INST.", f"{kpis.get('top_installation_day_orders') or 0} instalacoes")
    _kpi_card(ax_hl, 0.405, 0.1, 0.19, 0.85, CARD_BLUE, _short_name(kpis.get("top_installer")), "TOP INSTALADOR", f"{kpis.get('top_installer_orders') or 0} instalacoes")
    _kpi_card(ax_hl, 0.605, 0.1, 0.19, 0.85, CARD_ORANGE, _short_name(kpis.get("fastest_technician")), "MAIS RAPIDO", _format_minutes(kpis.get("fastest_median_minutes")))
    _kpi_card(ax_hl, 0.805, 0.1, 0.17, 0.85, CARD_PURPLE, len(ranking), "TECNICOS", "Com instalacao")

    inst_day = report.get("installations_per_day") or []
    ax_d = fig.add_axes([0.05, 0.44, 0.38, 0.28])
    days = [row["day"] for row in inst_day]
    values = [int(row.get("installations") or 0) for row in inst_day]
    bars = ax_d.bar(days, values, color=[CARD_GREEN if day == kpis.get("top_installation_day") else "#A7F3D0" for day in days], edgecolor="none", width=0.65)
    for bar, value in zip(bars, values):
        ax_d.text(bar.get_x() + bar.get_width() / 2, value + 0.1, str(value), ha="center", va="bottom", fontsize=10, fontweight="bold", color=TEXT_DARK)
    _style_axis(ax_d, "Instalacoes por Dia", "Qtd", max(values, default=0))

    ax_t = fig.add_axes([0.50, 0.44, 0.46, 0.28])
    timed = [row for row in ranking if row.get("median_minutes") is not None][:8]
    names = [_short_name(row["technician"]) for row in timed]
    medians = [float(row.get("median_minutes") or 0) for row in timed]
    bars = ax_t.barh(names[::-1], medians[::-1], color=VIP_MEDIUM, edgecolor="none")
    for bar, value in zip(bars, medians[::-1]):
        ax_t.text(value + 1, bar.get_y() + bar.get_height() / 2, f"{value:.0f} min", va="center", fontsize=9, fontweight="bold", color=TEXT_DARK)
    _style_axis(ax_t, "Tempo Mediano por Instalacao", "Minutos", max(medians, default=0), axis="x")

    _ranking_table(fig, ranking, title="Ranking de Instalacoes — Score", columns=("total", "days", "installations_per_day"), y=0.03, h=0.37)
    _add_footer(fig, 2)
    pdf.savefig(fig, dpi=150); plt.close(fig)


def _page_ranking(pdf, report: dict[str, Any]) -> None:
    period = report.get("period", {})
    ranking = report.get("technician_ranking") or []
    fig = plt.figure(figsize=(11.69, 8.27), facecolor="white")
    _add_header(fig, "Ranking de Tecnicos — Produtividade e Tempo", f"Periodo: {period.get('label', '-')}")
    ax_leg = fig.add_axes([0.05, 0.84, 0.9, 0.05]); ax_leg.axis("off")
    ax_leg.add_patch(Rectangle((0, 0), 1, 1, facecolor="#F0F9FA", transform=ax_leg.transAxes))
    ax_leg.text(0.01, 0.55, "Score = 50% OS/dia + 30% eficiencia de tempo + 20% turno manha", fontsize=9, color=VIP_DARK, transform=ax_leg.transAxes, va="center", style="italic")
    _ranking_table(fig, ranking, title="Ranking Geral — Score", columns=("total", "days", "orders_per_day"), y=0.06, h=0.76)
    _add_footer(fig, 3)
    pdf.savefig(fig, dpi=150); plt.close(fig)


def _page_times(pdf, report: dict[str, Any]) -> None:
    period = report.get("period", {})
    fig = plt.figure(figsize=(11.69, 8.27), facecolor="white")
    _add_header(fig, "Tempos de Execucao e Conclusoes", f"Periodo: {period.get('label', '-')}")
    subject_times = (report.get("subject_execution_times") or [])[:12]
    ax = fig.add_axes([0.18, 0.38, 0.44, 0.43])
    labels = [str(row["subject"])[:28] for row in subject_times]
    values = [float(row.get("median_minutes") or 0) for row in subject_times]
    colors = [_range_color(row.get("range")) for row in subject_times]
    bars = ax.barh(labels[::-1], values[::-1], color=colors[::-1], edgecolor="none")
    for bar, value in zip(bars, values[::-1]):
        ax.text(value + 1.5, bar.get_y() + bar.get_height() / 2, f"{value:.0f} min", va="center", fontsize=9, color=TEXT_DARK)
    _style_axis(ax, "Tempo Mediano por Tipo de OS", "Minutos", max(values, default=0), axis="x")

    ax_cards = fig.add_axes([0.64, 0.38, 0.31, 0.43]); ax_cards.axis("off")
    ax_cards.text(0, 0.97, "Destaques Operacionais", fontsize=12, fontweight="bold", color=TEXT_DARK, transform=ax_cards.transAxes)
    y = 0.86
    colors_cards = [CARD_GREEN, CARD_BLUE, CARD_ORANGE, VIP_PRIMARY, CARD_PURPLE]
    for color, item in zip(colors_cards, report.get("highlights") or []):
        ax_cards.add_patch(FancyBboxPatch((0, y - 0.13), 1, 0.13, boxstyle="round,pad=0.005,rounding_size=0.015", facecolor=color, edgecolor="none", transform=ax_cards.transAxes))
        ax_cards.text(0.05, y - 0.04, item.get("label", ""), fontsize=8, color="white", fontweight="bold", transform=ax_cards.transAxes)
        ax_cards.text(0.22, y - 0.04, _short_name(item.get("title")), fontsize=11, color="white", fontweight="bold", transform=ax_cards.transAxes)
        ax_cards.text(0.22, y - 0.09, item.get("text", ""), fontsize=8.5, color="white", alpha=0.95, transform=ax_cards.transAxes)
        y -= 0.17

    ax_con = fig.add_axes([0.05, 0.05, 0.9, 0.28]); ax_con.axis("off")
    ax_con.text(0, 0.95, "Principais Conclusoes", fontsize=13, fontweight="bold", color=TEXT_DARK, transform=ax_con.transAxes)
    ax_con.add_patch(Rectangle((0, 0.91), 0.08, 0.008, facecolor=VIP_PRIMARY, transform=ax_con.transAxes))
    y = 0.82
    for conclusion in (report.get("conclusions") or [])[:8]:
        ax_con.text(0.01, y, f"• {conclusion}", fontsize=9.2, color=TEXT_DARK, transform=ax_con.transAxes, va="top")
        y -= 0.1
    _add_footer(fig, 4)
    pdf.savefig(fig, dpi=150); plt.close(fig)


def _ranking_table(fig, rows, *, title: str, columns: tuple[str, str, str], y: float, h: float) -> None:
    ax = fig.add_axes([0.05, y, 0.9, h]); ax.axis("off")
    ax.text(0, 0.97, title, fontsize=10, fontweight="bold", color=TEXT_DARK, transform=ax.transAxes)
    headers = ["#", "Tecnico", "Total", "Dias", "OS/dia", "T.Medio", "T.Mediano", "% Manha", "Score"]
    xs = [0.01, 0.05, 0.38, 0.46, 0.53, 0.62, 0.71, 0.80, 0.90]
    header_y = 0.86
    ax.add_patch(Rectangle((0, header_y - 0.05), 1, 0.085, facecolor=NAVY, transform=ax.transAxes))
    for header, x in zip(headers, xs):
        ax.text(x, header_y - 0.004, header, fontsize=8.5, fontweight="bold", color="white", transform=ax.transAxes, va="center")
    row_y = header_y - 0.11
    row_h = 0.085 if h > 0.5 else 0.11
    for index, row in enumerate(rows[:10], 1):
        if index % 2 == 0:
            ax.add_patch(Rectangle((0, row_y - row_h * 0.48), 1, row_h, facecolor="#F3F4F6", transform=ax.transAxes))
        productivity = row.get(columns[2])
        values = [index, str(row.get("technician") or "-")[:30], int(row.get(columns[0]) or 0), int(row.get(columns[1]) or 0), f"{float(productivity or 0):.2f}", _number_or_dash(row.get("avg_minutes")), _number_or_dash(row.get("median_minutes")), f"{float(row.get('morning_percentage') or 0):.0f}%", f"{float(row.get('score') or 0):.3f}"]
        for value, x in zip(values, xs):
            ax.text(x, row_y, str(value), fontsize=8.5, color=VIP_PRIMARY if index <= 3 and x in (xs[0], xs[8]) else TEXT_DARK, fontweight="bold" if index <= 3 else "normal", transform=ax.transAxes, va="center")
        row_y -= row_h


def _number_or_dash(value: Any) -> str:
    if value is None:
        return "-"
    return f"{float(value):.1f}"


def _range_color(value: str | None) -> str:
    return {"green": CARD_GREEN, "blue": CARD_BLUE, "orange": CARD_ORANGE, "red": CARD_RED}.get(value or "", VIP_MEDIUM)


def _style_axis(ax, title: str, ylabel: str, max_value: float, axis: str = "y") -> None:
    ax.set_title(title, fontsize=12, fontweight="bold", color=TEXT_DARK, loc="left", pad=10)
    if axis == "y":
        ax.set_ylabel(ylabel, fontsize=9, color=TEXT_MED)
        ax.set_ylim(0, max(max_value * 1.25, 1))
        ax.grid(axis="y", alpha=0.2, linestyle="--")
    else:
        ax.set_xlabel(ylabel, fontsize=9, color=TEXT_MED)
        ax.set_xlim(0, max(max_value * 1.3, 1))
        ax.grid(axis="x", alpha=0.2, linestyle="--")
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for spine in ["left", "bottom"]:
        ax.spines[spine].set_color("#E5E7EB")
    ax.tick_params(colors=TEXT_MED, labelsize=8)
    ax.set_axisbelow(True)
