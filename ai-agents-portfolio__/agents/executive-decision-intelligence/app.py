import numpy as np
import pandas as pd
import streamlit as st
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

st.title("Executive Decision Intelligence")
st.caption("Sample data. Finds which KPIs actually move revenue.")

# ---- 1. Sample monthly KPIs and revenue (36 months)
rng = np.random.default_rng(12)
n = 36
df = pd.DataFrame({
    "marketing_spend": rng.normal(50, 8, n),
    "headcount": np.linspace(100, 120, n) + rng.normal(0, 2, n),
    "delivery_days": rng.normal(4, 0.6, n),
    "defect_rate": rng.normal(2, 0.4, n),
    "nps": rng.normal(45, 6, n),
    "utilization": rng.normal(78, 5, n),
})
df["revenue"] = (20 + 2 * df.marketing_spend + 1.5 * df.nps - 25 * df.delivery_days
                 - 10 * df.defect_rate + rng.normal(0, 10, n))
df.loc[20, "revenue"] -= 60                              # a hidden bad month
kpis = [c for c in df.columns if c != "revenue"]

# ---- 2. Which KPIs move with revenue?
st.subheader("Correlation of each KPI with revenue")
corr = df[kpis].corrwith(df.revenue).sort_values()
st.bar_chart(corr)

# ---- 3. Regression on standardised KPIs: train on first 30 months, test on last 6
sc = StandardScaler().fit(df[kpis])
X = sc.transform(df[kpis])
model = LinearRegression().fit(X[:30], df.revenue[:30])
st.metric("Model fit on the last 6 months (R2)", f"{model.score(X[30:], df.revenue[30:]):.2f}")
coef = pd.Series(model.coef_, index=kpis).sort_values(key=abs, ascending=False)
st.subheader("KPI influence (revenue change per 1 standard deviation)")
st.bar_chart(coef)

# ---- 4. Odd months
resid = df.revenue - model.predict(X)
odd = df[(resid - resid.mean()).abs() > 2.5 * resid.std()]
if len(odd):
    st.warning(f"Unusual revenue in month(s): {', '.join(str(i + 1) for i in odd.index)}")

# ---- 5. Executive summary (built only from the numbers above)
top = coef.index[:2]
st.info(f"Revenue is most sensitive to **{top[0]}** ({coef[top[0]]:+.1f}) and **{top[1]}** ({coef[top[1]]:+.1f}). "
        "Focus management attention on these KPIs. This shows association, not proof of cause.")
