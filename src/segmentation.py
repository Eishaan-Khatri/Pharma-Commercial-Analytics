from __future__ import annotations

import numpy as np
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
    labels_by_k = {}
    for k in range(2, 8):
        labels, inertia, silhouette = _fit_kmeans(x_scaled, k=k, seed=42)
        labels_by_k[k] = labels
        score_rows.append(
            {
                "k": k,
                "inertia": float(inertia),
                "silhouette": float(silhouette),
                "selection_note": "business_selected" if k == 4 else "diagnostic",
            }
        )
    scores = pd.DataFrame(score_rows)

    selected_k = 4
    labels = labels_by_k[selected_k]
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
        .reset_index(drop=True)
    )
    profiles["segment_label"] = _label_profiles(profiles)
    segmented = segmented.merge(profiles[["cluster", "segment_label"]], on="cluster", how="left")
    return scores, segmented, profiles


def _label_profiles(profiles: pd.DataFrame) -> list[str]:
    labels_by_cluster: dict[int, str] = {}
    remaining = set(profiles["cluster"].tolist())

    low_volume_cluster = int(profiles.sort_values("total_net_sales", ascending=True).iloc[0]["cluster"])
    labels_by_cluster[low_volume_cluster] = "Low-volume niche"
    remaining.discard(low_volume_cluster)

    high_value_candidates = profiles[profiles["cluster"].isin(remaining)].copy()
    high_value_candidates["score"] = (
        high_value_candidates["total_net_sales"].rank(pct=True)
        + high_value_candidates["growth_rate"].rank(pct=True)
    )
    high_value_cluster = int(high_value_candidates.sort_values("score", ascending=False).iloc[0]["cluster"])
    labels_by_cluster[high_value_cluster] = "High-value growing"
    remaining.discard(high_value_cluster)

    campaign_candidates = profiles[profiles["cluster"].isin(remaining)].copy()
    campaign_cluster = int(campaign_candidates.sort_values("campaign_share", ascending=False).iloc[0]["cluster"])
    labels_by_cluster[campaign_cluster] = "Campaign-responsive"
    remaining.discard(campaign_cluster)

    for cluster in remaining:
        labels_by_cluster[int(cluster)] = "Stable core"

    return [labels_by_cluster[int(cluster)] for cluster in profiles["cluster"]]


def _standardize(x: np.ndarray) -> np.ndarray:
    mean = x.mean(axis=0)
    std = x.std(axis=0)
    std[std == 0] = 1.0
    return (x - mean) / std


def _fit_kmeans(x: np.ndarray, k: int, seed: int = 42) -> tuple[np.ndarray, float, float]:
    try:
        from sklearn.cluster import KMeans
        from sklearn.metrics import silhouette_score

        model = KMeans(n_clusters=k, random_state=seed, n_init=50)
        labels = model.fit_predict(x)
        silhouette = silhouette_score(x, labels)
        return labels, float(model.inertia_), float(silhouette)
    except Exception:
        labels, _, inertia = _kmeans_fallback(x, k=k, seed=seed)
        return labels, float(inertia), float(_silhouette_score_fallback(x, labels))


def _kmeans_fallback(x: np.ndarray, k: int, seed: int = 42, max_iter: int = 100):
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


def _silhouette_score_fallback(x: np.ndarray, labels: np.ndarray) -> float:
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
