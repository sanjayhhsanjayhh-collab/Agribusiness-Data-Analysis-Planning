# Resubmission Changes — Response to Evaluator Feedback

| Feedback | What changed | Evidence |
|---|---|---|
| Report was broad and lacked concrete examples | Added a five-year maize table and original percentage calculations for area, production, and yield; added year-over-year total food-grain production analysis and CAGR formula. | Main report Section 5; Appendix A; `outputs/endpoint_change_metrics.csv`; `outputs/foodgrains_yoy_analysis.csv` |
| Forecasting methods were too vague | Worked through naïve, three-year moving-average, and linear-trend methods with exact forecasts, absolute errors, and absolute percentage errors using a time-ordered maize training period. | Main report Section 5; Appendix B; `outputs/maize_forecast_holdout_comparison.csv`; `outputs/maize_forecast_holdout.png` |
| Forecast reliability was overstated / insufficiently validated | Explicitly labelled the historical comparison as one holdout point and all forward projections as illustrative. No reliability claim is made from five annual observations. | Main report Section 5; Appendix B; notebook and README caveats |
| Price spread and supply-chain loss values lacked source data | Clearly labelled the ₹18/₹24/₹32 price example and 2%/4%/2% loss example as hypothetical teaching scenarios. The source crop table contains no price or measured loss values. | Appendix B; `outputs/hypothetical_price_spread_scenario.csv`; `outputs/hypothetical_supply_chain_loss_scenario.csv` |
| Timeline was generic | Added dated daily Week 1 tasks and dated follow-on project phases, with deliverables and acceptance checks. | Main report Section 6 |
| Evaluation criteria lacked depth | Added a weighted 1–5 rubric with detailed score anchors and a weighted-score formula; summary rubric weights match the expanded rubric. | Main report Section 8; Appendix D |
| Analysis was not reproducible | Packaged source data, source PDF, Python script, notebook, requirements, audit CSV, calculation outputs, and charts. | `analyze_agri_data.py`, `Agribusiness_Data_Analysis_Reproducible.ipynb`, `outputs/`, `README_Resubmission.md` |
