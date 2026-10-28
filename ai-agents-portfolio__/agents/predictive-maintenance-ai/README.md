# Predictive Maintenance AI

## Problem
Unexpected machine failures cause downtime and cost.

## Solution
Random Forest predicts failure within 7 days from sensor data; priority = risk x criticality; maintenance is placed on the lowest-load day.

## Data
All data is **synthetic sample data** generated inside `app.py` (no files or API keys needed). Replace the "Sample data" section with your own CSV to use real data.

## Run it
```
pip install -r requirements.txt
streamlit run app.py
```

## Limitations
Results come from simulated data and simple models. They show associations, not proven causes, and a human should review any decision.
