"""Reproducible agribusiness data analysis for the Week 1 resubmission.

Input values are selected rows transcribed from the supplied Department of
Agriculture & Farmers Welfare (DA&FW) All-India Crop-wise Area, Production &
Yield table. The 2025-26 figures are labelled Third Advance Estimates.
Synthetic price-spread and supply-chain examples are generated only as
teaching scenarios; they are not observed market data.

Run:
    python -m pip install pandas numpy matplotlib
    python analyze_agri_data.py
"""
from pathlib import Path
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "crop_statistics_selected_all_india.csv"
OUT = ROOT / "outputs"
OUT.mkdir(parents=True, exist_ok=True)
EXPECTED_YEARS = ["2021-22", "2022-23", "2023-24", "2024-25", "2025-26"]
REQUIRED_COLUMNS = {
    "agricultural_year", "crop", "area_lakh_hectares", "production_value",
    "production_unit", "yield_kg_per_hectare", "estimate_status"
}

# 1. Load and validate the data.
df = pd.read_csv(DATA)
missing_columns = REQUIRED_COLUMNS - set(df.columns)
if missing_columns:
    raise ValueError(f"Required columns missing: {sorted(missing_columns)}")
if df[list(REQUIRED_COLUMNS)].isna().any().any():
    raise ValueError("Missing values exist in required columns. Review the source before analysis.")
if df.duplicated(["crop", "agricultural_year"]).any():
    dupes = df.loc[df.duplicated(["crop", "agricultural_year"], keep=False), ["crop", "agricultural_year"]]
    raise ValueError(f"Duplicate crop-year keys found:\n{dupes}")
if sorted(df["agricultural_year"].unique()) != EXPECTED_YEARS:
    raise ValueError(f"Unexpected year coverage: {sorted(df['agricultural_year'].unique())}")
for col in ["area_lakh_hectares", "production_value", "yield_kg_per_hectare"]:
    df[col] = pd.to_numeric(df[col], errors="raise")
    if (df[col] < 0).any():
        raise ValueError(f"Negative numeric values found in {col}; review before proceeding.")
# Production units must not silently change within the same crop's five-year series.
unit_counts = df.groupby("crop")["production_unit"].nunique()
if (unit_counts > 1).any():
    raise ValueError(f"Production unit changes found within crop(s): {unit_counts[unit_counts > 1].index.tolist()}")
if not df.loc[df.agricultural_year.eq("2025-26"), "estimate_status"].str.contains("Third Advance Estimate", case=False).all():
    raise ValueError("2025-26 status should be clearly marked as a Third Advance Estimate.")

# Machine-readable data-quality checks.
audit_rows = [
    ("Input row count", len(df), "PASS" if len(df) == 40 else "REVIEW", "Selected rows; expected 8 crop groups x 5 years"),
    ("Unique crop-year keys", df[["crop", "agricultural_year"]].drop_duplicates().shape[0], "PASS" if not df.duplicated(["crop", "agricultural_year"]).any() else "FAIL", "Each crop-year should appear once"),
    ("Distinct crop groups", df["crop"].nunique(), "PASS" if df["crop"].nunique() == 8 else "REVIEW", "Selected crop/aggregate groups, not the entire source table"),
    ("Expected years present", ", ".join(sorted(df["agricultural_year"].unique())), "PASS" if sorted(df["agricultural_year"].unique()) == EXPECTED_YEARS else "FAIL", "2021-22 through 2025-26"),
    ("Missing required values", int(df[list(REQUIRED_COLUMNS)].isna().sum().sum()), "PASS" if not df[list(REQUIRED_COLUMNS)].isna().any().any() else "FAIL", "Missing and zero values must be treated differently"),
    ("Negative values in numeric fields", int((df[["area_lakh_hectares", "production_value", "yield_kg_per_hectare"]] < 0).sum().sum()), "PASS" if not (df[["area_lakh_hectares", "production_value", "yield_kg_per_hectare"]] < 0).any().any() else "FAIL", "Range check only; does not verify every source transcription"),
    ("Consistent production unit within each crop", int(unit_counts.max()), "PASS" if (unit_counts <= 1).all() else "FAIL", "Unit may differ between crops, so compare within-crop percentage changes"),
]
pd.DataFrame(audit_rows, columns=["check", "result", "status", "interpretation"]).to_csv(OUT / "data_quality_audit.csv", index=False)

# 2. Endpoint descriptive analysis.
summary_rows = []
for crop, g in df.groupby("crop", sort=False):
    g = g.set_index("agricultural_year").loc[EXPECTED_YEARS]
    first, last = g.iloc[0], g.iloc[-1]
    summary_rows.append({
        "crop": crop,
        "area_2021_22_lakh_ha": first["area_lakh_hectares"],
        "area_2025_26_lakh_ha": last["area_lakh_hectares"],
        "area_change_pct": (last["area_lakh_hectares"] / first["area_lakh_hectares"] - 1) * 100,
        "production_2021_22": first["production_value"],
        "production_2025_26": last["production_value"],
        "production_unit": last["production_unit"],
        "production_change_pct": (last["production_value"] / first["production_value"] - 1) * 100,
        "yield_2021_22_kg_ha": first["yield_kg_per_hectare"],
        "yield_2025_26_kg_ha": last["yield_kg_per_hectare"],
        "yield_change_pct": (last["yield_kg_per_hectare"] / first["yield_kg_per_hectare"] - 1) * 100,
        "status_2025_26": last["estimate_status"]
    })
summary = pd.DataFrame(summary_rows)
summary.to_csv(OUT / "endpoint_change_metrics.csv", index=False, float_format="%.4f")

# Year-over-year analysis of the Total Food Grains aggregate.
food = df.loc[df["crop"].eq("Total Food Grains")].copy()
food["year_order"] = food["agricultural_year"].map({y: i for i, y in enumerate(EXPECTED_YEARS)})
food = food.sort_values("year_order").drop(columns="year_order")
food["yoy_change_pct"] = food["production_value"].pct_change() * 100
food.to_csv(OUT / "foodgrains_yoy_analysis.csv", index=False, float_format="%.4f")
food_vals = food["production_value"].to_numpy(float)
food_cagr = ((food_vals[-1] / food_vals[0]) ** (1 / (len(food_vals) - 1)) - 1) * 100
food_endpoint_change = (food_vals[-1] / food_vals[0] - 1) * 100

# 3. Historical single-holdout forecast-method demonstration on maize.
maize = df.loc[df["crop"].eq("Maize")].copy()
maize["year_order"] = maize["agricultural_year"].map({y: i for i, y in enumerate(EXPECTED_YEARS)})
maize = maize.sort_values("year_order")
maize_series = maize["production_value"].to_numpy(float)
train = maize_series[:-1]   # 2021-22 through 2024-25
reference_value = float(maize_series[-1])  # 2025-26 Third Advance Estimate
forecast_naive = float(train[-1])
forecast_ma3 = float(train[-3:].mean())
forecast_linear = float(np.polyval(np.polyfit(np.arange(len(train)), train, 1), len(train)))
forecast_rows = []
for method, forecast in [
    ("Naive (last available value)", forecast_naive),
    ("Three-year moving average", forecast_ma3),
    ("Linear trend (least squares)", forecast_linear),
]:
    error = reference_value - forecast
    forecast_rows.append({
        "method": method,
        "training_period": "2021-22 to 2024-25",
        "forecast_for": "2025-26",
        "forecast_lakh_tonnes": forecast,
        "reference_value_lakh_tonnes": reference_value,
        "signed_error_reference_minus_forecast": error,
        "absolute_error_lakh_tonnes": abs(error),
        "absolute_percentage_error_pct": abs(error) / abs(reference_value) * 100,
        "reference_status": "Third Advance Estimate; not final outturn",
        "validation_note": "Single holdout comparison only; not enough to validate a reliable model"
    })
maize_holdout = pd.DataFrame(forecast_rows)
maize_holdout.to_csv(OUT / "maize_forecast_holdout_comparison.csv", index=False, float_format="%.4f")

# Forward-looking demonstration for food-grain production. These values have no observed target here.
food_naive = float(food_vals[-1])
food_ma3 = float(food_vals[-3:].mean())
food_linear = float(np.polyval(np.polyfit(np.arange(len(food_vals)), food_vals, 1), len(food_vals)))
next_year_rows = []
for method, forecast in [
    ("Naive baseline", food_naive),
    ("Three-year moving average", food_ma3),
    ("Linear trend (least squares)", food_linear),
]:
    next_year_rows.append({
        "method": method,
        "illustrative_forecast_for": "2026-27",
        "forecast_lakh_tonnes": forecast,
        "status": "Illustrative scenario only; no 2026-27 comparison value and no validated predictive claim"
    })
pd.DataFrame(next_year_rows).to_csv(OUT / "foodgrains_2026_27_illustrative_forecasts.csv", index=False, float_format="%.4f")

# 4. Synthetic teaching scenario: price spread. NOT observed market data.
price = pd.DataFrame([
    {"stage": "Farm-gate", "illustrative_price_inr_per_kg": 18.0, "data_status": "HYPOTHETICAL - teaching scenario"},
    {"stage": "Wholesale", "illustrative_price_inr_per_kg": 24.0, "data_status": "HYPOTHETICAL - teaching scenario"},
    {"stage": "Retail", "illustrative_price_inr_per_kg": 32.0, "data_status": "HYPOTHETICAL - teaching scenario"},
])
price.to_csv(OUT / "hypothetical_price_spread_scenario.csv", index=False)
retail_spread = float(price.iloc[-1]["illustrative_price_inr_per_kg"] - price.iloc[0]["illustrative_price_inr_per_kg"])
wholesale_gap = float(price.iloc[1]["illustrative_price_inr_per_kg"] - price.iloc[0]["illustrative_price_inr_per_kg"])

# Synthetic teaching scenario: staged physical losses. Each percentage applies to the quantity entering that stage.
quantity = 1000.0
supply_rows = [{"stage": "Harvested quantity", "input_kg": quantity, "loss_rate_pct": 0.0, "loss_kg": 0.0, "output_kg": quantity, "data_status": "HYPOTHETICAL - teaching scenario"}]
for stage, rate_pct in [("Collection", 2.0), ("Storage", 4.0), ("Transport", 2.0)]:
    loss = quantity * rate_pct / 100.0
    output = quantity - loss
    supply_rows.append({"stage": stage, "input_kg": quantity, "loss_rate_pct": rate_pct, "loss_kg": loss, "output_kg": output, "data_status": "HYPOTHETICAL - teaching scenario"})
    quantity = output
supply = pd.DataFrame(supply_rows)
supply.to_csv(OUT / "hypothetical_supply_chain_loss_scenario.csv", index=False, float_format="%.4f")
total_loss_pct = (1000.0 - quantity) / 1000.0 * 100.0

# 5. Visualisations. Each chart title states scope and unit.
plt.figure(figsize=(9, 5.2))
plt.plot(food["agricultural_year"], food["production_value"], marker="o", linewidth=2.2)
plt.title("All-India Total Food-Grain Production (2021-22 to 2025-26)")
plt.xlabel("Agricultural year")
plt.ylabel("Production (lakh tonnes)")
plt.grid(True, alpha=0.25)
plt.tight_layout()
plt.savefig(OUT / "foodgrains_production_trend.png", dpi=180)
plt.close()

plot = summary.sort_values("production_change_pct")
plt.figure(figsize=(9, 5.4))
plt.barh(plot["crop"], plot["production_change_pct"])
plt.axvline(0, linewidth=0.8)
plt.title("Endpoint Change in Reported Production (2021-22 to 2025-26)")
plt.xlabel("Change (%) within each crop's reported production unit")
plt.tight_layout()
plt.savefig(OUT / "production_endpoint_change.png", dpi=180)
plt.close()

# Maize variables are shown in separate panels because their units differ.
fig, axes = plt.subplots(3, 1, figsize=(9, 8.2), sharex=True)
axes[0].plot(maize["agricultural_year"], maize["area_lakh_hectares"], marker="o", color="#0f766e")
axes[0].set_ylabel("Area (lakh ha)")
axes[0].grid(True, alpha=0.2)
axes[1].plot(maize["agricultural_year"], maize["production_value"], marker="o", color="#2563eb")
axes[1].set_ylabel("Production (lakh tonnes)")
axes[1].grid(True, alpha=0.2)
axes[2].plot(maize["agricultural_year"], maize["yield_kg_per_hectare"], marker="o", color="#b45309")
axes[2].set_ylabel("Yield (kg/ha)")
axes[2].grid(True, alpha=0.2)
axes[2].set_xlabel("Agricultural year")
fig.suptitle("Maize: Area, Production and Yield (India, 2021-22 to 2025-26)", y=0.99)
fig.tight_layout()
fig.savefig(OUT / "maize_area_production_yield.png", dpi=180)
plt.close(fig)

plt.figure(figsize=(9, 5.1))
plt.bar(maize_holdout["method"], maize_holdout["forecast_lakh_tonnes"], label="Forecast")
plt.axhline(reference_value, color="#b91c1c", linestyle="--", linewidth=2, label="2025-26 Third Advance Estimate")
plt.ylabel("Maize production (lakh tonnes)")
plt.title("One-Point Holdout Demonstration: Maize Forecast Methods")
plt.xticks(rotation=12, ha="right")
plt.ylim(0, 630)
plt.xticks(rotation=10, ha="right", fontsize=8)
plt.legend(loc="upper right")
plt.tight_layout()
plt.savefig(OUT / "maize_forecast_holdout.png", dpi=180)
plt.close()

# 6. Human-readable summary.
maize_first = maize.iloc[0]
maize_last = maize.iloc[-1]
maize_prod_change = (maize_last["production_value"] / maize_first["production_value"] - 1) * 100
maize_area_change = (maize_last["area_lakh_hectares"] / maize_first["area_lakh_hectares"] - 1) * 100
maize_yield_change = (maize_last["yield_kg_per_hectare"] / maize_first["yield_kg_per_hectare"] - 1) * 100
with (OUT / "analysis_summary.txt").open("w", encoding="utf-8") as f:
    f.write("AGRIBUSINESS DATA ANALYSIS — REPRODUCIBLE SUMMARY\n")
    f.write("Source: selected crop rows transcribed from the supplied DA&FW All-India Crop-wise Area, Production & Yield table.\n")
    f.write("Source status: 2025-26 values are the Third Advance Estimates, not final outturns.\n")
    f.write("Data scope: selected eight crop/aggregate groups x five years; not the complete original table.\n\n")
    f.write(f"Maize production: {maize_first['production_value']:.2f} to {maize_last['production_value']:.2f} lakh tonnes; endpoint change {maize_prod_change:.2f}%.\n")
    f.write(f"Maize area: {maize_first['area_lakh_hectares']:.2f} to {maize_last['area_lakh_hectares']:.2f} lakh ha; endpoint change {maize_area_change:.2f}%.\n")
    f.write(f"Maize yield: {maize_first['yield_kg_per_hectare']:.0f} to {maize_last['yield_kg_per_hectare']:.0f} kg/ha; endpoint change {maize_yield_change:.2f}%.\n\n")
    f.write(f"Total food-grain production: {food_vals[0]:.2f} to {food_vals[-1]:.2f} lakh tonnes; endpoint change {food_endpoint_change:.2f}%; CAGR over four intervals {food_cagr:.2f}%.\n")
    f.write("Forecasting: the maize back-test-like demonstration has four training points and one comparison point. The 2025-26 comparison is itself a Third Advance Estimate. This cannot validate a reliable forecasting model.\n")
    f.write("Next-year food-grain forecasts are scenario outputs only, with no observed 2026-27 comparison value.\n\n")
    f.write(f"Hypothetical price example: farm-gate to retail spread = INR {retail_spread:.2f}/kg; farm-gate to wholesale gap = INR {wholesale_gap:.2f}/kg. These are not observed prices or profit margins.\n")
    f.write(f"Hypothetical supply-chain example: 1,000 kg falls to {quantity:.2f} kg after assumed stage losses; total loss {total_loss_pct:.2f}%. This is not observed loss data.\n")
    f.write("Output CSVs and charts are generated by analyze_agri_data.py.\n")

print("Analysis completed.")
print(f"Maize production change: {maize_prod_change:.2f}% | area: {maize_area_change:.2f}% | yield: {maize_yield_change:.2f}%")
print(f"Food grains endpoint change: {food_endpoint_change:.2f}% | CAGR: {food_cagr:.2f}%")
print("Maize single-holdout comparison:")
print(maize_holdout[["method", "forecast_lakh_tonnes", "absolute_error_lakh_tonnes", "absolute_percentage_error_pct"]].round(2).to_string(index=False))
print("IMPORTANT: single holdout / short series; not a validated predictive model.")
print(f"Generated outputs at: {OUT}")
