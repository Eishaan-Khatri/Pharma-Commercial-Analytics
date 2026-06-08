from __future__ import annotations

import numpy as np
import pandas as pd


def make_monthly_category_features(df: pd.DataFrame) -> pd.DataFrame:
    monthly = (
        df.groupby(["month", "drug_category"], as_index=False)
        .agg(
            net_sales=("net_sales", "sum"),
            units_sold=("units_sold", "sum"),
            transaction_count=("transaction_id", "count"),
            avg_discount_rate=("discount_rate", "mean"),
            campaign_share=("campaign_flag", "mean"),
        )
        .sort_values(["drug_category", "month"])
    )
    monthly["month_date"] = pd.to_datetime(monthly["month"] + "-01")

    grouped = monthly.groupby("drug_category", group_keys=False)
    monthly["lag_1_sales"] = grouped["net_sales"].shift(1)
    monthly["lag_2_sales"] = grouped["net_sales"].shift(2)
    monthly["lag_1_units"] = grouped["units_sold"].shift(1)
    monthly["lag_1_transaction_count"] = grouped["transaction_count"].shift(1)
    monthly["lag_1_avg_discount_rate"] = grouped["avg_discount_rate"].shift(1)
    monthly["lag_1_campaign_share"] = grouped["campaign_share"].shift(1)
    monthly["rolling_3_sales"] = grouped["net_sales"].transform(
        lambda s: s.shift(1).rolling(3, min_periods=1).mean()
    )
    monthly["rolling_3_units"] = grouped["units_sold"].transform(
        lambda s: s.shift(1).rolling(3, min_periods=1).mean()
    )
    monthly["month_number"] = monthly["month_date"].dt.month
    monthly["time_index"] = (
        (monthly["month_date"].dt.year - monthly["month_date"].dt.year.min()) * 12
        + monthly["month_date"].dt.month
    )
    return monthly


def make_segmentation_features(df: pd.DataFrame) -> pd.DataFrame:
    category = (
        df.groupby("drug_category", as_index=False)
        .agg(
            total_net_sales=("net_sales", "sum"),
            total_units=("units_sold", "sum"),
            transaction_count=("transaction_id", "count"),
            avg_order_value=("net_sales", "mean"),
            avg_discount_rate=("discount_rate", "mean"),
            campaign_share=("campaign_flag", "mean"),
        )
    )

    monthly = (
        df.groupby(["drug_category", "month"], as_index=False)
        .agg(monthly_sales=("net_sales", "sum"))
        .sort_values(["drug_category", "month"])
    )
    volatility = monthly.groupby("drug_category", as_index=False).agg(
        revenue_volatility=("monthly_sales", "std"),
        average_monthly_sales=("monthly_sales", "mean"),
    )

    def growth_rate(group: pd.DataFrame) -> float:
        group = group.sort_values("month")
        split = max(len(group) // 2, 1)
        first = group.iloc[:split]["monthly_sales"].mean()
        second = group.iloc[split:]["monthly_sales"].mean()
        if first == 0 or np.isnan(first):
            return 0.0
        return float((second - first) / first)

    growth = monthly.groupby("drug_category").apply(growth_rate).reset_index(name="growth_rate")
    out = category.merge(volatility, on="drug_category", how="left").merge(growth, on="drug_category", how="left")
    out["revenue_volatility"] = out["revenue_volatility"].fillna(0)
    out["growth_rate"] = out["growth_rate"].fillna(0)
    return out
