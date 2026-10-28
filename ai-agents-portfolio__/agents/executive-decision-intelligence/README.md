# Executive Decision Intelligence

## Problem
Hundreds of KPIs, but no clarity on which ones explain performance.

## Solution
Correlation and standardised regression link KPIs to revenue; a holdout checks the fit; anomalies are flagged.

## Data
All data is **synthetic sample data** generated inside `app.py` (no files or API keys needed). Replace the "Sample data" section with your own CSV to use real data.

## Run it
```
pip install -r requirements.txt
streamlit run app.py
```

## Limitations
Results come from simulated data and simple models. They show associations, not proven causes, and a human should review any decision.
