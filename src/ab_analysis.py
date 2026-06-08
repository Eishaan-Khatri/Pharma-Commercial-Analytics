from __future__ import annotations

import numpy as np
import pandas as pd


def bootstrap_mean_difference(
    treatment: np.ndarray,
    control: np.ndarray,
    iterations: int = 2_000,
    seed: int = 42,
) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    diffs = []
    for _ in range(iterations):
        treat_sample = rng.choice(treatment, size=len(treatment), replace=True)
        control_sample = rng.choice(control, size=len(control), replace=True)
        diffs.append(treat_sample.mean() - control_sample.mean())
    lower, upper = np.percentile(diffs, [2.5, 97.5])
    return float(lower), float(upper)


def run_ab_style_analysis(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    summary = (
        df.groupby("campaign_flag", as_index=False)
        .agg(
            transactions=("transaction_id", "count"),
            avg_net_sales=("net_sales", "mean"),
            avg_units=("units_sold", "mean"),
            avg_discount_rate=("discount_rate", "mean"),
            total_net_sales=("net_sales", "sum"),
        )
        .replace({"campaign_flag": {0: "non_campaign", 1: "campaign"}})
    )

    campaign = df[df["campaign_flag"] == 1]["net_sales"].to_numpy()
    non_campaign = df[df["campaign_flag"] == 0]["net_sales"].to_numpy()
    observed_difference = float(campaign.mean() - non_campaign.mean())
    lower, upper = bootstrap_mean_difference(campaign, non_campaign)

    inference = pd.DataFrame(
        [
            {
                "metric": "avg_net_sales_difference_campaign_minus_non_campaign",
                "observed_difference": observed_difference,
                "bootstrap_ci_95_low": lower,
                "bootstrap_ci_95_high": upper,
                "interpretation": "Comparison only; not causal without randomized assignment.",
            }
        ]
    )
    return summary, inference

