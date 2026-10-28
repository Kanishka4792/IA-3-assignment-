# Marketing Budget Optimizer

## Problem
Management cannot tell which marketing campaigns bring profitable customers.

## Solution
Fits a diminishing-returns curve (revenue = k x spend^b) per channel, then gives each slice of budget to the channel with the best marginal return.

## Data
All data is **synthetic sample data** generated inside `app.py` (no files or API keys needed). Replace the "Sample data" section with your own CSV to use real data.

## Run it
```
pip install -r requirements.txt
streamlit run app.py
```

## Limitations
Results come from simulated data and simple models. They show associations, not proven causes, and a human should review any decision.
