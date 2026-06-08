from __future__ import annotations

import itertools

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


def _ridge_regression_fit_predict(
    train_x: np.ndarray,
    y_train: np.ndarray,
    pred_x: np.ndarray,
    alpha: float,
) -> tuple[np.ndarray, np.ndarray]:
    train_scaled, pred_scaled = _standardize(train_x, pred_x)
    train_design = _add_intercept(train_scaled)
    pred_design = _add_intercept(pred_scaled)
    identity = np.eye(train_design.shape[1])
    identity[0, 0] = 0.0
    coef = np.linalg.pinv(train_design.T @ train_design + alpha * identity) @ train_design.T @ y_train
    fitted_train = train_design @ coef
    pred = pred_design @ coef
    return fitted_train, pred


def _month_based_splits(model_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    unique_months = sorted(model_df["month_date"].unique())
    if len(unique_months) < 8:
        raise ValueError("Need at least 8 modeled months for train/validation/test forecasting splits.")

    train_end = max(int(len(unique_months) * 0.60), 1)
    val_end = max(int(len(unique_months) * 0.80), train_end + 1)
    if val_end >= len(unique_months):
        val_end = len(unique_months) - 1

    train_months = set(unique_months[:train_end])
    val_months = set(unique_months[train_end:val_end])
    test_months = set(unique_months[val_end:])

    train = model_df[model_df["month_date"].isin(train_months)].copy()
    validation = model_df[model_df["month_date"].isin(val_months)].copy()
    test = model_df[model_df["month_date"].isin(test_months)].copy()

    split_summary = pd.DataFrame(
        [
            {
                "split": "train",
                "rows": len(train),
                "months": len(train_months),
                "start_month": min(train_months).strftime("%Y-%m"),
                "end_month": max(train_months).strftime("%Y-%m"),
            },
            {
                "split": "validation",
                "rows": len(validation),
                "months": len(val_months),
                "start_month": min(val_months).strftime("%Y-%m"),
                "end_month": max(val_months).strftime("%Y-%m"),
            },
            {
                "split": "test",
                "rows": len(test),
                "months": len(test_months),
                "start_month": min(test_months).strftime("%Y-%m"),
                "end_month": max(test_months).strftime("%Y-%m"),
            },
        ]
    )
    return train, validation, test, split_summary


def _make_model_matrix(
    train: pd.DataFrame,
    validation: pd.DataFrame,
    test: pd.DataFrame,
    base_features: list[str],
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    train_x = pd.get_dummies(train[base_features + ["drug_category"]], columns=["drug_category"], drop_first=False)
    val_x = pd.get_dummies(validation[base_features + ["drug_category"]], columns=["drug_category"], drop_first=False)
    test_x = pd.get_dummies(test[base_features + ["drug_category"]], columns=["drug_category"], drop_first=False)
    val_x = val_x.reindex(columns=train_x.columns, fill_value=0)
    test_x = test_x.reindex(columns=train_x.columns, fill_value=0)
    return train_x, val_x, test_x


def _predict_lightgbm(
    train_x: np.ndarray,
    y_train: np.ndarray,
    val_x: np.ndarray,
    params: dict,
) -> np.ndarray | None:
    try:
        from lightgbm import LGBMRegressor
    except Exception:
        return None

    model = LGBMRegressor(
        objective="regression",
        random_state=42,
        verbose=-1,
        **params,
    )
    model.fit(train_x, y_train)
    return model.predict(val_x)


def _best_lightgbm_params(
    train_x: np.ndarray,
    y_train: np.ndarray,
    val_x: np.ndarray,
    y_val: np.ndarray,
) -> tuple[dict | None, dict[str, float] | None]:
    grid = {
        "n_estimators": [80, 140, 220],
        "learning_rate": [0.035, 0.06, 0.09],
        "num_leaves": [7, 15, 31],
        "min_child_samples": [8, 16],
        "subsample": [0.85],
        "colsample_bytree": [0.85],
        "reg_lambda": [0.0, 2.0],
    }

    best_params = None
    best_metrics = None
    for values in itertools.product(*grid.values()):
        params = dict(zip(grid.keys(), values))
        pred = _predict_lightgbm(train_x, y_train, val_x, params)
        if pred is None:
            return None, None
        pred = np.clip(pred, 0, None)
        metrics = _metrics(y_val, pred)
        if best_metrics is None or metrics["RMSE"] < best_metrics["RMSE"]:
            best_params = params
            best_metrics = metrics
    return best_params, best_metrics


def run_forecasting(monthly: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    model_df = monthly.dropna(subset=["lag_1_sales", "lag_2_sales", "rolling_3_sales", "rolling_3_units"]).copy()
    model_df = model_df.sort_values("month_date")
    model_df["month_sin"] = np.sin(2 * np.pi * model_df["month_number"] / 12)
    model_df["month_cos"] = np.cos(2 * np.pi * model_df["month_number"] / 12)
    model_df["discount_campaign_interaction"] = model_df["lag_1_avg_discount_rate"] * model_df["lag_1_campaign_share"]

    train, validation, test, split_summary = _month_based_splits(model_df)
    train_val = pd.concat([train, validation], ignore_index=True)

    base_features = [
        "lag_1_sales",
        "lag_2_sales",
        "rolling_3_sales",
        "rolling_3_units",
        "lag_1_units",
        "lag_1_transaction_count",
        "lag_1_avg_discount_rate",
        "lag_1_campaign_share",
        "discount_campaign_interaction",
        "month_number",
        "month_sin",
        "month_cos",
        "time_index",
    ]

    train_x, val_x, test_x = _make_model_matrix(train, validation, test, base_features)
    train_val_x, _, final_test_x = _make_model_matrix(train_val, validation, test, base_features)

    y_train = train["net_sales"].to_numpy(dtype=float)
    y_val = validation["net_sales"].to_numpy(dtype=float)
    y_train_val = train_val["net_sales"].to_numpy(dtype=float)
    y_test = test["net_sales"].to_numpy(dtype=float)

    train_array = train_x.to_numpy(dtype=float)
    val_array = val_x.to_numpy(dtype=float)
    train_val_array = train_val_x.to_numpy(dtype=float)
    test_array = final_test_x.to_numpy(dtype=float)

    predictions = test[["month", "drug_category", "net_sales", "lag_1_sales", "rolling_3_sales"]].copy()
    predictions = predictions.rename(columns={"net_sales": "actual_sales"})
    predictions["naive_last_period"] = predictions["lag_1_sales"]
    predictions["moving_average_3"] = predictions["rolling_3_sales"]

    val_naive = validation["lag_1_sales"].to_numpy(dtype=float)
    val_moving = validation["rolling_3_sales"].to_numpy(dtype=float)
    metric_rows = [
        {
            "model": "naive_last_period",
            **{f"validation_{k}": v for k, v in _metrics(y_val, val_naive).items()},
            **_metrics(y_test, predictions["naive_last_period"].to_numpy(dtype=float)),
            "selected_params": "none",
        },
        {
            "model": "moving_average_3",
            **{f"validation_{k}": v for k, v in _metrics(y_val, val_moving).items()},
            **_metrics(y_test, predictions["moving_average_3"].to_numpy(dtype=float)),
            "selected_params": "window=3",
        },
    ]

    val_linear = _linear_regression_predict(train_array, y_train, val_array).clip(min=0)
    predictions["linear_regression"] = _linear_regression_predict(train_val_array, y_train_val, test_array).clip(min=0)
    metric_rows.append(
        {
            "model": "linear_regression",
            **{f"validation_{k}": v for k, v in _metrics(y_val, val_linear).items()},
            **_metrics(y_test, predictions["linear_regression"].to_numpy(dtype=float)),
            "selected_params": "ordinary_least_squares",
        }
    )

    best_alpha = None
    best_ridge_val = None
    for alpha in [0.1, 1.0, 5.0, 20.0, 100.0, 250.0]:
        pred = _ridge_regression_predict(train_array, y_train, val_array, alpha=alpha).clip(min=0)
        metrics = _metrics(y_val, pred)
        if best_ridge_val is None or metrics["RMSE"] < best_ridge_val["RMSE"]:
            best_alpha = alpha
            best_ridge_val = metrics
    predictions["ridge_regression"] = _ridge_regression_predict(
        train_val_array,
        y_train_val,
        test_array,
        alpha=float(best_alpha),
    ).clip(min=0)
    metric_rows.append(
        {
            "model": "ridge_regression",
            **{f"validation_{k}": v for k, v in best_ridge_val.items()},
            **_metrics(y_test, predictions["ridge_regression"].to_numpy(dtype=float)),
            "selected_params": f"alpha={best_alpha}",
        }
    )

    lgbm_params, lgbm_val_metrics = _best_lightgbm_params(train_array, y_train, val_array, y_val)
    if lgbm_params is not None and lgbm_val_metrics is not None:
        lightgbm_pred = _predict_lightgbm(train_val_array, y_train_val, test_array, lgbm_params)
        predictions["lightgbm"] = np.clip(lightgbm_pred, 0, None)
        metric_rows.append(
            {
                "model": "lightgbm",
                **{f"validation_{k}": v for k, v in lgbm_val_metrics.items()},
                **_metrics(y_test, predictions["lightgbm"].to_numpy(dtype=float)),
                "selected_params": "; ".join(f"{key}={value}" for key, value in lgbm_params.items()),
            }
        )

        ridge_train_fit, ridge_val_base = _ridge_regression_fit_predict(
            train_array,
            y_train,
            val_array,
            alpha=float(best_alpha),
        )
        residual_train = y_train - ridge_train_fit

        residual_best_params = None
        residual_best_metrics = None
        residual_param_grid = [
            {"n_estimators": 60, "learning_rate": 0.035, "num_leaves": 7, "min_child_samples": 8, "subsample": 0.85, "colsample_bytree": 0.85, "reg_lambda": 2.0},
            {"n_estimators": 100, "learning_rate": 0.035, "num_leaves": 15, "min_child_samples": 8, "subsample": 0.85, "colsample_bytree": 0.85, "reg_lambda": 2.0},
            {"n_estimators": 120, "learning_rate": 0.025, "num_leaves": 15, "min_child_samples": 12, "subsample": 0.85, "colsample_bytree": 0.85, "reg_lambda": 4.0},
            {"n_estimators": 160, "learning_rate": 0.02, "num_leaves": 31, "min_child_samples": 12, "subsample": 0.85, "colsample_bytree": 0.85, "reg_lambda": 4.0},
        ]
        for params in residual_param_grid:
            residual_val = _predict_lightgbm(train_array, residual_train, val_array, params)
            if residual_val is None:
                break
            combined_val = np.clip(ridge_val_base + residual_val, 0, None)
            metrics = _metrics(y_val, combined_val)
            if residual_best_metrics is None or metrics["RMSE"] < residual_best_metrics["RMSE"]:
                residual_best_params = params
                residual_best_metrics = metrics

        if residual_best_params is not None and residual_best_metrics is not None:
            ridge_train_val_fit, ridge_test_base = _ridge_regression_fit_predict(
                train_val_array,
                y_train_val,
                test_array,
                alpha=float(best_alpha),
            )
            residual_train_val = y_train_val - ridge_train_val_fit
            residual_test = _predict_lightgbm(train_val_array, residual_train_val, test_array, residual_best_params)
            predictions["ridge_lightgbm_residual"] = np.clip(ridge_test_base + residual_test, 0, None)
            metric_rows.append(
                {
                    "model": "ridge_lightgbm_residual",
                    **{f"validation_{k}": v for k, v in residual_best_metrics.items()},
                    **_metrics(y_test, predictions["ridge_lightgbm_residual"].to_numpy(dtype=float)),
                    "selected_params": f"ridge_alpha={best_alpha}; residual_lightgbm="
                    + "; ".join(f"{key}={value}" for key, value in residual_best_params.items()),
                }
            )

    metrics = pd.DataFrame(metric_rows).sort_values("RMSE").reset_index(drop=True)
    return metrics, predictions, split_summary
