# CV Bullet Bank

This file exists for one purpose: choose the best three CV points from the
Pharma Commercial Analytics project without making unsafe or inflated claims.

The project should be presented as a commercial analytics and data science
workflow, not as a clinical AI system and not as a real pharma revenue-impact
case study. The public repository uses synthetic data to safely demonstrate the
original workflow.

## One-Line Project Identity

Pharma Commercial Analytics is a business-facing analytics project covering
transaction cleaning, SQL-style KPI analysis, forecasting, category
segmentation, campaign comparison, and dashboard reporting for pharma-style
commercial sales data.

## Strongest Evidence In The Repo

| Evidence | Source |
|---|---|
| Public sample run uses 25,000 generated transaction rows | `outputs/tables/data_quality_report.csv` |
| Dataset shape includes 57 drug categories, 5 regions, and 5 channels | `outputs/tables/data_quality_report.csv` |
| Date range spans 2024-01-01 to 2025-12-31 | `outputs/tables/data_quality_report.csv` |
| Monthly category table contains 1,354 category-month rows | `outputs/metrics/run_summary.csv` |
| Forecasting compares naive, moving average, linear regression, ridge regression, LightGBM, and ridge + LightGBM residual | `outputs/metrics/forecast_model_metrics.csv` |
| Final test uses chronological holdout: train older months, validate next block, test final months | `outputs/metrics/forecast_split_summary.csv` |
| Linear regression is best by final-test RMSE in the sample run: 14,687.75 | `outputs/metrics/forecast_model_metrics.csv` |
| Best model improves RMSE over naive baseline by 20.06% | `outputs/metrics/run_summary.csv` |
| K-means category segmentation uses 4 business-selected clusters with silhouette 0.4036 | `outputs/metrics/cluster_selection_scores.csv` |
| Segment profiles separate high-value growing, stable core, campaign-responsive, and low-volume niche categories | `outputs/tables/segment_profiles.csv` |
| Campaign comparison includes bootstrap confidence interval and explicitly avoids causal claims | `outputs/tables/ab_style_inference.csv` |
| Dashboard-style executive output and four detailed views exist | `dashboards/screenshots/` |
| Methodology, limitations, interview guide, and claim ledger are documented | `docs/` |

## Final 3 Best CV Bullets

Use these three bullets when this project appears in a CV or resume.

```text
- Built a reproducible pharma commercial analytics workflow covering transaction cleaning, SQL-style KPI analysis, forecasting, category segmentation, campaign comparison, and executive dashboard reporting.
- Compared six forecasting baselines across 57 drug categories using chronological train/validation/test splits; the best final-test model reduced RMSE by 20.06% versus the naive baseline.
- Designed four business-readable K-means category segments and campaign comparison modules, separating high-value growing, stable core, campaign-responsive, and low-volume niche groups while documenting non-causal limitations with bootstrap confidence intervals.
```

## Shorter One-Page Resume Version

Use this if space is tight.

```text
- Built a reproducible pharma commercial analytics pipeline for transaction cleaning, KPI analysis, forecasting, segmentation, campaign comparison, and dashboard reporting.
- Compared six forecasting baselines across 57 categories; the best chronological-test model improved RMSE by 20.06% over naive.
- Segmented categories using K-means and translated outputs into executive-facing dashboard views with documented limitations and claim boundaries.
```

## Stronger Data Science Version

Best for Data Scientist, Business Analyst, Commercial Analytics, and Decision
Science roles.

```text
- Developed an end-to-end commercial analytics pipeline over pharma-style transaction data, including validation, SQL-style KPI generation, monthly feature aggregation, forecasting, segmentation, and reporting.
- Benchmarked forecasting baselines with leakage-aware chronological splits across 57 categories; compared naive, moving-average, linear regression, ridge regression, LightGBM, and ridge + LightGBM residual models with RMSE/MAE/sMAPE reporting.
- Built interpretable 4-cluster K-means segment profiles and A/B-style campaign comparisons, using bootstrap confidence intervals and explicit non-causal framing to keep business recommendations defensible.
```

## Industrial AI / Tata Steel Version

Best when applying to industrial AI, manufacturing analytics, supply chain
analytics, or Tata Steel-type roles.

```text
- Built a production-style analytics workflow for industrial-commercial decision support, converting noisy transaction streams into cleaned KPIs, forecasts, segment profiles, and dashboard-ready outputs.
- Implemented interpretable forecasting and clustering modules for category-level planning, comparing six baseline models and surfacing high-value, stable core, campaign-responsive, and low-volume groups for business review.
- Designed stakeholder-facing reporting with a claim ledger, limitations section, and reproducible pipeline so outputs can be audited rather than treated as black-box predictions.
```

## ML Engineer Version

Best when applying to ML Engineer or Applied ML roles where code quality matters.

```text
- Rebuilt the project as a reproducible Python package with modular components for data generation, cleaning, feature engineering, forecasting, clustering, A/B-style analysis, visualization, and reporting.
- Implemented model evaluation pipelines for regression forecasting and category segmentation, generating versioned metrics CSVs, SVG figures, reports, and dashboard artifacts from a single command.
- Added documentation for methodology, limitations, data dictionary, interview explanation, and claim risk so the public repo can be reviewed and defended end to end.
```

## Research / RA Version

Best when applying to research assistant roles where methodological discipline
matters more than business impact.

```text
- Reconstructed a public, reproducible analytics study from a previously lost project, separating verified original claims from rebuilt synthetic-data evidence through a claim ledger.
- Evaluated forecasting and segmentation methods with transparent metrics, leakage-aware splits, baseline comparisons, and documented limitations instead of overstating model accuracy or causal impact.
- Produced a full research-style artifact set: methodology, data dictionary, limitations, final report, generated tables, figures, notebooks, and GitHub Pages case-study site.
```

## What To Avoid Saying

Do not use these claims in a CV unless you have separate private proof and can
defend them in an interview.

| Avoid | Why |
|---|---|
| Increased pharma revenue by X percent | No causal business outcome is proven in the public repo |
| Deployed to production | The public project is a reproducible portfolio rebuild |
| Worked on patient-level or clinical pharma data | This is commercial sales analytics, not clinical analytics |
| Achieved high accuracy | Forecasting uses regression metrics, not classification accuracy |
| Proved campaign impact | Campaign analysis is comparison-only, not causal inference |
| Used real public pharma sales data | Public repo uses synthetic sample data |
| Built a Tableau/Power BI dashboard if only showing this repo | Public repo uses dashboard-style SVG outputs; mention Tableau/Power BI only if discussing original/private work |

## Safe Claim Levels

| Claim Type | Safe Wording |
|---|---|
| Original project scale | "Original portfolio version referenced 600K+ transactions across 57 categories" |
| Public repo scale | "Public reproducible sample run uses 25,000 synthetic transactions across 57 categories" |
| Business output | "Executive-facing dashboard reporting" |
| Campaign analysis | "A/B-style comparison with non-causal limitations" |
| Forecasting | "Compared six forecasting baselines with chronological train/validation/test splits" |
| Segmentation | "Built 4-cluster K-means segment profiles for category-level planning" |

## Which Three Bullets To Pick By Role

| Role | Pick These Bullets |
|---|---|
| Data Scientist | data pipeline + forecasting + segmentation/campaign comparison |
| Business Analyst | KPI analysis + dashboard + segmentation |
| ML Engineer | reproducible package + model evaluation + generated artifacts |
| Industrial AI | decision support + forecasting/clustering + auditable reporting |
| Research Assistant | reconstruction discipline + transparent evaluation + full artifact set |
| Product/Data Analytics | commercial workflow + stakeholder dashboard + defensible limitations |

## Interview Defense For The Three Main Bullets

### Bullet 1: Full analytics workflow

What you did:

- Created a clean public version of a lost pharma commercial analytics project.
- Generated transaction-style sample data.
- Built cleaning, KPI, forecasting, segmentation, comparison, reporting, and dashboard layers.

Why it matters:

- Recruiters see that this is not a single notebook.
- It demonstrates an end-to-end analytics workflow from raw data to stakeholder output.

Limitation to admit:

- The public repo uses synthetic data, so it demonstrates workflow quality, not real business outcome.

### Bullet 2: Forecasting baselines

What you did:

- Aggregated monthly category-level features.
- Compared naive, moving-average, linear regression, ridge regression, LightGBM, and ridge-plus-LightGBM residual models.
- Reported MAE, RMSE, and sMAPE.

Why linear/ridge plus LightGBM:

- Linear regression gives a readable trend/lag baseline.
- Ridge regression adds regularization when features are correlated.
- LightGBM adds a nonlinear tabular baseline.
- The residual variant tests whether LightGBM can improve what ridge misses.
- In the current final-test run, linear regression wins; the repo documents that instead of overstating the tree model.

Alternatives:

- ARIMA/SARIMA for classical time series.
- Prophet for business forecasting.
- XGBoost/CatBoost for additional nonlinear tabular forecasting.
- LSTM/Temporal Fusion Transformer if there is enough real sequential data.

Why not use these first:

- The public version needs to be lightweight, reproducible, and defensible.
- Simple baselines are easier to explain and audit.

### Bullet 3: Segmentation and campaign comparison

What you did:

- Built K-means category segmentation using commercial features.
- Selected 4 business-readable clusters and reported the silhouette score.
- Produced segment labels that are readable by business stakeholders.
- Added campaign comparison with bootstrap confidence intervals.

Why K-means:

- It is simple, fast, and easy to explain.
- It gives useful first-pass grouping for business review.

Alternatives:

- Gaussian Mixture Models for softer cluster membership.
- Hierarchical clustering for dendrogram-based business interpretation.
- DBSCAN/HDBSCAN for density-based clusters.
- PCA/UMAP before clustering for visualization.

Limitation to admit:

- Campaign comparison is not causal because there is no randomized assignment.
- It should be treated as exploratory evidence, not proof of campaign lift.

## Best Project Entry For Resume

Use this entry when you have room for a project title and three bullets.

```text
Pharma Commercial Analytics | Python, SQL, pandas, LightGBM, forecasting, K-means, dashboard reporting
- Built a reproducible pharma commercial analytics workflow covering transaction cleaning, SQL-style KPI analysis, forecasting, category segmentation, campaign comparison, and executive dashboard reporting.
- Compared six forecasting baselines across 57 drug categories using chronological train/validation/test splits; the best final-test model reduced RMSE by 20.06% versus the naive baseline.
- Designed four business-readable K-means category segments and campaign comparison modules, separating high-value growing, stable core, campaign-responsive, and low-volume niche groups while documenting non-causal limitations with bootstrap confidence intervals.
```

## Best One-Line Version

Use this when the project gets only one bullet in a crowded resume.

```text
- Built a reproducible pharma commercial analytics workflow with SQL-style KPIs, six forecasting baselines, 4-cluster K-means segmentation, A/B-style comparison, and executive dashboard reporting across 57 pharma-style categories.
```

## Why These Are The Best Three Points

These bullets are strong because they show:

1. End-to-end execution: not just modeling, but data to dashboard.
2. Analytics maturity: forecasting, segmentation, metrics, and validation.
3. Professional restraint: limitations and claim boundaries are documented.

That combination is better for shortlisting than saying "used ML on pharma
data" because it proves you can build, evaluate, explain, and package a data
science project properly.
