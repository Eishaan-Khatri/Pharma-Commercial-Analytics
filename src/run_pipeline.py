from __future__ import annotations

import argparse

import pandas as pd

from src.ab_analysis import run_ab_style_analysis
from src.config import (
    CLEAN_DATA_PATH,
    DASHBOARD_DIR,
    FIGURES_DIR,
    METRICS_DIR,
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
    create_dashboard_views,
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

    forecast_metrics, forecast_predictions, split_summary = run_forecasting(monthly)
    forecast_metrics.to_csv(TABLES_DIR / "forecast_model_metrics.csv", index=False)
    forecast_predictions.to_csv(TABLES_DIR / "forecast_predictions.csv", index=False)
    split_summary.to_csv(TABLES_DIR / "forecast_split_summary.csv", index=False)

    seg_features = make_segmentation_features(clean)
    cluster_scores, segmented, segment_profiles = run_segmentation(seg_features)
    cluster_scores.to_csv(TABLES_DIR / "cluster_selection_scores.csv", index=False)
    segmented.to_csv(TABLES_DIR / "category_segments.csv", index=False)
    segment_profiles.to_csv(TABLES_DIR / "segment_profiles.csv", index=False)

    ab_summary, ab_inference = run_ab_style_analysis(clean)
    ab_summary.to_csv(TABLES_DIR / "ab_style_group_summary.csv", index=False)
    ab_inference.to_csv(TABLES_DIR / "ab_style_inference.csv", index=False)

    naive_rmse = float(forecast_metrics.loc[forecast_metrics["model"] == "naive_last_period", "RMSE"].iloc[0])
    ridge_rmse = float(forecast_metrics.loc[forecast_metrics["model"] == "ridge_regression", "RMSE"].iloc[0])
    best_model = forecast_metrics.iloc[0]
    best_rmse = float(best_model["RMSE"])
    selected_k_row = cluster_scores[cluster_scores["k"] == 4].iloc[0]
    run_summary = pd.DataFrame(
        [
            {
                "sample_rows": len(sample),
                "clean_rows": len(clean),
                "drug_categories": clean["drug_category"].nunique(),
                "regions": clean["region"].nunique(),
                "channels": clean["channel"].nunique(),
                "monthly_category_rows": len(monthly),
                "best_forecast_model": best_model["model"],
                "naive_rmse": naive_rmse,
                "ridge_rmse": ridge_rmse,
                "best_rmse": best_rmse,
                "best_improvement_over_naive_pct": (naive_rmse - best_rmse) / naive_rmse * 100,
                "best_improvement_over_ridge_pct": (ridge_rmse - best_rmse) / ridge_rmse * 100,
                "business_selected_clusters": 4,
                "business_selected_kmeans_silhouette": selected_k_row["silhouette"],
            }
        ]
    )
    run_summary.to_csv(TABLES_DIR / "run_summary.csv", index=False)

    forecast_metrics.to_csv(METRICS_DIR / "forecast_model_metrics.csv", index=False)
    split_summary.to_csv(METRICS_DIR / "forecast_split_summary.csv", index=False)
    cluster_scores.to_csv(METRICS_DIR / "cluster_selection_scores.csv", index=False)
    ab_inference.to_csv(METRICS_DIR / "campaign_comparison_ci.csv", index=False)
    run_summary.to_csv(METRICS_DIR / "run_summary.csv", index=False)

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
    create_dashboard_views(
        clean,
        forecast_metrics,
        forecast_predictions,
        segment_profiles,
        ab_summary,
        ab_inference,
        DASHBOARD_DIR,
    )

    best_model = forecast_metrics.iloc[0]
    model_table = df_to_markdown(
        forecast_metrics[["model", "validation_RMSE", "MAE", "RMSE", "sMAPE", "selected_params"]].round(4)
    )
    split_table = df_to_markdown(split_summary)
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

Validation design: leakage-aware month-based split. Training uses older months,
validation uses the next chronological block, and testing uses the final months.

## Split Summary

{split_table}

## Model Comparison

{model_table}
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
- Forecast split summary: `outputs/tables/forecast_split_summary.csv`
- Segment profiles: `outputs/tables/segment_profiles.csv`
- A/B-style analysis: `outputs/tables/ab_style_inference.csv`
- Executive dashboard: `dashboards/screenshots/executive_dashboard.svg`
- Dashboard views: `dashboards/screenshots/executive_summary.svg`, `category_view.svg`, `forecast_view.svg`, `segment_view.svg`, `campaign_comparison_view.svg`
- Resume evidence metrics: `outputs/metrics/`

## Best Forecasting Model In Sample Run

{best_model['model']} with RMSE {best_model['RMSE']:,.2f}.

Naive baseline RMSE: {naive_rmse:,.2f}.

Best-model improvement over naive: {(naive_rmse - best_rmse) / naive_rmse * 100:,.2f}%.

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
