# Notebook Guide

These notebooks are lightweight entry points for reviewers who prefer notebook-based inspection. The main reproducible pipeline lives in `src/run_pipeline.py`.

Recommended order:

1. `01_eda.ipynb`
2. `02_forecasting.ipynb`
3. `03_segmentation.ipynb`
4. `04_ab_style_analysis.ipynb`

If a notebook does not show outputs on GitHub, run the full project first:

```powershell
python -m src.run_pipeline --rows 25000 --force
```

