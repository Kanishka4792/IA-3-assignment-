import numpy as np
import pandas as pd
import streamlit as st

st.title("Delivery Performance Root-Cause Finder")
st.caption("Sample data. Finds where late deliveries come from.")

# ---- 1. Sample orders
rng = np.random.default_rng(11)
n = 3000
staff = {"Warehouse A": 0.95, "Warehouse B": 0.90, "Warehouse C": 0.65, "Warehouse D": 0.92}
df = pd.DataFrame({
    "warehouse": rng.choice(list(staff), n, p=[.3, .3, .15, .25]),
    "carrier": rng.choice(["Carrier X", "Carrier Y", "Carrier Z"], n, p=[.4, .4, .2]),
    "in_stock": rng.random(n) < 0.95,
    "promised_days": rng.integers(3, 6, n),
})
df["staffing_level"] = df.warehouse.map(staff)
actual = (df.promised_days + rng.normal(0, 0.4, n)
          + np.where(df.carrier == "Carrier Z", 0.9, 0)
          + np.where(df.staffing_level < 0.8, 2, 0)
          + np.where(~df.in_stock, 2, 0))
df["delay_days"] = (actual - df.promised_days).clip(lower=0).round()
df["late"] = df.delay_days >= 1
df["review"] = (5 - 0.7 * df.delay_days).clip(1, 5)

st.metric("Overall late rate", f"{df.late.mean():.0%}")

# ---- 2. Break the delays down
st.subheader("Late rate by warehouse")
st.bar_chart(df.groupby("warehouse").late.mean())
st.subheader("Late rate by carrier")
st.bar_chart(df.groupby("carrier").late.mean())
st.subheader("Stock availability")
st.dataframe(df.groupby("in_stock").late.mean().rename("late rate"))
st.subheader("Review score by delay (days)")
st.bar_chart(df.groupby("delay_days").review.mean())
st.caption("Delay and low reviews move together. That is an association, not proof of cause.")

# ---- 3. Rank the worst combinations
combo = df.groupby(["warehouse", "carrier"]).agg(orders=("late", "size"), late_orders=("late", "sum"),
                                                late_rate=("late", "mean"))
combo["priority_score"] = (combo.late_rate * combo.late_orders).round(1)
combo = combo.sort_values("priority_score", ascending=False)
st.subheader("Top problem areas")
st.dataframe(combo.head(5))
worst_wh = df.groupby("warehouse").late.mean().idxmax()
worst_car = df.groupby("carrier").late.mean().idxmax()
st.error(f"Worst warehouse: **{worst_wh}** (staffing level {staff[worst_wh]:.0%}) - check staffing and stock there. "
         f"Worst carrier: **{worst_car}** - review its service level.")
