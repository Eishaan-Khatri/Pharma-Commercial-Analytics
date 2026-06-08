# Final Project Report

This rebuilt project demonstrates a complete pharma commercial analytics workflow using synthetic public sample data.

## Workflow

1. Generate transaction-style sample data.
2. Clean and validate transaction fields.
3. Aggregate SQL-style business metrics.
4. Forecast month-category revenue.
5. Segment drug categories using K-means.
6. Compare campaign and non-campaign groups cautiously.
7. Generate dashboard-style screenshots and reports.

## Main Outputs

- Data quality report: `outputs/tables/data_quality_report.csv`
- Forecast metrics: `outputs/tables/forecast_model_metrics.csv`
- Segment profiles: `outputs/tables/segment_profiles.csv`
- A/B-style analysis: `outputs/tables/ab_style_inference.csv`
- Executive dashboard: `dashboards/screenshots/executive_dashboard.svg`

## Best Forecasting Model In Sample Run

ridge_regression with RMSE 8,538.73.

## Key Limitation

The data in this public repository is synthetic. It shows analytics workflow quality, not real pharma business outcomes.
