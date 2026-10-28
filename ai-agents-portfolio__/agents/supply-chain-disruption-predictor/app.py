import numpy as np
import pandas as pd
import streamlit as st

st.title("Supply Chain Disruption Predictor")
st.caption("Sample data. Scores supplier risk and simulates what a delay would do to production.")

# ---- 1. Sample suppliers
rng = np.random.default_rng(8)
df = pd.DataFrame({
    "supplier": [f"Supplier {i}" for i in range(1, 9)],
    "component": ["Engine", "Steel", "Tyres", "Seats", "Chips", "Paint", "Glass", "Wiring"],
    "on_time_rate": rng.uniform(0.70, 0.99, 8).round(2),
    "lead_time_std_days": rng.uniform(1, 8, 8).round(1),
    "criticality_1to5": rng.integers(1, 6, 8),
    "stock_cover_days": rng.integers(3, 30, 8),
    "orders_per_day_at_risk": rng.integers(50, 200, 8),
})

# ---- 2. Risk = likelihood x impact
likelihood = (1 - df.on_time_rate) * 0.7 + (df.lead_time_std_days / 10) * 0.3
impact = df.criticality_1to5 / 5
df["risk_score"] = (likelihood * impact * 100).round(1)
df["risk_level"] = pd.qcut(df.risk_score.rank(method="first"), 3, labels=["Low", "Medium", "High"])
st.subheader("Supplier risk")
st.dataframe(df.sort_values("risk_score", ascending=False))

# ---- 3. Simulate a delay
st.subheader("What if a supplier is late?")
who = st.selectbox("Supplier", df.supplier)
delay = st.slider("Delay (days)", 0, 30, 10)
row = df[df.supplier == who].iloc[0]
stop_days = max(0, delay - row.stock_cover_days)
orders = stop_days * row.orders_per_day_at_risk
c1, c2 = st.columns(2)
c1.metric("Production stoppage (days)", stop_days)
c2.metric("Customer orders delayed", int(orders))

if stop_days == 0:
    st.success(f"Stock covers {row.stock_cover_days} days, so no stoppage.")
elif stop_days <= 2:
    st.warning("Recommended: expedite the shipment.")
else:
    st.error("Recommended: switch to a backup supplier and re-plan production.")
if stop_days > 0 and row.criticality_1to5 >= 4:
    st.info("High-impact action: send to a manager for approval before acting.")
