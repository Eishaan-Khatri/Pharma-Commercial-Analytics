# Limitations

## 1. Public Data Is Synthetic

The rebuilt repository uses generated sample data. It demonstrates workflow and code quality, not real pharma commercial outcomes.

## 2. A/B-Style Analysis Is Not Causal

Unless treatment and control groups are randomized, campaign comparisons cannot prove business impact. This project reports observed differences and limitations.

## 3. Forecasting Is Kept Interpretable

The current public rebuild includes naive, moving-average, linear regression,
ridge regression, LightGBM, and ridge-plus-LightGBM residual baselines. Linear
regression wins on final-test RMSE in the checked-in sample run. That should be
reported honestly; do not claim LightGBM is best unless a future run actually
shows that in `outputs/metrics/forecast_model_metrics.csv`.

SARIMA/Prophet-style models can still be added later if the goal is a more
classical time-series comparison.

## 4. Segmentation Requires Business Validation

K-means produces mathematical clusters. A business team must validate whether those clusters are useful for decisions.

## 5. No Clinical Claims

The project is commercial analytics. It does not analyze patients, outcomes, drug safety, or clinical recommendations.
