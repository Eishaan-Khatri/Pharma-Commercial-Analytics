# Claim Ledger

This file keeps the project honest.

It answers one simple question:

> What can I safely say about this project, and what should I not say?

## What Came From The Older Project Notes

| Claim | Status |
|---|---|
| Project name: Pharma Commercial Analytics | safe |
| Older project note mentioned 600K+ transactions | safe if worded as "older project note mentioned" |
| Older project note mentioned 57 drug categories | safe |
| Methods included forecasting, segmentation, and campaign-style comparison | safe |
| Tools included Python, R, SQL, Tableau/Power BI | safe if talking about the original broader work |

## What This Public Repo Proves

| Item | What The Repo Shows |
|---|---|
| Generated sample data | 25,000 rows with pharma-style sales columns |
| Cleaning | duplicate checks, date parsing, numeric checks, derived fields |
| Forecasting | six model baselines with a time-based split |
| LightGBM | tested, but not the winning final-test model |
| Segmentation | 4 K-means groups with readable labels |
| Campaign comparison | comparison with a bootstrap range, not causal proof |
| Dashboard output | SVG dashboard files anyone can open |
| Resume evidence | exact CSVs under `outputs/metrics/` |

## Current Public Metrics

| Metric | Value | File |
|---|---:|---|
| Rows | 25,000 | `outputs/metrics/run_summary.csv` |
| Drug categories | 57 | `outputs/metrics/run_summary.csv` |
| Regions | 5 | `outputs/metrics/run_summary.csv` |
| Channels | 5 | `outputs/metrics/run_summary.csv` |
| Monthly category rows | 1,354 | `outputs/metrics/run_summary.csv` |
| Best final-test model | linear_regression | `outputs/metrics/forecast_model_metrics.csv` |
| Naive RMSE | 18,373.13 | `outputs/metrics/run_summary.csv` |
| Best RMSE | 14,687.75 | `outputs/metrics/run_summary.csv` |
| RMSE drop vs naive | 20.06% | `outputs/metrics/run_summary.csv` |
| Category segments | 4 | `outputs/metrics/run_summary.csv` |
| 4-cluster silhouette | 0.4036 | `outputs/metrics/run_summary.csv` |

## Safe Way To Describe It

Use:

> A pharma-style commercial analytics project using generated transaction data, with cleaning, KPI checks, forecasting, segmentation, campaign comparison, and dashboard reporting.

## Don't Say These

Don't claim:

- real pharma revenue impact,
- patient-level data,
- clinical insight,
- live company deployment,
- campaign lift,
- LightGBM as the best model,
- company outcomes from the generated sample data.

## Why This Matters

Recruiters can forgive synthetic data.

They won't forgive fake certainty.

This repo is stronger when the claims are careful.
