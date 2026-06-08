# Methodology

## 1. Data Generation / Loading

The public repository uses synthetic transaction data because the original raw data is not available in the workspace and should not be assumed shareable.

The generator creates:

- 57 drug categories,
- multiple regions,
- multiple channels,
- customer segments,
- realistic seasonality,
- category-level market share differences,
- campaign-like periods,
- transaction-level sales, discounts, and revenue.

## 2. Data Cleaning

The cleaning step:

- parses dates,
- removes duplicate transaction IDs,
- converts numeric fields,
- removes invalid negative units or sales values,
- fills required derived columns,
- creates month and quarter buckets,
- creates average selling price.

Why this matters: analytics projects fail when downstream dashboards or models are built on inconsistent transaction data.

## 3. SQL Analytics

SQL is included because commercial analytics roles expect evidence that you can query structured business data, not only use notebooks.

The SQL layer covers:

- monthly revenue,
- top categories,
- category growth,
- region/channel contribution,
- campaign and non-campaign comparison.

## 4. Forecasting

Forecasting is performed on month-category aggregates.

Models used:

- naive last-period baseline,
- moving average baseline,
- linear regression,
- ridge regression,
- LightGBM,
- ridge + LightGBM residual model.

Why these models:

- they are interpretable,
- they are appropriate for a public portfolio rebuild,
- they make leakage easier to audit,
- they fit the original portfolio claim of linear/ridge regression,
- they add one stronger nonlinear tabular baseline without hiding when it loses.

The reported run uses a chronological split:

- train on older months,
- validate on the next month block,
- test on the final month block.

This avoids random-split leakage across time.

Alternatives:

- ARIMA/SARIMA for classical time-series modeling,
- XGBoost/CatBoost for additional nonlinear tabular forecasting,
- Prophet-style models for decomposable trend/seasonality,
- deep learning only if much more historical data exists.

## 5. Segmentation

K-means clustering is used to group categories by commercial behavior.

Features include:

- total revenue,
- total units,
- average order value,
- average discount rate,
- transaction frequency,
- growth rate,
- revenue volatility,
- campaign share.

Why K-means:

- it is simple,
- it is easy to explain,
- it matches the original portfolio claim,
- it produces dashboard-friendly segment labels.

Alternatives:

- hierarchical clustering for dendrogram-style exploration,
- Gaussian mixture models when clusters overlap,
- DBSCAN when clusters are irregular and noise-heavy,
- business rules when interpretability matters more than unsupervised learning.

## 6. A/B-Style Analysis

The campaign comparison is deliberately called A/B-style analysis, not causal inference.

Why:

- real A/B testing requires randomized assignment,
- commercial campaigns often target specific regions/products,
- seasonality and category mix may confound the result.

The analysis therefore reports:

- group means,
- observed difference,
- bootstrap confidence interval,
- limitations.

## 7. Dashboarding

Dashboard screenshots are generated from the analysis outputs to show how a non-technical stakeholder would consume the work.

Dashboard sections:

- executive overview,
- category performance,
- forecasting,
- segmentation,
- campaign comparison.

The public repo includes separate generated SVG views for each of these sections,
plus one combined executive dashboard.
