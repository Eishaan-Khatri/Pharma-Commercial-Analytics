from __future__ import annotations

import html
from pathlib import Path

import pandas as pd


COLORS = ["#1D4ED8", "#B45309", "#047857", "#7C3AED", "#DC2626", "#0F766E"]


def _fmt(value: float) -> str:
    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    if abs(value) >= 1_000:
        return f"{value / 1_000:.1f}K"
    return f"{value:.1f}"


def _write_svg(path: Path, width: int, height: int, body: str, title: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#ffffff"/>
  <text x="24" y="34" font-family="Arial" font-size="20" font-weight="700" fill="#111827">{html.escape(title)}</text>
  {body}
</svg>
"""
    path.write_text(svg, encoding="utf-8")


def _scale(value: float, min_value: float, max_value: float, out_min: float, out_max: float) -> float:
    if max_value == min_value:
        return (out_min + out_max) / 2
    return out_min + (value - min_value) * (out_max - out_min) / (max_value - min_value)


def _line_chart(points, x0, y0, width, height, color, label) -> str:
    values = [p[1] for p in points]
    min_v, max_v = min(values), max(values)
    coords = []
    for i, (_, value) in enumerate(points):
        x = x0 + (i / max(len(points) - 1, 1)) * width
        y = _scale(value, min_v, max_v, y0 + height, y0)
        coords.append((x, y))
    polyline = " ".join(f"{x:.1f},{y:.1f}" for x, y in coords)
    circles = "\n".join(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="{color}"/>' for x, y in coords
    )
    return f"""
    <polyline points="{polyline}" fill="none" stroke="{color}" stroke-width="2.5"/>
    {circles}
    <text x="{x0}" y="{y0 - 8}" font-family="Arial" font-size="12" fill="{color}">{html.escape(label)}</text>
    <text x="{x0}" y="{y0 + height + 18}" font-family="Arial" font-size="11" fill="#6B7280">{html.escape(str(points[0][0]))}</text>
    <text x="{x0 + width - 56}" y="{y0 + height + 18}" font-family="Arial" font-size="11" fill="#6B7280">{html.escape(str(points[-1][0]))}</text>
    """


def _bar_chart(labels, values, x0, y0, width, height, color="#1D4ED8", horizontal=True) -> str:
    max_v = max(values) if values else 1
    body = []
    if horizontal:
        bar_h = min(28, height / max(len(values), 1) - 6)
        for i, (label, value) in enumerate(zip(labels, values)):
            y = y0 + i * (bar_h + 7)
            w = (value / max_v) * width
            body.append(f'<text x="{x0}" y="{y + bar_h * 0.75:.1f}" font-family="Arial" font-size="11" fill="#374151">{html.escape(str(label)[:28])}</text>')
            body.append(f'<rect x="{x0 + 180}" y="{y:.1f}" width="{w:.1f}" height="{bar_h:.1f}" fill="{color}" rx="3"/>')
            body.append(f'<text x="{x0 + 186 + w:.1f}" y="{y + bar_h * 0.75:.1f}" font-family="Arial" font-size="10" fill="#6B7280">{_fmt(float(value))}</text>')
    else:
        bar_w = min(70, width / max(len(values), 1) - 12)
        for i, (label, value) in enumerate(zip(labels, values)):
            x = x0 + i * (bar_w + 14)
            h = (value / max_v) * height
            body.append(f'<rect x="{x:.1f}" y="{y0 + height - h:.1f}" width="{bar_w:.1f}" height="{h:.1f}" fill="{color}" rx="3"/>')
            body.append(f'<text x="{x:.1f}" y="{y0 + height + 16}" font-family="Arial" font-size="10" fill="#6B7280" transform="rotate(20 {x:.1f},{y0 + height + 16})">{html.escape(str(label)[:16])}</text>')
    return "\n".join(body)


def plot_revenue_trend(df: pd.DataFrame, path) -> None:
    monthly = df.groupby("month", as_index=False).agg(net_sales=("net_sales", "sum"))
    points = list(zip(monthly["month"], monthly["net_sales"]))
    body = _line_chart(points, 60, 70, 760, 260, COLORS[0], "Net sales")
    _write_svg(Path(path), 900, 390, body, "Monthly Net Sales Trend")


def plot_top_categories(df: pd.DataFrame, path) -> None:
    top = (
        df.groupby("drug_category", as_index=False)
        .agg(net_sales=("net_sales", "sum"))
        .sort_values("net_sales", ascending=False)
        .head(12)
    )
    body = _bar_chart(top["drug_category"].tolist(), top["net_sales"].tolist(), 28, 70, 560, 300, COLORS[1])
    _write_svg(Path(path), 900, 430, body, "Top Drug Categories By Net Sales")


def plot_forecast(predictions: pd.DataFrame, path) -> None:
    sample = predictions.groupby("month", as_index=False).agg(
        actual_sales=("actual_sales", "sum"),
        ridge_regression=("ridge_regression", "sum"),
        moving_average_3=("moving_average_3", "sum"),
    )
    body = ""
    body += _line_chart(list(zip(sample["month"], sample["actual_sales"])), 60, 75, 760, 230, COLORS[0], "Actual")
    body += _line_chart(list(zip(sample["month"], sample["ridge_regression"])), 60, 75, 760, 230, COLORS[2], "Ridge")
    body += _line_chart(list(zip(sample["month"], sample["moving_average_3"])), 60, 75, 760, 230, COLORS[1], "Moving average")
    _write_svg(Path(path), 900, 370, body, "Forecast vs Actual Net Sales")


def plot_segment_profiles(profiles: pd.DataFrame, path) -> None:
    body = _bar_chart(
        profiles["segment_label"].tolist(),
        profiles["total_net_sales"].tolist(),
        28,
        70,
        560,
        280,
        COLORS[2],
    )
    _write_svg(Path(path), 900, 400, body, "Average Revenue By Segment")


def plot_campaign_comparison(summary: pd.DataFrame, path) -> None:
    body = _bar_chart(
        summary["campaign_flag"].tolist(),
        summary["avg_net_sales"].tolist(),
        80,
        80,
        500,
        240,
        COLORS[3],
        horizontal=False,
    )
    _write_svg(Path(path), 760, 400, body, "Campaign vs Non-Campaign Average Sale")


def create_dashboard_collage(df, metrics, profiles, ab_summary, dashboard_path) -> None:
    monthly = df.groupby("month", as_index=False).agg(net_sales=("net_sales", "sum"))
    top = (
        df.groupby("drug_category", as_index=False)
        .agg(net_sales=("net_sales", "sum"))
        .sort_values("net_sales", ascending=False)
        .head(6)
    )

    total_sales = df["net_sales"].sum()
    transactions = len(df)
    units = df["units_sold"].sum()
    avg_order = df["net_sales"].mean()

    cards = f"""
    <rect x="28" y="58" width="250" height="72" fill="#F9FAFB" stroke="#D1D5DB" rx="8"/>
    <text x="44" y="84" font-family="Arial" font-size="12" fill="#6B7280">Net Sales</text>
    <text x="44" y="112" font-family="Arial" font-size="24" font-weight="700" fill="#111827">{_fmt(total_sales)}</text>
    <rect x="298" y="58" width="250" height="72" fill="#F9FAFB" stroke="#D1D5DB" rx="8"/>
    <text x="314" y="84" font-family="Arial" font-size="12" fill="#6B7280">Transactions</text>
    <text x="314" y="112" font-family="Arial" font-size="24" font-weight="700" fill="#111827">{transactions:,}</text>
    <rect x="568" y="58" width="250" height="72" fill="#F9FAFB" stroke="#D1D5DB" rx="8"/>
    <text x="584" y="84" font-family="Arial" font-size="12" fill="#6B7280">Units Sold</text>
    <text x="584" y="112" font-family="Arial" font-size="24" font-weight="700" fill="#111827">{units:,}</text>
    <rect x="838" y="58" width="250" height="72" fill="#F9FAFB" stroke="#D1D5DB" rx="8"/>
    <text x="854" y="84" font-family="Arial" font-size="12" fill="#6B7280">Avg Order</text>
    <text x="854" y="112" font-family="Arial" font-size="24" font-weight="700" fill="#111827">{_fmt(avg_order)}</text>
    """

    trend = _line_chart(list(zip(monthly["month"], monthly["net_sales"])), 48, 190, 470, 190, COLORS[0], "Monthly sales")
    categories = _bar_chart(top["drug_category"].tolist(), top["net_sales"].tolist(), 590, 175, 310, 185, COLORS[1])
    model_bars = _bar_chart(metrics["model"].tolist(), metrics["RMSE"].tolist(), 60, 490, 400, 180, COLORS[2], horizontal=False)
    campaign_bars = _bar_chart(
        ab_summary["campaign_flag"].tolist(),
        ab_summary["avg_net_sales"].tolist(),
        620,
        490,
        300,
        180,
        COLORS[3],
        horizontal=False,
    )
    body = f"""
    {cards}
    <text x="48" y="165" font-family="Arial" font-size="16" font-weight="700" fill="#111827">Trend</text>
    {trend}
    <text x="590" y="165" font-family="Arial" font-size="16" font-weight="700" fill="#111827">Top Categories</text>
    {categories}
    <text x="60" y="465" font-family="Arial" font-size="16" font-weight="700" fill="#111827">Forecast RMSE</text>
    {model_bars}
    <text x="620" y="465" font-family="Arial" font-size="16" font-weight="700" fill="#111827">Campaign Comparison</text>
    {campaign_bars}
    """
    _write_svg(Path(dashboard_path), 1120, 760, body, "Pharma Commercial Analytics - Executive Dashboard")
