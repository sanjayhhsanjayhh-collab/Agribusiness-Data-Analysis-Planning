# Agribusiness Data Analysis Planning — Final Resubmission

**Student:** SANJAY H H  
**USN:** 1MJ24CD041  
**Programme:** 5th Semester, CSE (Data Science)  
**Institution:** MVJ College of Engineering, Bengaluru

## Purpose

This package is built for the Week 1 assignment **Agribusiness Data Analysis Planning** and explicitly addresses the previous rejection feedback about vague forecasting methods, insufficient concrete numerical examples, generic milestones, brief evaluation criteria, and weak reproducibility.

## Main files

- `Agribusiness_Data_Analysis_Planning_Final_Resubmission_Sanjay_HH.docx` — editable final report with feedback-to-evidence map, original numerical analysis, worked forecasting methods, explicitly hypothetical price and loss examples, dated milestones, and weighted 1–5 evaluation rubric.
- `Agribusiness_Data_Analysis_Planning_Final_Resubmission_Sanjay_HH.pdf` — printable version of the same report.
- `source_DAandFW_crop_statistics_2025_26.pdf` — supplied 3-page DA&FW crop statistics table used for the worked national crop case study.
- `crop_statistics_selected_all_india.csv` — 40 selected rows (eight crop/aggregate groups × five agricultural years) transcribed from the source table.
- `analyze_agri_data.py` — reproducible Python analysis that validates the CSV, calculates metrics, creates forecast comparisons and saves output tables/charts.
- `Agribusiness_Data_Analysis_Reproducible.ipynb` — interactive notebook with the core workflow.
- `requirements.txt` — core Python dependencies.
- `outputs/` — generated CSVs, text summary and charts.

## Original numerical analysis

The source-backed maize comparison from 2021–22 to 2025–26 reports:

- Area: 99.58 to 144.08 lakh hectares, **+44.69%**.
- Production: 337.30 to 550.93 lakh tonnes, **+63.34%**.
- Yield: 3,387 to 3,824 kg/ha, **+12.90%**.

For total food grains, production moved from 3,156.16 to 3,765.63 lakh tonnes, an endpoint increase of **19.31%** and descriptive CAGR of approximately **4.51%** over four intervals.

**Important:** the 2025–26 figures in the supplied table are **Third Advance Estimates**, not final outturns. These are national values, not state/district-level results. Percent changes describe the reported endpoints and do not establish causes.

## Forecasting evidence and limitations

The maize demonstration trains on 2021–22 through 2024–25 and compares one-step-ahead estimates to the source-reported 2025–26 Third Advance Estimate. Results:

| Method | Forecast (lakh tonnes) | Absolute error | Absolute percentage error |
|---|---:|---:|---:|
| Naïve baseline | 434.09 | 116.84 | 21.21% |
| Three-year moving average | 397.20 | 153.73 | 27.90% |
| Linear trend | 453.77 | 97.17 | 17.64% |

This is one holdout point and the comparison value is an advance estimate. **It does not validate a reliable predictive model.** The separate 2026–27 food-grain outputs are illustrative projections without an observed target, so there is no forecast-accuracy claim. The report recommends longer history and rolling-origin/time-ordered validation with multiple test periods before model selection.

## Hypothetical examples are not real observations

- The ₹18/kg farm-gate, ₹24/kg wholesale and ₹32/kg retail figures exist only to demonstrate price-spread arithmetic. The spread is not profit or a net margin.
- The 1,000 kg post-harvest example uses assumed stage losses of 2%, 4% and 2% (each applied to the quantity entering that stage), resulting in approximately 921.98 kg and 7.80% net loss. These are not measured supply-chain loss rates.
- The supplied crop table has no actual historical mandi prices, market arrivals, farm input costs, crop-specific post-harvest losses or matched farm water use. Those conclusions require additional measured/public datasets.

## Reproduce the outputs

From this folder, run:

```bash
python -m pip install -r requirements.txt
python analyze_agri_data.py
```

This regenerates the CSV tables and charts in `outputs/`. To use the notebook, open `Agribusiness_Data_Analysis_Reproducible.ipynb` in Jupyter and run its cells in order. Keep the input CSV in this folder.

## Public data portals planned for future data collection

1. Department of Agriculture & Farmers Welfare, Third Advance Estimates for 2025–26: https://desagri.gov.in/whats-new-posts/third-advance-estimates-of-production-of-foodgrains-oilseeds-and-other-commercial-crops-for-the-2025-26/
2. e-NAM market trade details (state, APMC, commodity, date, prices, arrivals/traded quantities where available): https://www.enam.gov.in/web/dashboard/trade-data
3. India Meteorological Department, rainfall information: https://mausam.imd.gov.in/responsive/rainfallinformation_msd.php
4. World Bank Agriculture & Rural Development indicators: https://data.worldbank.org/topic/agriculture-and-rural-development
5. FAOSTAT: https://www.fao.org/faostat/
6. Research paper on integrated computer vision, IoT, blockchain and climate-smart cultivation: Safeer, S., Gallo, P., & Pulvento, C. (2025), *Internet of Things*, 34, 101749. https://doi.org/10.1016/j.iot.2025.101749

## Submission checklist

1. Upload the DOCX/PDF and the reproducible files to the project repository.
2. Include the data source and the current outputs; do not upload synthetic examples as if they were field observations.
3. Add a screenshot of the output charts or a short analysis walkthrough to the repository README.
4. Verify that the repository link used on the submission platform points to this updated version.
