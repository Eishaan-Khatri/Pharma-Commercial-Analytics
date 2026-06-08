# Limitations

## 1. Public Data Is Synthetic

The rebuilt repository uses generated sample data. It demonstrates workflow and code quality, not real pharma commercial outcomes.

## 2. A/B-Style Analysis Is Not Causal

Unless treatment and control groups are randomized, campaign comparisons cannot prove business impact. This project reports observed differences and limitations.

## 3. Forecasting Is Kept Interpretable

Linear and ridge regression are useful baselines, but they may miss nonlinear patterns. Stronger models such as LightGBM or SARIMA can be added later.

## 4. Segmentation Requires Business Validation

K-means produces mathematical clusters. A business team must validate whether those clusters are useful for decisions.

## 5. No Clinical Claims

The project is commercial analytics. It does not analyze patients, outcomes, drug safety, or clinical recommendations.

