# Interview Guide

## 30-Second Explanation

I rebuilt a pharma commercial analytics workflow around transaction-style sales data. The project covers cleaning, SQL-style KPI analysis, forecasting, category segmentation, campaign comparison, and dashboard reporting. The public repo uses synthetic data so the workflow is reproducible without exposing private commercial data.

## 60-Second Explanation

The project starts with transaction data containing category, region, channel, customer segment, units, price, discount, and campaign fields. I clean the data, create derived metrics like net sales and average selling price, then aggregate it into monthly category-level features. For forecasting, I compare naive, moving-average, linear, ridge, LightGBM, and ridge-plus-LightGBM residual baselines using chronological train/validation/test splits. For segmentation, I use K-means to group categories by revenue, volume, discount behavior, campaign share, growth, and volatility. Finally, I run A/B-style campaign comparison and generate dashboard-style SVG outputs.

## Why This Project Is Useful

It shows that I can handle a business analytics workflow end to end:

- data cleaning,
- SQL-style thinking,
- feature engineering,
- forecasting,
- clustering,
- cautious statistical comparison,
- dashboard communication.

## Why Synthetic Data Is Acceptable Here

The goal of the public repo is to demonstrate the workflow safely. Commercial pharma data may be private, so the correct public approach is to publish:

- schema,
- synthetic sample data,
- reproducible code,
- generated reports,
- limitations.

## Why Linear and Ridge Regression

Linear regression is a readable baseline. Ridge regression adds regularization, which helps when features are correlated. I also added LightGBM and a ridge-plus-LightGBM residual model as stronger nonlinear checks. The important point is that I kept the claim honest: in the current chronological test split, linear regression wins on RMSE.

Alternatives:

- ARIMA/SARIMA for classical time-series forecasting,
- XGBoost/LightGBM for nonlinear tabular forecasting,
- Prophet-style models for trend and seasonality,
- neural networks only if there is much more historical data.

## Why K-Means

K-means is simple and explainable. It helps group drug categories into business-readable segments: high-value growing, stable core, campaign-responsive, and low-volume niche.

Alternatives:

- hierarchical clustering for visual grouping,
- Gaussian mixture models for soft clusters,
- DBSCAN for irregular clusters,
- business-rule segmentation when interpretability is the priority.

## Why A/B-Style, Not A/B Testing

True A/B testing needs randomized assignment. This project compares campaign and non-campaign groups, but it does not claim causality. That is why I call it A/B-style or campaign comparison analysis.

## Questions I Can Answer

### What was your main contribution?

I designed the full analytics workflow: data schema, cleaning logic, feature engineering, forecasting, segmentation, campaign comparison, reports, and dashboard-style outputs.

### What is the biggest limitation?

The public data is synthetic. It proves workflow and code quality, not real pharma business impact.

### What would you improve next?

I would add real anonymized aggregates, stronger time-series baselines, dashboard interactivity, and better causal methods if randomized campaign data were available.

### Why not use a more advanced model?

Because the goal was commercial analytics, not model showmanship. For this kind of project, simple interpretable baselines are often more useful and easier to defend.
