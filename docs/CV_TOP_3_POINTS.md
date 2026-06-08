# CV Top 3 Points

Use this file when you want to add **Pharma Commercial Analytics** to a resume and need only the best three points.

The goal is not to make the project sound bigger than it is. The goal is to make it sound clear, useful, and defensible.

This project is best for:

- data analyst roles,
- data science roles,
- business analytics roles,
- consulting analytics roles,
- industrial AI roles where analytics proof helps.

This project is not your strongest proof for:

- NLP roles,
- computer vision roles,
- pure ML research roles,
- applied scientist roles where papers matter more.

For those roles, keep this project lower or use only one bullet.

---

## The 3 Best CV Points

```text
- Built a pharma-style sales analytics project over 25,000 generated transaction rows across 57 categories, covering KPI checks, forecasting, segmentation, campaign comparison, and dashboard reporting.
- Compared six forecasting baselines with a time-based train/validation/test split; the best final-test model cut RMSE by 20.06% compared with the naive last-period baseline.
- Grouped 57 categories into four K-means segments: high-value growing, stable core, campaign-responsive, and low-volume niche; kept the campaign section comparison-only with a bootstrap confidence interval.
```

These are the best three because they cover the full project:

1. **Data-to-dashboard work**
2. **Forecasting and evaluation**
3. **Segmentation and business interpretation**

That is stronger than saying only "I used Python and Power BI."

---

## Why These 3 Points Work

### Point 1: Data-to-dashboard work

```text
Built a pharma-style sales analytics project over 25,000 generated transaction rows across 57 categories, covering KPI checks, forecasting, segmentation, campaign comparison, and dashboard reporting.
```

Why this is good:

- It shows project size.
- It shows business context.
- It shows you did more than one model.
- It tells the recruiter what the project actually contains.

What it proves:

- You can clean and organize sales-style data.
- You can build a complete analytics project.
- You can produce outputs that a non-technical reviewer can read.

Evidence:

| Claim | Proof file |
|---|---|
| 25,000 rows | `outputs/metrics/run_summary.csv` |
| 57 categories | `outputs/metrics/run_summary.csv` |
| KPI checks | `reports/eda_summary.md`, `outputs/tables/` |
| Dashboard reporting | `dashboards/screenshots/` |

Weakness:

The data is generated. Do not make it sound like real pharma sales data.

Safe interview line:

> Since the raw older project files were not available for public upload, I rebuilt the project with generated transaction-style data and kept the claims tied to public files.

---

### Point 2: Forecasting and no-peeking evaluation

```text
Compared six forecasting baselines with a time-based train/validation/test split; the best final-test model cut RMSE by 20.06% compared with the naive last-period baseline.
```

Why this is good:

- It shows model comparison.
- It shows you understand time-based evaluation.
- It gives a real metric.
- It avoids the weak student-project mistake of random splitting time-series data.

What it proves:

- You can build baselines.
- You can compare models honestly.
- You can keep the final test months separate.

Evidence:

| Claim | Proof file |
|---|---|
| six forecasting baselines | `outputs/metrics/forecast_model_metrics.csv` |
| time-based train/validation/test split | `outputs/metrics/forecast_split_summary.csv` |
| best model was linear regression | `outputs/metrics/run_summary.csv` |
| naive RMSE 18,373.13 | `outputs/metrics/run_summary.csv` |
| best RMSE 14,687.75 | `outputs/metrics/run_summary.csv` |
| 20.06% RMSE drop | `outputs/metrics/run_summary.csv` |

Important detail:

LightGBM was tested, but it did not win. The winning final-test model was `linear_regression`.

Do not write:

```text
LightGBM was the winning model.
```

That is false for the current public run.

Safe interview line:

> I tested both simple and nonlinear models. The simple linear model won on the final test block, which is why I used that in the final claim instead of forcing the LightGBM story.

---

### Point 3: Segmentation and campaign caution

```text
Grouped 57 categories into four K-means segments: high-value growing, stable core, campaign-responsive, and low-volume niche; kept the campaign section comparison-only with a bootstrap confidence interval.
```

Why this is good:

- It shows business interpretation.
- It shows you can turn numbers into readable groups.
- It shows you understand the limit of campaign analysis.
- It avoids fake causal claims.

What it proves:

- You can use clustering for business review.
- You can explain model output in plain language.
- You can avoid overclaiming when the data is observational.

Evidence:

| Claim | Proof file |
|---|---|
| 4 K-means segments | `outputs/tables/segment_profiles.csv` |
| segment names | `outputs/tables/segment_profiles.csv` |
| silhouette 0.4036 | `outputs/metrics/run_summary.csv` |
| bootstrap confidence interval | `outputs/metrics/campaign_comparison_ci.csv` |
| campaign dashboard view | `dashboards/screenshots/campaign_comparison_view.svg` |

Weakness:

The campaign flag is not randomized. That means the campaign comparison is not proof that the campaign caused higher or lower sales.

Safe interview line:

> I treated the campaign section as a comparison, not a causal claim, because there was no randomized assignment.

---

## Short Version For A Crowded Resume

Use this when you only have space for two lines:

```text
- Built a pharma-style analytics pipeline across 25,000 generated rows and 57 categories, covering KPI checks, forecasting, K-means segmentation, campaign comparison, and dashboard reporting.
- Compared six forecast baselines with a time-based split; best final-test RMSE was 14,687.75, which was 20.06% lower than the naive baseline.
```

Use this when you only have space for one line:

```text
- Built a pharma-style analytics pipeline with KPI checks, six forecast baselines, 4-cluster K-means segmentation, campaign comparison, and dashboard reporting across 57 categories.
```

---

## Which Version To Use By Role

### Data Analyst

Use all three bullets.

Focus on:

- KPI checks,
- dashboards,
- category segments,
- clear reporting.

### Data Scientist

Use bullets 1 and 2 first.

Focus on:

- baseline comparison,
- time-based split,
- RMSE improvement,
- model honesty.

### Business Analyst / Consulting

Use bullets 1 and 3 first.

Focus on:

- sales categories,
- dashboards,
- segment labels,
- campaign comparison limits.

### ML Engineer

Use a different version:

```text
- Rebuilt the project as a Python pipeline with separate modules for data generation, cleaning, features, forecasting, segmentation, campaign comparison, reporting, and SVG dashboard output.
- Added an `outputs/metrics/` layer so every resume number can be traced to a CSV file.
- Compared simple and nonlinear forecast baselines, including LightGBM, while keeping the final claim tied to the actual winning model.
```

### Research / Applied Scientist

Use only one bullet, or skip this project if space is tight.

Better proof for those roles:

- Hinglish ESWA,
- CASML,
- CV robustness,
- agent systems,
- industrial anomaly detection.

This pharma project helps show analytics discipline, but it is not your strongest research signal.

---

## What Not To Say

Do not write:

```text
Improved pharma revenue.
Deployed analytics system for a real company.
Used patient-level data.
Built clinical AI.
Proved campaign lift.
LightGBM was the winner.
Presented the older 600K+ note as the current public dataset.
```

Why not:

- The public repo uses generated data.
- The public run has 25,000 rows, not 600K rows.
- LightGBM was tested but did not win.
- Campaign comparison is not causal.
- There is no clinical or patient-level work here.

---

## Best 60-Second Interview Explanation

```text
I rebuilt an older pharma commercial analytics project as a public repo. Since the raw older files were not available for public upload, I used generated transaction-style data and made the repo fully checkable.

The project cleans 25,000 rows, builds monthly category features, compares six forecast models with a time-based split, groups 57 categories into four K-means segments, compares campaign-like rows without claiming causality, and creates dashboard files.

The strongest result is the forecasting comparison: the best final-test model reduced RMSE by 20.06% compared with the naive baseline. I also kept an outputs/metrics folder so every number used in the CV can be traced back to a CSV.
```

---

## Final Recommendation

Use these three bullets only when the role cares about analytics, forecasting, dashboards, or business data.

For a one-page resume, do not let this project crowd out stronger work like your Hinglish paper, CASML, agent systems, or industrial anomaly detection.

The best use of this project is simple:

> It proves you can take messy business-style data, build a clean analysis pipeline, compare models honestly, and explain the result without fake impact claims.
