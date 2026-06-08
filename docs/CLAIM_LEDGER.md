# Claim Ledger

This file separates what is confirmed from what is reconstructed.

## Confirmed From Portfolio/CV Evidence

| Claim | Status |
|---|---|
| Project title: Pharma Commercial Analytics | Confirmed |
| Dataset scale: 600K+ pharma transactions | Confirmed from portfolio/CV text |
| Category scale: 57 drug categories | Confirmed from portfolio/CV text |
| Methods: forecasting, segmentation, A/B-style analysis | Confirmed from portfolio/CV text |
| Models: linear/ridge regression, K-means clustering | Confirmed from portfolio/CV text |
| Tools: Python, R, SQL, Tableau/Power BI | Confirmed from portfolio/CV text |

## Reconstructed In This Public Repo

| Item | Status |
|---|---|
| Synthetic transaction data generator | Rebuilt for public reproducibility |
| SQL schema and business queries | Rebuilt from the documented project scope |
| Forecasting code | Rebuilt with chronological train/validation/test split and baseline comparisons |
| LightGBM forecasting baseline | Added in public rebuild and evaluated, but not the best final-test model |
| Ridge + LightGBM residual baseline | Added in public rebuild and evaluated, but not the best final-test model |
| Segmentation code | Rebuilt with 4 business-readable K-means profiles |
| A/B-style comparison code | Rebuilt as non-causal comparison analysis |
| Dashboard-style screenshots | Rebuilt from synthetic sample outputs |
| `outputs/metrics/` evidence layer | Added for exact CSV support behind resume claims |

## Current Public Sample Metrics

| Metric | Value | Source |
|---|---:|---|
| Public sample rows | 25,000 | `outputs/metrics/run_summary.csv` |
| Drug categories | 57 | `outputs/metrics/run_summary.csv` |
| Regions | 5 | `outputs/metrics/run_summary.csv` |
| Channels | 5 | `outputs/metrics/run_summary.csv` |
| Monthly category rows | 1,354 | `outputs/metrics/run_summary.csv` |
| Best final-test forecasting model | linear_regression | `outputs/metrics/forecast_model_metrics.csv` |
| Naive RMSE | 18,373.13 | `outputs/metrics/run_summary.csv` |
| Best RMSE | 14,687.75 | `outputs/metrics/run_summary.csv` |
| Improvement over naive | 20.06% | `outputs/metrics/run_summary.csv` |
| Business-selected K-means clusters | 4 | `outputs/metrics/run_summary.csv` |
| 4-cluster silhouette | 0.4036 | `outputs/metrics/run_summary.csv` |

## Claims To Avoid

- Do not claim clinical or patient-level analysis.
- Do not claim causal campaign impact.
- Do not claim production deployment.
- Do not claim revenue improvement.
- Do not claim the generated sample results are real business results.
- Do not lead with high model accuracy; the project is about analytics workflow quality.
- Do not say LightGBM was the best model in the current sample run; it was implemented and evaluated, but linear regression won on final-test RMSE.

## Safe Public Summary

> Rebuilt a pharma commercial analytics workflow using SQL, Python/R-style analysis, leakage-aware forecasting, segmentation, A/B-style comparison, and dashboard reporting over transaction-style sales data. The public repository uses synthetic sample data to demonstrate the original workflow safely, with exact resume-supporting metrics stored under `outputs/metrics/`.
