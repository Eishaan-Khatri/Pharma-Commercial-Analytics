# GitHub Pages Guide

This repo has a static project page:

```text
index.html
assets/site.css
assets/site.js
```

It is meant to run from the repository root on GitHub Pages.

## Enable The Site

1. Push the repo to GitHub.
2. Open repository settings.
3. Go to **Pages**.
4. Choose:
   - Source: `Deploy from a branch`
   - Branch: `main`
   - Folder: `/root`
5. Save.

The site should open here:

```text
https://eishaan-khatri.github.io/Pharma-Commercial-Analytics/
```

## What The Site Does

The page is a case study. It shows:

- the dataset size,
- the model comparison,
- the dashboard output,
- the files that prove the claims,
- the limits of the project.

It is not meant to sound like a product ad.

## Local Preview

Open directly:

```text
D:\CV\portfolio\Pharma-Commercial-Analytics\index.html
```

Or run a small local server:

```powershell
cd D:\CV\portfolio\Pharma-Commercial-Analytics
python -m http.server 8765
```

Then open:

```text
http://127.0.0.1:8765/
```
