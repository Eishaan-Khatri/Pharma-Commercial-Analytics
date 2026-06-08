# GitHub Pages Guide

This repository includes a static project website:

```text
index.html
assets/site.css
assets/site.js
```

It is designed to work directly with GitHub Pages from the repository root.

## Enable GitHub Pages

1. Push this repository to GitHub.
2. Open the repository settings.
3. Go to **Pages**.
4. Select:
   - Source: `Deploy from a branch`
   - Branch: `main`
   - Folder: `/root`
5. Save.

The site should become available at:

```text
https://eishaan-khatri.github.io/Pharma-Commercial-Analytics/
```

## What The Site Is For

The website is not a generic landing page. It is a project case study built around:

- generated dashboard output,
- sample-run metrics,
- workflow explanation,
- method choices,
- risk/claim boundaries,
- repository proof links.

## Local Preview

Option 1: open directly:

```text
D:\CV\portfolio\Pharma-Commercial-Analytics\index.html
```

Option 2: serve locally:

```powershell
cd D:\CV\portfolio\Pharma-Commercial-Analytics
python -m http.server 8765
```

Then open:

```text
http://127.0.0.1:8765/
```

