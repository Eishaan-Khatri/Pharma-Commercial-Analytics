# CV Bullet Bank

Use this file when you want to add **Pharma Commercial Analytics** to a resume.

The rule is simple:

> Only use a bullet if the repo has a file that backs it up.

## Best 3 Bullets

```text
- Built a pharma-style sales analytics project over 25,000 generated transaction rows across 57 categories, covering KPI checks, forecasting, segmentation, campaign comparison, and dashboard reporting.
- Compared six forecasting baselines with a time-based train/validation/test split; the best final-test model cut RMSE by 20.06% compared with the naive last-period baseline.
- Grouped 57 categories into four K-means segments: high-value growing, stable core, campaign-responsive, and low-volume niche; kept the campaign section comparison-only with a bootstrap confidence interval.
```

## Shorter Version

Use this if the resume is crowded.

```text
- Built a pharma-style analytics pipeline for KPI analysis, forecasting, K-means segmentation, campaign comparison, and dashboard reporting across 25,000 generated rows and 57 categories.
- Compared six forecast baselines with a no-peeking time split; best final-test RMSE was 14,687.75, which was 20.06% lower than naive.
- Created four readable category segments and clearly marked the campaign section as comparison-only.
```

## Best One-Line Version

```text
- Built a pharma-style analytics pipeline with KPI checks, six forecast baselines, 4-cluster K-means segmentation, campaign comparison, and dashboard reporting across 57 categories.
```

## Evidence Behind The Bullets

| Claim | Proof File |
|---|---|
| 25,000 rows | `outputs/metrics/run_summary.csv` |
| 57 categories | `outputs/metrics/run_summary.csv` |
| six forecast baselines | `outputs/metrics/forecast_model_metrics.csv` |
| time-based split | `outputs/metrics/forecast_split_summary.csv` |
| best RMSE 14,687.75 | `outputs/metrics/run_summary.csv` |
| 20.06% RMSE drop vs naive | `outputs/metrics/run_summary.csv` |
| 4 K-means segments | `outputs/tables/segment_profiles.csv` |
| campaign comparison interval | `outputs/metrics/campaign_comparison_ci.csv` |
| dashboard proof | `dashboards/screenshots/` |

## Data Science Resume Version

```text
- Built a commercial analytics project over generated pharma-style transaction data, including cleaning, KPI tables, monthly category features, forecast testing, segmentation, and dashboard outputs.
- Tested naive, moving-average, linear, ridge, LightGBM, and ridge-plus-LightGBM residual models with older months for training and later months for testing.
- Created four K-means category groups and used bootstrap intervals for campaign comparison while making clear that it was not a causal test.
```

## ML Engineer Resume Version

```text
- Rebuilt the project as a Python pipeline with separate modules for data generation, cleaning, features, forecasting, segmentation, comparison, reporting, and SVG dashboard output.
- Added an `outputs/metrics/` layer so each resume number can be traced to a CSV instead of being buried in a notebook.
- Compared simple and nonlinear forecast baselines, including LightGBM, while keeping the final claim tied to the actual winning model.
```

## Business Analytics Resume Version

```text
- Turned generated transaction-style sales data into category KPIs, forecast checks, segment profiles, campaign comparison tables, and executive dashboard views.
- Grouped categories into high-value growing, stable core, campaign-responsive, and low-volume niche segments for easier business review.
- Kept campaign results honest by reporting a bootstrap range and avoiding causal lift claims.
```

## What Not To Put On A Resume

Don't write:

- "improved pharma revenue",
- "used inside a live company system",
- "used patient-level data",
- "built clinical AI",
- "proved the campaign caused lift",
- "LightGBM won".

Those are not supported by the public repo.

## How To Defend The Project In 60 Seconds

Say:

> I rebuilt an older pharma commercial analytics project as a public repo. Since I didn't have the original raw files, I used generated sample data and kept the claims careful. The pipeline cleans rows, builds monthly category features, compares six forecast models with a time-based split, groups categories with K-means, compares campaign rows without claiming causality, and creates dashboard files. The main numbers are stored under `outputs/metrics/`.

## Why These Bullets Work

They show three things:

1. You can build the full pipeline, not just one notebook.
2. You can evaluate models without peeking into the future.
3. You know when **not** to overclaim.

That last point matters more than people think.
