# Learning Guide

This guide explains what each part of the project does, why it is used, and what alternatives exist.

## Big Picture

This is a commercial analytics project. The goal is not to build the most complex model. The goal is to show a complete business data workflow:

1. collect or simulate transaction data,
2. clean it,
3. create business metrics,
4. forecast trends,
5. segment categories,
6. compare campaign-like groups,
7. turn results into dashboards.

A recruiter should see that you can move from messy data to decision-ready output.

## Why SQL Is Used

SQL is used because transaction data usually lives in databases. Even if Python can do the same aggregation, SQL proves you understand business data systems.

Used for:

- grouping by month/category,
- calculating KPIs,
- comparing campaign and non-campaign groups,
- preparing dashboard tables.

Alternatives:

- pandas for local analysis,
- DuckDB for file-based SQL analytics,
- Spark SQL for very large data,
- BigQuery/Snowflake/Redshift in production.

## Why pandas Is Used

pandas is the main Python library for tabular data. It is used for cleaning, joining, grouping, and feature creation.

Used for:

- loading CSVs,
- cleaning columns,
- deriving revenue metrics,
- aggregating monthly data,
- preparing model inputs.

Alternatives:

- Polars for faster local analytics,
- Spark for distributed data,
- SQL if analysis stays inside a database.

## Why Linear Regression Is Used

Linear regression predicts a numeric target by learning a weighted sum of features.

In this project:

- target = monthly net sales,
- features = lags, rolling averages, month, category, discount, transaction count.

Why useful:

- easy to explain,
- good baseline,
- shows feature importance direction,
- less likely to look like model overkill.

Alternatives:

- ARIMA/SARIMA for classical time series,
- LightGBM/XGBoost for nonlinear tabular forecasting,
- neural networks for larger and richer sequences.

## Why Ridge Regression Is Used

Ridge regression is linear regression with regularization. It penalizes very large coefficients.

Why useful:

- handles many correlated features better,
- reduces overfitting,
- still interpretable enough for business settings.

Alternative:

- Lasso regression if you want feature selection,
- Elastic Net if you want both ridge and lasso behavior.

## Why K-Means Is Used

K-means groups similar categories into clusters.

In this project, categories are clustered using:

- revenue,
- units,
- transaction frequency,
- discount rate,
- growth,
- volatility,
- campaign share.

Why useful:

- simple,
- fast,
- easy to show in dashboards,
- produces business-friendly groupings.

Alternatives:

- hierarchical clustering for tree-like grouping,
- DBSCAN for irregular clusters,
- Gaussian mixture models for softer membership,
- rule-based segmentation when business logic matters more.

## Why A/B-Style Analysis Is Used Carefully

The portfolio mentioned A/B testing. In a public rebuild, the honest wording is A/B-style analysis unless random assignment is documented.

The project compares campaign and non-campaign groups, but it does not claim the campaign caused the difference.

Alternatives:

- randomized A/B test,
- difference-in-differences,
- propensity score matching,
- causal forests,
- uplift modeling.

Those are stronger methods, but they require stronger assumptions and better data.

## Why Dashboards Are Important

Most analytics work is not useful unless a decision-maker can understand it.

Dashboards convert:

- model results,
- KPI tables,
- forecast errors,
- cluster profiles,
- campaign comparisons,

into visible business summaries.

Alternatives:

- Tableau,
- Power BI,
- Streamlit,
- Plotly Dash,
- static HTML reports,
- PDF reports.

## How To Explain This Project In An Interview

Use this structure:

> I rebuilt a pharma commercial analytics workflow around transaction-style sales data. The project covers cleaning, SQL-style aggregation, forecasting, category segmentation, campaign comparison, and dashboard reporting. I used simple interpretable models because the goal was not SOTA modeling; it was to create a business-readable analytics pipeline and avoid overclaiming.

## What Makes The Project Good

- It is end-to-end.
- It includes SQL and Python.
- It has models and dashboards.
- It explains limitations.
- It avoids fake business impact claims.
- It is aligned with real analytics roles.

