# AgriScope Analytics — Agribusiness Data Analysis Dashboard

**Student:** SANJAY H H  
**USN:** 1MJ24CD041  
**Course:** 5th Sem CSE (Data Science)  
**College:** MVJ College of Engineering, Bengaluru

## Run locally
1. Download/extract this folder.
2. Double-click `index.html` or right-click and open it in Chrome/Edge.
3. No Python, package installation, internet connection, API key, or account is required. The data is embedded in the HTML for offline operation.

## Dashboard features
- Crop/category and metric selectors for production, cultivated area, and yield.
- Latest value, endpoint change, maximum value, and observation count KPI cards.
- Five-year SVG trend chart and year-specific crop comparison.
- Forecast demonstration comparing a naïve baseline, a three-year moving average, and a linear trend using the first four years to predict the fifth.
- Absolute-error table and chart for the final-year holdout.
- Searchable data table and CSV export.
- Estimate-status labels and explicit data limitations.

## Data provenance and limitations
The data file contains selected All-India crop/category data transcribed from the supplied Department of Agriculture & Farmers Welfare (DA&FW) table, 2021–22 through 2025–26. The last year is marked as a third advance estimate in the source. Area is in lakh hectares; production is in lakh tonnes for most groups and lakh bales for cotton (1 bale = 170 kg); yield is in kg/ha. Refer to `source_DAandFW_crop_statistics_2025_26.pdf`.

This is a selected dataset (8 category groups × 5 years = 40 rows), not the complete official table. Aggregate rows overlap crop components. The dashboard excludes aggregate categories from the crop-comparison chart and excludes cotton from the production comparison because its production unit differs.

The final-year forecast comparison is a **single holdout demonstration only**. Five observations per series are not enough to make strong generalization claims; a proper model would need more years, rolling-origin evaluation, more predictors, and suitable error metrics. Price spread, losses, climate causality, and regional comparisons are not calculated because this dataset does not contain the required variables.

## Publish on GitHub Pages
1. Copy `index.html` and `README.md` into the root of your repository (the CSV and PDF are included as supporting/source files, though the dashboard has embedded data).
2. On GitHub, open **Settings → Pages**.
3. Choose deployment from the `main` branch and `/ (root)`, then save.
4. Wait for GitHub Pages to publish the site and open the URL shown in Settings → Pages.

## Files
- `index.html` — complete offline dashboard.
- `crop_statistics_selected_all_india.csv` — selected data used by the dashboard.
- `source_DAandFW_crop_statistics_2025_26.pdf` — source table supplied for the project.

- `dashboard_preview.png` — full-page reference screenshot of the interactive dashboard.
