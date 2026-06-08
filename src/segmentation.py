from __future__ import annotations

import pandas as pd


SEGMENT_FEATURES = [
    "total_net_sales",
    "total_units",
    "transaction_count",
    "avg_order_value",
    "avg_discount_rate",
    "campaign_share",
    "revenue_volatility",
    "growth_rate",
]


def run_segmentation(features: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    x = features[SEGMENT_FEATURES].fillna(0).to_numpy(dtype=float)
    x_scaled = _standardize(x)

    score_rows = []
    for k in range(2, 8):
        labels, centroids, inertia = _kmeans(x_scaled, k=k, seed=42)
        score_rows.append(
            {
                "k": k,
                "inertia": float(inertia),
                "silhouette": float(_silhouette_score(x_scaled, labels)),
            }
        )
    scores = pd.DataFrame(score_rows)
    best_k = int(scores.sort_values("silhouette", ascending=False).iloc[0]["k"])

    labels, _, _ = _kmeans(x_scaled, k=best_k, seed=42)
    segmented = features.copy()
    segmented["cluster"] = labels

    profiles = (
        segmented.groupby("cluster", as_index=False)
        .agg(
            categories=("drug_category", "count"),
            total_net_sales=("total_net_sales", "mean"),
            avg_order_value=("avg_order_value", "mean"),
            avg_discount_rate=("avg_discount_rate", "mean"),
            campaign_share=("campaign_share", "mean"),
            growth_rate=("growth_rate", "mean"),
            revenue_volatility=("revenue_volatility", "mean"),
        )
        .sort_values("total_net_sales", ascending=False)
    )
    profiles["segment_label"] = _label_profiles(profiles)
    segmented = segmented.merge(profiles[["cluster", "segment_label"]], on="cluster", how="left")
    return scores, segmented, profiles


def _label_profiles(profiles: pd.DataFrame) -> list[str]:
    top_sales_cluster = profiles.sort_values("total_net_sales", ascending=False).iloc[0]["cluster"]
    volatility_high = profiles["revenue_volatility"].median()
    campaign_high = profiles["campaign_share"].median()
    discount_high = profiles["avg_discount_rate"].median()
    low_sales = profiles["total_net_sales"].median()

    labels = []
    for _, row in profiles.iterrows():
        if row["cluster"] == top_sales_cluster and row["growth_rate"] > 0:
            labels.append("High-value growing categories")
        elif row["campaign_share"] >= campaign_high and row["growth_rate"] > 0:
            labels.append("Campaign-responsive categories")
        elif row["revenue_volatility"] >= volatility_high:
            labels.append("Volatile categories")
        elif row["avg_discount_rate"] >= discount_high:
            labels.append("Discount-sensitive categories")
        elif row["total_net_sales"] < low_sales:
            labels.append("Niche low-volume categories")
        else:
            labels.append("Stable baseline categories")
    return labels


def _standardize(x):
    mean = x.mean(axis=0)
    std = x.std(axis=0)
    std[std == 0] = 1.0
    return (x - mean) / std


def _kmeans(x, k: int, seed: int = 42, max_iter: int = 100):
    import numpy as np

    rng = np.random.default_rng(seed + k)
    centroids = x[rng.choice(len(x), size=k, replace=False)].copy()
    labels = np.zeros(len(x), dtype=int)

    for _ in range(max_iter):
        distances = ((x[:, None, :] - centroids[None, :, :]) ** 2).sum(axis=2)
        new_labels = distances.argmin(axis=1)
        if np.array_equal(labels, new_labels):
            break
        labels = new_labels
        for cluster in range(k):
            members = x[labels == cluster]
            if len(members) == 0:
                centroids[cluster] = x[rng.integers(0, len(x))]
            else:
                centroids[cluster] = members.mean(axis=0)

    inertia = float(((x - centroids[labels]) ** 2).sum())
    return labels, centroids, inertia


def _silhouette_score(x, labels):
    import numpy as np

    unique_labels = np.unique(labels)
    if len(unique_labels) < 2:
        return 0.0

    scores = []
    for i, point in enumerate(x):
        own_label = labels[i]
        own_cluster = x[labels == own_label]
        if len(own_cluster) <= 1:
            a = 0.0
        else:
            a = np.sqrt(((own_cluster - point) ** 2).sum(axis=1)).sum() / (len(own_cluster) - 1)

        b_values = []
        for other_label in unique_labels:
            if other_label == own_label:
                continue
            other_cluster = x[labels == other_label]
            b_values.append(np.sqrt(((other_cluster - point) ** 2).sum(axis=1)).mean())
        b = min(b_values)
        denom = max(a, b)
        scores.append(0.0 if denom == 0 else (b - a) / denom)

    return float(np.mean(scores))
