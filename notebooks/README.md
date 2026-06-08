# Notebook Guide

These notebooks are small entry points for people who like checking work in notebook form.

The main pipeline is still:

```powershell
python -m src.run_pipeline --rows 25000 --force
```

Recommended order:

1. `01_eda.ipynb`
2. `02_forecasting.ipynb`
3. `03_segmentation.ipynb`
4. `04_ab_style_analysis.ipynb`

If GitHub does not show notebook outputs, run the pipeline first. The important proof files are also saved in `outputs/`, `reports/`, and `dashboards/screenshots/`.
