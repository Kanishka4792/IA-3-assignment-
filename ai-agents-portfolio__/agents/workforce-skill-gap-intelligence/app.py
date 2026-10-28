import numpy as np
import pandas as pd
import streamlit as st

st.title("Workforce Capacity & Skill Gap Intelligence")
st.caption("Sample data. Compares the skills we have with the skills projects need.")

# ---- 1. Sample skills inventory (hours per week each employee can give to each skill)
rng = np.random.default_rng(6)
skills = ["Python", "SQL", "Cloud", "Design", "Testing", "Project Mgmt"]
rows = []
for e in range(1, 31):
    for s in rng.choice(skills, rng.integers(1, 3), replace=False):
        rows.append([f"Emp{e}", s, int(rng.integers(10, 35))])
inv = pd.DataFrame(rows, columns=["employee", "skill", "hours_available"])
capacity = inv.groupby("skill").hours_available.sum().reindex(skills).fillna(0)

# ---- 2. Sample project demand per week
demand = pd.DataFrame({f"Week {w}": rng.integers(60, 260, len(skills)) for w in range(1, 9)}, index=skills)
week = st.selectbox("Week", demand.columns)

# ---- 3. Gap = demand - capacity
tbl = pd.DataFrame({"demand (hrs)": demand[week], "capacity (hrs)": capacity})
tbl["gap (hrs)"] = tbl["demand (hrs)"] - tbl["capacity (hrs)"]

def advice(r):
    if r["gap (hrs)"] <= 0:
        return "OK"
    if r["gap (hrs)"] <= 0.25 * r["demand (hrs)"]:
        return "Train existing staff / reassign"
    return "Hire or contract"

tbl["recommendation"] = tbl.apply(advice, axis=1)
st.dataframe(tbl.sort_values("gap (hrs)", ascending=False))
st.bar_chart(tbl[["demand (hrs)", "capacity (hrs)"]])
worst = tbl["gap (hrs)"].idxmax()
if tbl.loc[worst, "gap (hrs)"] > 0:
    st.error(f"Critical gap: **{worst}** is short by {tbl.loc[worst, 'gap (hrs)']} hours in {week}.")
else:
    st.success("Capacity covers demand for every skill this week.")
