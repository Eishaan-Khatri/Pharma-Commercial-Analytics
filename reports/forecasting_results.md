# Forecasting Results

Best sample-run model by RMSE: linear_regression

MAE: 9,677.58

RMSE: 14,687.75

sMAPE: 36.54%

Validation design: leakage-aware month-based split. Training uses older months,
validation uses the next chronological block, and testing uses the final months.

## Split Summary

| split | rows | months | start_month | end_month |
| --- | --- | --- | --- | --- |
| train | 732 | 13 | 2024-03 | 2025-03 |
| validation | 227 | 4 | 2025-04 | 2025-07 |
| test | 281 | 5 | 2025-08 | 2025-12 |

## Model Comparison

| model | validation_RMSE | MAE | RMSE | sMAPE | selected_params |
| --- | --- | --- | --- | --- | --- |
| linear_regression | 19302.4699 | 9677.582 | 14687.751 | 36.5406 | ordinary_least_squares |
| ridge_regression | 16900.4345 | 9477.4058 | 14769.9054 | 33.9718 | alpha=20.0 |
| ridge_lightgbm_residual | 17255.4352 | 9322.4287 | 15435.2739 | 32.7575 | ridge_alpha=20.0; residual_lightgbm=n_estimators=160; learning_rate=0.02; num_leaves=31; min_child_samples=12; subsample=0.85; colsample_bytree=0.85; reg_lambda=4.0 |
| moving_average_3 | 17469.2387 | 9841.9527 | 16515.9879 | 26.6946 | window=3 |
| lightgbm | 19405.5197 | 9669.4051 | 17641.9418 | 30.5283 | n_estimators=80; learning_rate=0.06; num_leaves=31; min_child_samples=8; subsample=0.85; colsample_bytree=0.85; reg_lambda=0.0 |
| naive_last_period | 21191.9294 | 10798.3302 | 18373.1268 | 32.1886 | none |
