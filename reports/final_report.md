# Final Project Report

This is the short report for **Pharma Commercial Analytics**.

The project uses generated public data, so treat the results as proof of the build, not real business results.

## What This Run Did

1. Made 25,000 pharma-style sales rows.
2. Cleaned the rows and checked the fields.
3. Built monthly category tables.
4. Tested forecast models.
5. Grouped categories with K-means.
6. Compared campaign and non-campaign rows.
7. Created charts, dashboard views, and CSV evidence files.

## Main Numbers

| Item | Value |
|---|---:|
| Rows | 25,000 |
| Categories | 57 |
| Regions | 5 |
| Channels | 5 |
| Monthly category rows | 1,354 |
| Best forecast model | linear_regression |
| Naive RMSE | 18,373.13 |
| Best RMSE | 14,687.75 |
| RMSE drop vs naive | 20.06% |
| K-means segments | 4 |
| 4-cluster silhouette | 0.4036 |

## Files To Check

- `outputs/metrics/run_summary.csv`
- `outputs/metrics/forecast_model_metrics.csv`
- `outputs/metrics/forecast_split_summary.csv`
- `outputs/tables/segment_profiles.csv`
- `outputs/metrics/campaign_comparison_ci.csv`
- `dashboards/screenshots/executive_dashboard.svg`

## Key Limit

The data is generated.

So don't read this as:

> "This improved real pharma revenue."

Read it as:

> "This shows I can build and explain a full commercial analytics project."
