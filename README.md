# Pharma Commercial Analytics

Sales data can get messy fast.

You might have thousands of rows, many product groups, discounts, campaigns, regions, and channels. A manager doesn't want to stare at raw CSVs. They want to know:

- Which categories are doing well?
- Can we make a rough forecast for the next few months?
- Which groups of products behave alike?
- Did campaign rows look different from non-campaign rows?
- Can someone check the numbers without guessing?

That's what this repo is about.

**Pharma Commercial Analytics** is a rebuilt public version of an older pharma sales analytics project. The old project note mentioned `600K+` transactions across `57` categories. I don't have those raw files here, and I don't want to pretend I do. So this repo uses generated sample data with the same kind of columns and rebuilds the project in a way anyone can run and check.

No patient data.
No clinical claims.
No fake revenue-impact story.

Just a clean analytics project.

## What You Can Learn From This Repo

If you're a recruiter, reviewer, or someone checking my work, this repo shows that I can take messy business-style data and turn it into something readable.

It covers:

- cleaning transaction rows,
- writing SQL-style sales summaries,
- building monthly category features,
- testing simple forecasting models,
- grouping categories into business segments,
- comparing campaign and non-campaign rows carefully,
- making dashboard-style outputs,
- keeping claims tied to actual files.

## Quick Fictional Example

Imagine a fictional sales team at a pharma distributor.

They sell many kinds of products: antibiotics, vitamins, cardiology products, vaccines, and so on. Every day, they get orders from hospitals, retail stores, government buyers, and online channels.

At the end of the month, someone asks:

> "Which categories should we watch next month, and did campaign rows look any different?"

This project is the kind of workflow that helps answer that question. The example is fictional, but the analytics steps are real.

## Dashboard Preview

![Executive dashboard](dashboards/screenshots/executive_dashboard.svg)

The dashboard is generated from the project files. It isn't a polished Power BI clone. It's proof that the pipeline can create readable business outputs from the same tables used in the reports.

## Current Sample Run

The checked-in run uses generated public data:

| Item | Value |
|---|---:|
| Rows | 25,000 |
| Drug categories | 57 |
| Regions | 5 |
| Channels | 5 |
| Monthly category rows | 1,354 |
| Date range | 2024-01-01 to 2025-12-31 |
| Forecast split | older months train, next block validate, final months test |
| Best model on final test | linear regression |
| Naive RMSE | 18,373.13 |
| Best RMSE | 14,687.75 |
| RMSE drop vs naive | 20.06% |
| Category segments | 4 |
| 4-cluster silhouette | 0.4036 |

One important detail: I tested LightGBM too. It did **not** win on this final test split. The repo says that openly because the point is to be honest, not to force a fancier model into the headline.

## What The Pipeline Does

```text
generate data
  -> clean rows
  -> build monthly category features
  -> forecast sales
  -> segment categories
  -> compare campaign rows
  -> make charts, reports, and dashboard views
```

## How To Run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m src.run_pipeline --rows 25000 --force
```

That command rebuilds the sample data, outputs, reports, and dashboard files.

## Main Files To Check

| File | What It's For |
|---|---|
| `src/run_pipeline.py` | Runs the whole project |
| `src/forecasting.py` | Forecast model comparison |
| `src/segmentation.py` | K-means category grouping |
| `src/ab_analysis.py` | Campaign vs non-campaign comparison |
| `outputs/metrics/run_summary.csv` | Main numbers used for resume claims |
| `outputs/metrics/forecast_model_metrics.csv` | Forecast model results |
| `outputs/metrics/forecast_split_summary.csv` | Train/validation/test split |
| `outputs/tables/segment_profiles.csv` | Category segment labels |
| `dashboards/screenshots/executive_dashboard.svg` | Main dashboard output |
| `docs/CLAIM_LEDGER.md` | What can and can't be claimed |
| `docs/CV_BULLET_BANK.md` | Resume bullets backed by this repo |

## Methods Used

| Step | Tool / Method | Plain-English Reason |
|---|---|---|
| Cleaning | pandas | Good for fixing CSV-style tables |
| SQL summaries | SQL files + pandas checks | Sales data often lives in tables |
| Forecasting | naive, moving average, linear, ridge, LightGBM, ridge + LightGBM residual | Compare simple and stronger baselines without hiding the loser |
| Segmentation | K-means | Easy way to group similar categories |
| Campaign comparison | mean difference + bootstrap interval | Shows the gap without pretending we proved cause and effect |
| Dashboard | generated SVGs | Easy to view on GitHub Pages |

## Dashboard Views

- `dashboards/screenshots/executive_summary.svg`
- `dashboards/screenshots/category_view.svg`
- `dashboards/screenshots/forecast_view.svg`
- `dashboards/screenshots/segment_view.svg`
- `dashboards/screenshots/campaign_comparison_view.svg`

## Safe CV Summary

Built a pharma-style commercial analytics project over 25,000 generated transaction-style rows across 57 categories, covering KPI checks, chronological forecasting tests, K-means segmentation, campaign comparison, and dashboard reporting.

## What Not To Claim

Don't claim:

- real pharma revenue impact,
- live company deployment,
- patient-level data analysis,
- clinical insight,
- campaign lift,
- LightGBM as the winning model.

This is public proof of analytics structure and code quality, not a real company case study.
