from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from src.config import (
    CHANNELS,
    CUSTOMER_SEGMENTS,
    DRUG_CATEGORIES,
    RANDOM_SEED,
    REGIONS,
    SAMPLE_DATA_PATH,
    ensure_directories,
)


def _category_parameters(rng: np.random.Generator) -> pd.DataFrame:
    weights = rng.dirichlet(np.linspace(3.0, 0.7, len(DRUG_CATEGORIES)))
    base_prices = rng.lognormal(mean=4.0, sigma=0.45, size=len(DRUG_CATEGORIES))
    base_units = rng.integers(4, 35, size=len(DRUG_CATEGORIES))
    trend = rng.normal(loc=0.015, scale=0.035, size=len(DRUG_CATEGORIES))
    campaign_lift = rng.uniform(0.04, 0.22, size=len(DRUG_CATEGORIES))

    return pd.DataFrame(
        {
            "drug_category": DRUG_CATEGORIES,
            "category_weight": weights,
            "base_price": base_prices,
            "base_units": base_units,
            "trend": trend,
            "campaign_lift": campaign_lift,
        }
    )


def generate_transactions(rows: int = 25_000, seed: int = RANDOM_SEED) -> pd.DataFrame:
    """Generate public synthetic transaction data for the rebuilt project."""
    rng = np.random.default_rng(seed)
    params = _category_parameters(rng)

    dates = pd.date_range("2024-01-01", "2025-12-31", freq="D")
    chosen_dates = rng.choice(dates, size=rows, replace=True)
    category_idx = rng.choice(len(params), size=rows, p=params["category_weight"].to_numpy())
    selected = params.iloc[category_idx].reset_index(drop=True)

    region = rng.choice(REGIONS, size=rows, p=[0.24, 0.22, 0.17, 0.24, 0.13])
    channel = rng.choice(CHANNELS, size=rows, p=[0.35, 0.23, 0.24, 0.10, 0.08])
    segment = rng.choice(CUSTOMER_SEGMENTS, size=rows, p=[0.18, 0.22, 0.20, 0.24, 0.08, 0.08])

    months = pd.DatetimeIndex(chosen_dates).month.to_numpy()
    month_index = ((pd.DatetimeIndex(chosen_dates).year - 2024) * 12 + months - 1).to_numpy()
    seasonality = 1.0 + 0.12 * np.sin((months - 1) / 12 * 2 * np.pi)
    trend_multiplier = 1.0 + selected["trend"].to_numpy() * month_index

    campaign_probability = np.where(np.isin(months, [3, 4, 9, 10]), 0.26, 0.12)
    campaign_flag = rng.binomial(1, campaign_probability)
    campaign_multiplier = 1.0 + campaign_flag * selected["campaign_lift"].to_numpy()

    channel_multiplier = pd.Series(channel).map(
        {"Retail": 1.00, "Hospital": 1.18, "Distributor": 1.35, "Online": 0.82, "Government": 1.55}
    ).to_numpy()

    expected_units = (
        selected["base_units"].to_numpy()
        * seasonality
        * trend_multiplier.clip(0.55, 1.65)
        * campaign_multiplier
        * channel_multiplier
    )
    units_sold = rng.poisson(np.maximum(expected_units, 1)).clip(1, None)

    product_suffix = rng.integers(1, 9, size=rows)
    product_id = [
        f"{cat[:3].upper().replace(' ', '')}-{suffix:02d}"
        for cat, suffix in zip(selected["drug_category"], product_suffix)
    ]

    price_noise = rng.normal(1.0, 0.08, size=rows).clip(0.75, 1.30)
    unit_price = selected["base_price"].to_numpy() * price_noise

    base_discount = rng.beta(2.0, 14.0, size=rows)
    campaign_discount = campaign_flag * rng.uniform(0.04, 0.12, size=rows)
    channel_discount = pd.Series(channel).map(
        {"Retail": 0.03, "Hospital": 0.05, "Distributor": 0.08, "Online": 0.04, "Government": 0.10}
    ).to_numpy()
    discount_rate = (base_discount + campaign_discount + channel_discount).clip(0.0, 0.38)

    gross_sales = units_sold * unit_price
    discount_amount = gross_sales * discount_rate
    net_sales = gross_sales - discount_amount

    df = pd.DataFrame(
        {
            "transaction_id": [f"TXN-{i + 1:08d}" for i in range(rows)],
            "transaction_date": pd.to_datetime(chosen_dates).strftime("%Y-%m-%d"),
            "drug_category": selected["drug_category"].to_numpy(),
            "product_id": product_id,
            "region": region,
            "channel": channel,
            "customer_segment": segment,
            "units_sold": units_sold.astype(int),
            "unit_price": np.round(unit_price, 2),
            "gross_sales": np.round(gross_sales, 2),
            "discount_rate": np.round(discount_rate, 4),
            "discount_amount": np.round(discount_amount, 2),
            "net_sales": np.round(net_sales, 2),
            "campaign_flag": campaign_flag.astype(int),
        }
    )
    return df.sort_values("transaction_date").reset_index(drop=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synthetic pharma transaction data.")
    parser.add_argument("--rows", type=int, default=25_000, help="Number of synthetic rows to generate.")
    parser.add_argument("--seed", type=int, default=RANDOM_SEED, help="Random seed.")
    parser.add_argument("--output", type=Path, default=SAMPLE_DATA_PATH, help="Output CSV path.")
    args = parser.parse_args()

    ensure_directories()
    df = generate_transactions(rows=args.rows, seed=args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.output, index=False)
    print(f"Generated {len(df):,} rows at {args.output}")


if __name__ == "__main__":
    main()

