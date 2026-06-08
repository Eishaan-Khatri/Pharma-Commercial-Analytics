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


def _best_prediction_column(predictions: pd.DataFrame) -> str:
    for column in ["ridge_lightgbm_residual", "lightgbm", "ridge_regression", "linear_regression", "moving_average_3"]:
        if column in predictions.columns:
            return column
    return "naive_last_period"


def plot_forecast(predictions: pd.DataFrame, path) -> None:
    best_col = _best_prediction_column(predictions)
    sample = predictions.groupby("month", as_index=False).agg(
        actual_sales=("actual_sales", "sum"),
        best_forecast=(best_col, "sum"),
        moving_average_3=("moving_average_3", "sum"),
    )
    body = ""
    body += _line_chart(list(zip(sample["month"], sample["actual_sales"])), 60, 75, 760, 230, COLORS[0], "Actual")
    body += _line_chart(list(zip(sample["month"], sample["best_forecast"])), 60, 75, 760, 230, COLORS[2], best_col.replace("_", " ").title())
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


def create_dashboard_views(df, forecast_metrics, forecast_predictions, profiles, ab_summary, ab_inference, dashboard_dir) -> None:
    dashboard_dir = Path(dashboard_dir)
    _create_executive_summary_view(df, forecast_metrics, profiles, ab_inference, dashboard_dir / "executive_summary.svg")
    _create_category_view(df, profiles, dashboard_dir / "category_view.svg")
    _create_forecast_view(forecast_metrics, forecast_predictions, dashboard_dir / "forecast_view.svg")
    _create_segment_view(profiles, dashboard_dir / "segment_view.svg")
    _create_campaign_view(ab_summary, ab_inference, dashboard_dir / "campaign_comparison_view.svg")


def _create_executive_summary_view(df, metrics, profiles, ab_inference, path) -> None:
    best = metrics.iloc[0]
    total_sales = df["net_sales"].sum()
    body = f"""
    <rect x="30" y="62" width="250" height="86" fill="#F9FAFB" stroke="#D1D5DB" rx="8"/>
    <text x="48" y="91" font-family="Arial" font-size="12" fill="#6B7280">Rows</text>
    <text x="48" y="125" font-family="Arial" font-size="26" font-weight="700" fill="#111827">{len(df):,}</text>
    <rect x="305" y="62" width="250" height="86" fill="#F9FAFB" stroke="#D1D5DB" rx="8"/>
    <text x="323" y="91" font-family="Arial" font-size="12" fill="#6B7280">Net sales</text>
    <text x="323" y="125" font-family="Arial" font-size="26" font-weight="700" fill="#111827">{_fmt(total_sales)}</text>
    <rect x="580" y="62" width="250" height="86" fill="#F9FAFB" stroke="#D1D5DB" rx="8"/>
    <text x="598" y="91" font-family="Arial" font-size="12" fill="#6B7280">Best forecast</text>
    <text x="598" y="125" font-family="Arial" font-size="23" font-weight="700" fill="#111827">{html.escape(str(best['model']).replace('_', ' ').title())}</text>
    <rect x="855" y="62" width="250" height="86" fill="#F9FAFB" stroke="#D1D5DB" rx="8"/>
    <text x="873" y="91" font-family="Arial" font-size="12" fill="#6B7280">Best RMSE</text>
    <text x="873" y="125" font-family="Arial" font-size="26" font-weight="700" fill="#111827">{best['RMSE']:,.2f}</text>
    <text x="40" y="210" font-family="Arial" font-size="18" font-weight="700" fill="#111827">Executive summary</text>
    <text x="40" y="246" font-family="Arial" font-size="14" fill="#374151">This dashboard is generated from synthetic public data and proves the analytics workflow, not real pharma revenue impact.</text>
    <text x="40" y="278" font-family="Arial" font-size="14" fill="#374151">The pipeline cleans transactions, builds monthly category features, forecasts demand, segments categories, and compares campaign rows cautiously.</text>
    <text x="40" y="330" font-family="Arial" font-size="15" font-weight="700" fill="#111827">Segment labels</text>
    """
    y = 366
    for _, row in profiles.iterrows():
        body += f"""
        <rect x="42" y="{y - 20}" width="16" height="16" fill="{COLORS[int(row['cluster']) % len(COLORS)]}" rx="3"/>
        <text x="70" y="{y - 7}" font-family="Arial" font-size="13" fill="#374151">{html.escape(row['segment_label'])}: {int(row['categories'])} categories, avg sales {_fmt(float(row['total_net_sales']))}</text>
        """
        y += 30
    ci = ab_inference.iloc[0]
    body += f"""
    <text x="40" y="560" font-family="Arial" font-size="15" font-weight="700" fill="#111827">Campaign comparison boundary</text>
    <text x="40" y="590" font-family="Arial" font-size="13" fill="#374151">Observed avg-sale difference: {ci['observed_difference']:.2f}; 95% bootstrap CI [{ci['bootstrap_ci_95_low']:.2f}, {ci['bootstrap_ci_95_high']:.2f}]. Comparison only, not causal.</text>
    """
    _write_svg(Path(path), 1140, 660, body, "Executive Summary View")


def _create_category_view(df, profiles, path) -> None:
    top = (
        df.groupby("drug_category", as_index=False)
        .agg(net_sales=("net_sales", "sum"))
        .sort_values("net_sales", ascending=False)
        .head(12)
    )
    body = _bar_chart(top["drug_category"].tolist(), top["net_sales"].tolist(), 32, 74, 520, 330, COLORS[1])
    body += '<text x="640" y="78" font-family="Arial" font-size="15" font-weight="700" fill="#111827">Business segments</text>'
    y = 116
    for _, row in profiles.iterrows():
        body += f"""
        <rect x="640" y="{y - 22}" width="380" height="54" fill="#F9FAFB" stroke="#D1D5DB" rx="8"/>
        <text x="658" y="{y}" font-family="Arial" font-size="14" font-weight="700" fill="#111827">{html.escape(row['segment_label'])}</text>
        <text x="658" y="{y + 22}" font-family="Arial" font-size="12" fill="#6B7280">{int(row['categories'])} categories | avg sales {_fmt(float(row['total_net_sales']))} | growth {float(row['growth_rate']):.2%}</text>
        """
        y += 72
    _write_svg(Path(path), 1100, 470, body, "Category View")


def _create_forecast_view(metrics, predictions, path) -> None:
    best_col = _best_prediction_column(predictions)
    sample = predictions.groupby("month", as_index=False).agg(
        actual_sales=("actual_sales", "sum"),
        best_forecast=(best_col, "sum"),
    )
    body = _line_chart(list(zip(sample["month"], sample["actual_sales"])), 60, 78, 680, 210, COLORS[0], "Actual")
    body += _line_chart(list(zip(sample["month"], sample["best_forecast"])), 60, 78, 680, 210, COLORS[2], best_col.replace("_", " ").title())
    body += '<text x="60" y="350" font-family="Arial" font-size="15" font-weight="700" fill="#111827">Model RMSE comparison</text>'
    body += _bar_chart(metrics["model"].tolist(), metrics["RMSE"].tolist(), 60, 386, 660, 190, COLORS[3], horizontal=False)
    _write_svg(Path(path), 880, 640, body, "Forecast View")


def _create_segment_view(profiles, path) -> None:
    body = _bar_chart(profiles["segment_label"].tolist(), profiles["total_net_sales"].tolist(), 40, 84, 560, 300, COLORS[2])
    body += '<text x="670" y="86" font-family="Arial" font-size="15" font-weight="700" fill="#111827">Segment interpretation</text>'
    y = 126
    for _, row in profiles.iterrows():
        body += f"""
        <text x="670" y="{y}" font-family="Arial" font-size="14" font-weight="700" fill="#111827">{html.escape(row['segment_label'])}</text>
        <text x="670" y="{y + 22}" font-family="Arial" font-size="12" fill="#6B7280">Categories: {int(row['categories'])}; campaign share: {float(row['campaign_share']):.2%}; volatility: {_fmt(float(row['revenue_volatility']))}</text>
        """
        y += 72
    _write_svg(Path(path), 1120, 470, body, "Segment View")


def _create_campaign_view(summary, inference, path) -> None:
    body = _bar_chart(summary["campaign_flag"].tolist(), summary["avg_net_sales"].tolist(), 80, 84, 480, 240, COLORS[3], horizontal=False)
    ci = inference.iloc[0]
    body += f"""
    <text x="620" y="92" font-family="Arial" font-size="15" font-weight="700" fill="#111827">Causal honesty</text>
    <text x="620" y="130" font-family="Arial" font-size="13" fill="#374151">Observed difference: {float(ci['observed_difference']):.2f}</text>
    <text x="620" y="158" font-family="Arial" font-size="13" fill="#374151">95% bootstrap CI: [{float(ci['bootstrap_ci_95_low']):.2f}, {float(ci['bootstrap_ci_95_high']):.2f}]</text>
    <text x="620" y="202" font-family="Arial" font-size="13" fill="#374151">This is observational campaign comparison.</text>
    <text x="620" y="230" font-family="Arial" font-size="13" fill="#374151">It should not be presented as causal lift unless randomized assignment exists.</text>
    """
    _write_svg(Path(path), 1080, 420, body, "Campaign Comparison View")
