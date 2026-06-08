from __future__ import annotations

import argparse

import pandas as pd

from src.ab_analysis import run_ab_style_analysis
from src.config import (
    CLEAN_DATA_PATH,
    DASHBOARD_DIR,
    FIGURES_DIR,
    REPORTS_DIR,
    SAMPLE_DATA_PATH,
    TABLES_DIR,
    ensure_directories,
)
from src.data_cleaning import clean_transactions
from src.features import make_monthly_category_features, make_segmentation_features
from src.forecasting import run_forecasting
from src.generate_sample_data import generate_transactions
from src.segmentation import run_segmentation
from src.visualization import (
    create_dashboard_collage,
    plot_campaign_comparison,
    plot_forecast,
    plot_revenue_trend,
    plot_segment_profiles,
    plot_top_categories,
)


def write_markdown(path, title: str, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"# {title}\n\n{body.strip()}\n", encoding="utf-8")


def df_to_markdown(df: pd.DataFrame) -> str:
    headers = list(df.columns)
    rows = []
    rows.append("| " + " | ".join(headers) + " |")
    rows.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for _, row in df.iterrows():
        rows.append("| " + " | ".join(str(row[col]) for col in headers) + " |")
    return "\n".join(rows)


def run(rows: int = 25_000, force: bool = False) -> None:
    ensure_directories()

    if force or not SAMPLE_DATA_PATH.exists():
        sample = generate_transactions(rows=rows)
        sample.to_csv(SAMPLE_DATA_PATH, index=False)
    else:
        sample = pd.read_csv(SAMPLE_DATA_PATH)

    clean, quality = clean_transactions(sample)
    clean.to_csv(CLEAN_DATA_PATH, index=False)
    quality.to_csv(TABLES_DIR / "data_quality_report.csv", index=False)

    monthly = make_monthly_category_features(clean)
    monthly.to_csv(TABLES_DIR / "monthly_category_features.csv", index=False)

    forecast_metrics, forecast_predictions = run_forecasting(monthly)
    forecast_metrics.to_csv(TABLES_DIR / "forecast_model_metrics.csv", index=False)
    forecast_predictions.to_csv(TABLES_DIR / "forecast_predictions.csv", index=False)

    seg_features = make_segmentation_features(clean)
    cluster_scores, segmented, segment_profiles = run_segmentation(seg_features)
    cluster_scores.to_csv(TABLES_DIR / "cluster_selection_scores.csv", index=False)
    segmented.to_csv(TABLES_DIR / "category_segments.csv", index=False)
    segment_profiles.to_csv(TABLES_DIR / "segment_profiles.csv", index=False)

    ab_summary, ab_inference = run_ab_style_analysis(clean)
    ab_summary.to_csv(TABLES_DIR / "ab_style_group_summary.csv", index=False)
    ab_inference.to_csv(TABLES_DIR / "ab_style_inference.csv", index=False)

    plot_revenue_trend(clean, FIGURES_DIR / "monthly_revenue_trend.svg")
    plot_top_categories(clean, FIGURES_DIR / "top_categories.svg")
    plot_forecast(forecast_predictions, FIGURES_DIR / "forecast_vs_actual.svg")
    plot_segment_profiles(segment_profiles, FIGURES_DIR / "segment_profiles.svg")
    plot_campaign_comparison(ab_summary, FIGURES_DIR / "campaign_comparison.svg")
    create_dashboard_collage(
        clean,
        forecast_metrics,
        segment_profiles,
        ab_summary,
        DASHBOARD_DIR / "executive_dashboard.svg",
    )

    best_model = forecast_metrics.iloc[0]
    write_markdown(
        REPORTS_DIR / "eda_summary.md",
        "EDA Summary",
        f"""
Generated sample rows: {len(sample):,}

Clean rows used: {len(clean):,}

Drug categories: {clean['drug_category'].nunique()}

Date range: {clean['transaction_date'].min().date()} to {clean['transaction_date'].max().date()}

Total net sales in sample: {clean['net_sales'].sum():,.2f}

Top category by sample revenue: {clean.groupby('drug_category')['net_sales'].sum().idxmax()}
""",
    )
    write_markdown(
        REPORTS_DIR / "forecasting_results.md",
        "Forecasting Results",
        f"""
Best sample-run model by RMSE: {best_model['model']}

MAE: {best_model['MAE']:,.2f}

RMSE: {best_model['RMSE']:,.2f}

sMAPE: {best_model['sMAPE']:,.2f}%

Validation design: month-based holdout. This avoids random-split leakage across time.
""",
    )
    write_markdown(
        REPORTS_DIR / "segment_profiles.md",
        "Segment Profiles",
        df_to_markdown(segment_profiles),
    )
    write_markdown(
        REPORTS_DIR / "ab_style_analysis.md",
        "A/B-Style Campaign Comparison",
        f"""
This is comparison analysis, not causal inference.

{df_to_markdown(ab_summary)}

{df_to_markdown(ab_inference)}
""",
    )
    write_markdown(
        REPORTS_DIR / "final_report.md",
        "Final Project Report",
        f"""
This rebuilt project demonstrates a complete pharma commercial analytics workflow using synthetic public sample data.

## Workflow

1. Generate transaction-style sample data.
2. Clean and validate transaction fields.
3. Aggregate SQL-style business metrics.
4. Forecast month-category revenue.
5. Segment drug categories using K-means.
6. Compare campaign and non-campaign groups cautiously.
7. Generate dashboard-style screenshots and reports.

## Main Outputs

- Data quality report: `outputs/tables/data_quality_report.csv`
- Forecast metrics: `outputs/tables/forecast_model_metrics.csv`
- Segment profiles: `outputs/tables/segment_profiles.csv`
- A/B-style analysis: `outputs/tables/ab_style_inference.csv`
- Executive dashboard: `dashboards/screenshots/executive_dashboard.svg`

## Best Forecasting Model In Sample Run

{best_model['model']} with RMSE {best_model['RMSE']:,.2f}.

## Key Limitation

The data in this public repository is synthetic. It shows analytics workflow quality, not real pharma business outcomes.
""",
    )

    print("Pipeline complete.")
    print(f"Sample data: {SAMPLE_DATA_PATH}")
    print(f"Reports: {REPORTS_DIR}")
    print(f"Dashboard: {DASHBOARD_DIR / 'executive_dashboard.svg'}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the full pharma commercial analytics pipeline.")
    parser.add_argument("--rows", type=int, default=25_000, help="Rows to generate if sample data is absent.")
    parser.add_argument("--force", action="store_true", help="Regenerate sample data even if it already exists.")
    args = parser.parse_args()
    run(rows=args.rows, force=args.force)


if __name__ == "__main__":
    main()
