# Forecasting Results

This report answers one question:

> Which simple forecast model worked best on the final months?

## Answer

The best model in this run was:

```text
linear_regression
```

Its final-test RMSE was:

```text
14,687.75
```

The naive last-period model had RMSE:

```text
18,373.13
```

So the best model lowered RMSE by:

```text
20.06%
```

## Split

The split is based on time.

That means older months train the model, the next block helps choose settings, and the final months are used for the final score.

| split | rows | months | start_month | end_month |
|---|---:|---:|---|---|
| train | 732 | 13 | 2024-03 | 2025-03 |
| validation | 227 | 4 | 2025-04 | 2025-07 |
| test | 281 | 5 | 2025-08 | 2025-12 |

## Model Table

| model | validation_RMSE | MAE | RMSE | sMAPE | notes |
|---|---:|---:|---:|---:|---|
| linear_regression | 19,302.47 | 9,677.58 | 14,687.75 | 36.54% | best final-test RMSE |
| ridge_regression | 16,900.43 | 9,477.41 | 14,769.91 | 33.97% | close second |
| ridge_lightgbm_residual | 17,255.44 | 9,322.43 | 15,435.27 | 32.76% | good MAE, worse RMSE |
| moving_average_3 | 17,469.24 | 9,841.95 | 16,515.99 | 26.69% | simple baseline |
| lightgbm | 19,405.52 | 9,669.41 | 17,641.94 | 30.53% | tested, did not win |
| naive_last_period | 21,191.93 | 10,798.33 | 18,373.13 | 32.19% | baseline to beat |

## Plain-English Takeaway

The fancier model did not win.

That's okay. On this generated sample, the lag and trend features were simple enough that linear regression worked best on the final test block.

The honest resume claim is:

> Compared six forecast baselines and got a 20.06% RMSE drop over the naive baseline.
