import pandas as pd
import streamlit as st

st.title("What-If Business Simulator")
st.caption("Sample numbers. Shows whether the business can handle higher sales.")

# ---- 1. Current usage and capacity per month (edit these to match a real business)
base = pd.DataFrame({
    "current_usage": [4500, 8200, 10000, 9000],
    "capacity": [5500, 9000, 11500, 10000],
    "cost_per_extra_unit": [25, 12, 8, 15],
}, index=["Staff hours", "Production units", "Inventory units", "Deliveries"])

# ---- 2. Scenario
growth = st.slider("Increase in sales (%)", 0, 60, 20)
tbl = base.copy()
tbl["needed"] = (tbl.current_usage * (1 + growth / 100)).round()
tbl["utilization"] = (tbl.needed / tbl.capacity).round(2)
tbl["shortfall"] = (tbl.needed - tbl.capacity).clip(lower=0)
tbl["extra_cost"] = tbl.shortfall * tbl.cost_per_extra_unit
st.dataframe(tbl[["needed", "capacity", "utilization", "shortfall", "extra_cost"]])
st.bar_chart(tbl.utilization)

# ---- 3. Results
max_growth = (tbl.capacity / tbl.current_usage).min() - 1
bottleneck = tbl.utilization.idxmax()
c1, c2 = st.columns(2)
c1.metric("Maximum growth without new investment", f"{max_growth:.0%}")
c2.metric("Extra monthly cost for this scenario", f"{tbl.extra_cost.sum():,.0f}")

if tbl.shortfall.sum() == 0:
    st.success(f"All resources can support +{growth}% sales. Tightest area: {bottleneck}.")
else:
    st.error(f"Bottleneck: **{bottleneck}** ({tbl.utilization[bottleneck]:.0%} utilised).")
    st.write("Options: hire or use overtime for staff, outsource production or delivery, "
             "or phase the sales growth in stages.")
st.caption("This is a scenario, not a forecast.")
