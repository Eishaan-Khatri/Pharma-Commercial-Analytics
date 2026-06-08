from __future__ import annotations

import numpy as np
import pandas as pd


def _smape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    denominator = (np.abs(y_true) + np.abs(y_pred)) / 2
    mask = denominator != 0
    return float(np.mean(np.abs(y_true[mask] - y_pred[mask]) / denominator[mask]) * 100)


def _metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    mae = float(np.mean(np.abs(y_true - y_pred)))
    rmse = float(np.sqrt(np.mean((y_true - y_pred) ** 2)))
    return {
        "MAE": mae,
        "RMSE": rmse,
        "sMAPE": _smape(y_true, y_pred),
    }


def _standardize(train_x: np.ndarray, test_x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    mean = train_x.mean(axis=0)
    std = train_x.std(axis=0)
    std[std == 0] = 1.0
    return (train_x - mean) / std, (test_x - mean) / std


def _add_intercept(x: np.ndarray) -> np.ndarray:
    return np.column_stack([np.ones(len(x)), x])


def _linear_regression_predict(train_x: np.ndarray, y_train: np.ndarray, test_x: np.ndarray) -> np.ndarray:
    train_scaled, test_scaled = _standardize(train_x, test_x)
    train_design = _add_intercept(train_scaled)
    test_design = _add_intercept(test_scaled)
    coef, *_ = np.linalg.lstsq(train_design, y_train, rcond=None)
    return test_design @ coef


def _ridge_regression_predict(
    train_x: np.ndarray,
    y_train: np.ndarray,
    test_x: np.ndarray,
    alpha: float = 5.0,
) -> np.ndarray:
    train_scaled, test_scaled = _standardize(train_x, test_x)
    train_design = _add_intercept(train_scaled)
    test_design = _add_intercept(test_scaled)
    identity = np.eye(train_design.shape[1])
    identity[0, 0] = 0.0
    coef = np.linalg.pinv(train_design.T @ train_design + alpha * identity) @ train_design.T @ y_train
    return test_design @ coef


def run_forecasting(monthly: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    model_df = monthly.dropna(subset=["lag_1_sales", "lag_2_sales", "rolling_3_sales", "rolling_3_units"]).copy()
    model_df = model_df.sort_values("month_date")

    unique_months = sorted(model_df["month_date"].unique())
    cutoff_index = int(len(unique_months) * 0.80)
    cutoff_month = unique_months[cutoff_index]
    train = model_df[model_df["month_date"] < cutoff_month].copy()
    test = model_df[model_df["month_date"] >= cutoff_month].copy()

    base_features = [
        "lag_1_sales",
        "lag_2_sales",
        "rolling_3_sales",
        "rolling_3_units",
        "lag_1_units",
        "lag_1_transaction_count",
        "lag_1_avg_discount_rate",
        "lag_1_campaign_share",
        "month_number",
        "time_index",
    ]

    train_x = pd.get_dummies(train[base_features + ["drug_category"]], columns=["drug_category"], drop_first=False)
    test_x = pd.get_dummies(test[base_features + ["drug_category"]], columns=["drug_category"], drop_first=False)
    test_x = test_x.reindex(columns=train_x.columns, fill_value=0)

    y_train = train["net_sales"].to_numpy(dtype=float)
    y_test = test["net_sales"].to_numpy()

    predictions = test[["month", "drug_category", "net_sales", "lag_1_sales", "rolling_3_sales"]].copy()
    predictions = predictions.rename(columns={"net_sales": "actual_sales"})
    predictions["naive_last_period"] = predictions["lag_1_sales"]
    predictions["moving_average_3"] = predictions["rolling_3_sales"]

    train_array = train_x.to_numpy(dtype=float)
    test_array = test_x.to_numpy(dtype=float)
    predictions["linear_regression"] = _linear_regression_predict(train_array, y_train, test_array).clip(min=0)
    predictions["ridge_regression"] = _ridge_regression_predict(train_array, y_train, test_array).clip(min=0)

    metric_rows = []
    for col in ["naive_last_period", "moving_average_3", "linear_regression", "ridge_regression"]:
        row = {"model": col}
        row.update(_metrics(y_test, predictions[col].to_numpy()))
        metric_rows.append(row)

    metrics = pd.DataFrame(metric_rows).sort_values("RMSE").reset_index(drop=True)
    return metrics, predictions
