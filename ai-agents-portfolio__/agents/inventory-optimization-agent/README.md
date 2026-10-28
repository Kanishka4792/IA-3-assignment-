# Inventory Optimization Agent

## Problem
Stockouts on popular items and excess stock on slow ones.

## Solution
Recent-demand forecast, safety stock, reorder point and EOQ per product, with a manager-approval limit.

## Data
All data is **synthetic sample data** generated inside `app.py` (no files or API keys needed). Replace the "Sample data" section with your own CSV to use real data.

## Run it
```
pip install -r requirements.txt
streamlit run app.py
```

## Limitations
Results come from simulated data and simple models. They show associations, not proven causes, and a human should review any decision.
