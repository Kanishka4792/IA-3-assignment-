# Supply Chain Disruption Predictor

## Problem
Supply problems are noticed too late and delay production.

## Solution
Risk = likelihood x impact per supplier, plus a simulator showing production stoppage from a supplier delay.

## Data
All data is **synthetic sample data** generated inside `app.py` (no files or API keys needed). Replace the "Sample data" section with your own CSV to use real data.

## Run it
```
pip install -r requirements.txt
streamlit run app.py
```

## Limitations
Results come from simulated data and simple models. They show associations, not proven causes, and a human should review any decision.
