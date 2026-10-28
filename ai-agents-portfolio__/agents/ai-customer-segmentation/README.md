# AI Customer Segmentation

## Problem
Broad demographic segments make campaigns inefficient.

## Solution
K-Means on Recency, Frequency and Monetary value; silhouette score checks quality; rules label each segment and suggest a strategy.

## Data
All data is **synthetic sample data** generated inside `app.py` (no files or API keys needed). Replace the "Sample data" section with your own CSV to use real data.

## Run it
```
pip install -r requirements.txt
streamlit run app.py
```

## Limitations
Results come from simulated data and simple models. They show associations, not proven causes, and a human should review any decision.
