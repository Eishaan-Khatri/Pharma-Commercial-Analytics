# Interview Guide

Use this when someone asks, "What is this project?"

## 20-Second Version

I rebuilt a pharma commercial analytics project using generated transaction-style data. It covers cleaning, sales KPIs, forecasting, category segmentation, campaign comparison, and dashboard reporting. The main point is to show a clean data-to-dashboard workflow without pretending the public sample data is real business data.

## 60-Second Version

This project starts with sales-style rows: category, region, channel, customer segment, units, price, discount, and campaign flag.

I clean the rows, create monthly category features, and then compare six forecast models. The split is based on time, so the model trains on older months and tests on later months. The best model in this run is linear regression, with a 20.06% RMSE drop compared with the naive last-period baseline.

After that, I use K-means to group categories into four readable segments: high-value growing, stable core, campaign-responsive, and low-volume niche. I also compare campaign and non-campaign rows, but I clearly mark it as comparison-only, not causal proof.

## What Was My Main Work?

I built the full workflow:

- data generator,
- cleaning logic,
- monthly features,
- forecast comparison,
- K-means segmentation,
- campaign comparison,
- reports,
- dashboard SVGs,
- claim ledger,
- CV bullet bank.

## Why Use Generated Data?

Because the public repo should be safe to share.

The older project referred to larger pharma sales data, but the raw files aren't here. Instead of pretending, I rebuilt the workflow with generated data and tied every claim to a file.

That's more honest.

## Why Did A Simple Model Win?

Because the final test block favored the linear trend and lag features.

I did test LightGBM. It just didn't win here.

That can happen. A stronger model is not always the better model, especially when the dataset is small and the time pattern is simple.

## How Did You Avoid Forecast Leakage?

I didn't randomly mix old and future months.

The split is:

- train on older months,
- validate on the next block,
- test on the final months.

So the model doesn't get to learn from the future.

## Why K-Means?

K-means is easy to explain.

For a business analytics project, that's useful. A manager can understand:

- this group is high-value and growing,
- this one is stable,
- this one reacts more to campaigns,
- this one is small and niche.

If this were a real company project, a domain expert would still review the groups.

## Why Not Claim Campaign Lift?

Because this isn't a real randomized A/B test.

Campaign rows can differ for many reasons: discounts, channels, timing, product mix, or region mix. So I compare the groups and show a bootstrap range, but I don't say the campaign caused the gap.

## Biggest Limitation

The public data is generated.

So the repo proves project structure and code quality, not real pharma business impact.

## Best Resume Claim

```text
Built a pharma-style commercial analytics project over 25,000 generated transaction-style rows across 57 categories, covering KPI checks, chronological forecasting tests, K-means segmentation, campaign comparison, and dashboard reporting.
```

## What I'd Improve Next

I'd add:

- real anonymized aggregate data,
- a live dashboard,
- ARIMA/SARIMA or Prophet-style time-series baselines,
- stronger causal testing if randomized campaign data exists,
- business review for segment labels.
