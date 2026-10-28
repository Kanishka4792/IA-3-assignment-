# Customer Churn & Retention Intelligence

## Problem
A subscription business is losing customers despite marketing spend.

## Solution
Logistic regression scores churn risk; K-Means groups at-risk customers; a rule picks the main driver of each group and suggests an action.

## Data
All data is **synthetic sample data** generated inside `app.py` (no files or API keys needed). Replace the "Sample data" section with your own CSV to use real data.

## Run it
```
pip install -r requirements.txt
streamlit run app.py
```

## Limitations
Results come from simulated data and simple models. They show associations, not proven causes, and a human should review any decision.
