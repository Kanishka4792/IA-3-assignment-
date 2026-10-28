import pandas as pd
import streamlit as st

st.title("Profitability Decline Investigator")
st.caption("Sample data. Shows which departments' costs are pulling profit down.")

# ---- 1. Sample quarterly data from four departments
q = [f"Q{i}" for i in range(1, 9)]
df = pd.DataFrame({
    "revenue": [1000, 1060, 1120, 1180, 1210, 1230, 1245, 1255],
    "marketing": [60, 62, 66, 75, 88, 105, 125, 150],
    "labour": [200, 204, 210, 220, 236, 256, 278, 300],
    "operations": [100, 101, 102, 103, 104, 105, 106, 107],
    "logistics": [80, 82, 86, 93, 104, 118, 135, 155],
}, index=q)
df["cogs"] = df.revenue * 0.40
costs = ["cogs", "marketing", "labour", "operations", "logistics"]
df["profit"] = df.revenue - df[costs].sum(axis=1)
dept = {"revenue": "Marketing/Sales", "cogs": "Finance", "marketing": "Marketing",
        "labour": "HR", "operations": "Operations", "logistics": "Operations"}

st.subheader("Profit by quarter")
st.line_chart(df.profit)

# ---- 2. What changed between the peak and now?
peak = df.profit.idxmax()
latest = df.index[-1]
impact = {"revenue": df.revenue[latest] - df.revenue[peak]}
for c in costs:
    impact[c] = -(df[c][latest] - df[c][peak])            # higher cost = lower profit
imp = pd.DataFrame({"profit impact": pd.Series(impact)})
imp["department"] = imp.index.map(dept)
imp = imp.sort_values("profit impact")
st.subheader(f"What changed from the peak ({peak}) to {latest}")
st.metric("Profit change", f"{df.profit[latest] - df.profit[peak]:.0f}")
st.bar_chart(imp["profit impact"])
st.dataframe(imp)

# ---- 3. Cross-department links
st.subheader("Do department numbers move together?")
st.dataframe(df[["marketing", "labour", "logistics", "revenue"]].corr().round(2))
worst = imp.index[0]
st.error(f"The biggest drag is **{worst}** ({imp.loc[worst, 'department']}), costing {abs(imp.loc[worst, 'profit impact']):.0f}. "
         "Marketing growth and rising logistics cost move together, so each department can look fine "
         "while the company loses profit. Review marketing, HR and Operations plans jointly.")
