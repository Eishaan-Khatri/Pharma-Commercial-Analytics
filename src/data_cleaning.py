from __future__ import annotations

import pandas as pd


REQUIRED_COLUMNS = [
    "transaction_id",
    "transaction_date",
    "drug_category",
    "product_id",
    "region",
    "channel",
    "customer_segment",
    "units_sold",
    "unit_price",
    "gross_sales",
    "discount_rate",
    "discount_amount",
    "net_sales",
    "campaign_flag",
]


def clean_transactions(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    missing_columns = sorted(set(REQUIRED_COLUMNS) - set(df.columns))
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    quality_rows = []
    quality_rows.append({"check": "raw_rows", "value": len(df)})

    df = df.copy()
    df = df.drop_duplicates(subset=["transaction_id"])
    quality_rows.append({"check": "rows_after_deduplication", "value": len(df)})

    df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")
    numeric_columns = [
        "units_sold",
        "unit_price",
        "gross_sales",
        "discount_rate",
        "discount_amount",
        "net_sales",
        "campaign_flag",
    ]
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    before_valid = len(df)
    df = df.dropna(subset=["transaction_date", "drug_category", "product_id", "region", "channel"])
    df = df[(df["units_sold"] > 0) & (df["unit_price"] >= 0) & (df["gross_sales"] >= 0) & (df["net_sales"] >= 0)]
    quality_rows.append({"check": "rows_removed_invalid_or_missing", "value": before_valid - len(df)})

    df["drug_category"] = df["drug_category"].astype(str).str.strip()
    df["region"] = df["region"].astype(str).str.strip()
    df["channel"] = df["channel"].astype(str).str.strip()
    df["customer_segment"] = df["customer_segment"].astype(str).str.strip()
    df["campaign_flag"] = df["campaign_flag"].fillna(0).astype(int).clip(0, 1)

    df["month"] = df["transaction_date"].dt.to_period("M").astype(str)
    df["quarter"] = df["transaction_date"].dt.to_period("Q").astype(str)
    df["average_selling_price"] = df["net_sales"] / df["units_sold"].replace(0, pd.NA)
    df["average_selling_price"] = df["average_selling_price"].fillna(0).round(2)

    quality_rows.extend(
        [
            {"check": "clean_rows", "value": len(df)},
            {"check": "date_min", "value": str(df["transaction_date"].min().date())},
            {"check": "date_max", "value": str(df["transaction_date"].max().date())},
            {"check": "drug_categories", "value": df["drug_category"].nunique()},
            {"check": "regions", "value": df["region"].nunique()},
            {"check": "channels", "value": df["channel"].nunique()},
        ]
    )

    quality_report = pd.DataFrame(quality_rows)
    return df.sort_values("transaction_date").reset_index(drop=True), quality_report

