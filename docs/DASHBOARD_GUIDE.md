# Dashboard Guide

The dashboard files live here:

```text
dashboards/screenshots/
```

They are SVG files, so GitHub can show them easily.

## What The Dashboard Is For

The dashboard is not trying to be a fancy BI product.

It's there so someone can open the repo and quickly see:

- sales trends,
- top categories,
- forecast errors,
- category segments,
- campaign comparison.

That matters because a project shouldn't only work in code. It should also be easy to explain.

## Executive Summary

File:

```text
dashboards/screenshots/executive_summary.svg
```

This view answers:

> "What happened overall?"

It shows the main run details, the best forecast model, the segment labels, and the campaign warning.

## Category View

File:

```text
dashboards/screenshots/category_view.svg
```

This view answers:

> "Which product categories matter most?"

It shows the top categories and how the category groups look.

## Forecast View

File:

```text
dashboards/screenshots/forecast_view.svg
```

This view answers:

> "How close were the forecasts?"

It compares actual sales with the forecast and shows model RMSE values.

## Segment View

File:

```text
dashboards/screenshots/segment_view.svg
```

This view answers:

> "Which categories behave alike?"

It shows the four groups:

- high-value growing,
- stable core,
- campaign-responsive,
- low-volume niche.

## Campaign Comparison View

File:

```text
dashboards/screenshots/campaign_comparison_view.svg
```

This view answers:

> "Did campaign rows look different?"

It also says the important part: this is not proof that the campaign caused the difference.

## Fictional Example

Imagine a fictional sales manager named Riya.

Riya doesn't want to read five CSV files. She wants a quick answer before a weekly review meeting:

> "Which categories should I ask the team about?"

The dashboard helps her start that conversation. It doesn't replace deeper analysis, but it points her to the right places.
