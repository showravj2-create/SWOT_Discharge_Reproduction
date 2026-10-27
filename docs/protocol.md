# Scientific reproduction protocol

## Target

Andreadis et al. (2025), *A First Look at River Discharge Estimation From SWOT Satellite Observations*, DOI 10.1029/2024GL114185.

The article reports an assessment over the first 15 months of the SWOT mission, March 2023–July 2024, at 65 gauged reaches, with median correlation 0.73 (IQR 0.51–0.89) and median bias 50%.

## Step 1 — Freeze the protocol before inspecting results

Write down:
- exact SWOT product and version;
- exact quality fields and allowed values;
- gauging-station source and reach mapping;
- timestamp matching/aggregation method;
- discharge units;
- minimum valid pairs per reach;
- correlation and bias definitions.

The published paper and supporting information take precedence over the starter defaults. This repository's generic `quality_ok` column is a user-prepared flag, not an assertion about the paper's native field names.

## Step 2 — Harmonize

For each reach, match observations by stable ID and time. Use a documented tolerance. If the gauge is daily, specify how satellite overpass time maps to daily gauge flow. Keep a matching audit table with original timestamps and time differences.

## Step 3 — Filter

Apply the fixed date window [2023-03-01, 2024-08-01). Apply the paper's exact high-quality filter after confirming it from supporting information and product metadata. Exclude missing/non-finite values. Do not select observations based on whether they agree with the gauge.

## Step 4 — Per-reach metrics

This starter calculates:
- Pearson correlation;
- mean relative bias (%) = 100 × (mean(SWOT) − mean(gauge)) / mean(gauge);
- median absolute error;
- RMSE;
- number of paired observations.

**Metric caveat:** the article's precise bias definition must be verified before claiming exact reproduction. The code labels its chosen definition explicitly. Do not equate this definition with the paper's unless verified.

## Step 5 — Aggregate across reaches

Calculate median and interquartile range of per-reach correlation and median of per-reach bias. Do not pool all daily samples into one correlation because reaches with more observations would dominate.

## Step 6 — Compare

Compare the calculated values with published reference values. Explain discrepancies; do not tune filters until the values match. A near match alone does not prove exact reproduction.

## Step 7 — Report

Include:
- data product versions and retrieval date;
- exact filters and time-matching procedure;
- number of reaches and samples before/after each filter;
- per-reach metrics;
- aggregate metrics and uncertainty;
- examples of time series and scatterplots;
- limitations and deviations from the paper.
