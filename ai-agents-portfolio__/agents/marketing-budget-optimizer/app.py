import numpy as np
import pandas as pd
import streamlit as st

st.title("Marketing Budget Optimizer")
st.caption("Sample data. Finds weak spending and suggests a better budget split.")

# ---- 1. Sample data: 5 channels x 24 months (revenue grows with spend, but with diminishing returns)
rng = np.random.default_rng(1)
true = {"Google Ads": (60, 0.70), "Facebook": (45, 0.65), "Email": (120, 0.50),
        "LinkedIn": (35, 0.80), "YouTube": (40, 0.60)}
rows = []
for ch, (k, b) in true.items():
    for month in range(1, 25):
        spend = rng.uniform(2000, 20000)
        rows.append([ch, month, spend, k * spend ** b * rng.normal(1, 0.08)])
df = pd.DataFrame(rows, columns=["channel", "month", "spend", "revenue"])

# ---- 2. Fit revenue = k * spend^b for each channel (b < 1 means diminishing returns)
fits = {}
for ch, g in df.groupby("channel"):
    b, logk = np.polyfit(np.log(g.spend), np.log(g.revenue), 1)
    fits[ch] = (float(np.exp(logk)), float(np.clip(b, 0.1, 0.95)))
rev = lambda c, x: fits[c][0] * x ** fits[c][1]

# ---- 3. Give each budget slice to the channel with the best marginal return
current = df.groupby("channel").spend.mean()
total = st.slider("Total monthly budget", 20000, 150000, int(current.sum()), step=1000)
current_scaled = current / current.sum() * total

alloc = {c: 1000.0 for c in fits}
step = total / 200
left = total - sum(alloc.values())
while left >= step:
    best = max(fits, key=lambda c: fits[c][0] * fits[c][1] * alloc[c] ** (fits[c][1] - 1))
    alloc[best] += step
    left -= step

out = pd.DataFrame({"current spend": current_scaled.round(), "recommended spend": pd.Series(alloc).round()})
out["change"] = out["recommended spend"] - out["current spend"]
out["revenue now"] = [round(rev(c, current_scaled[c])) for c in out.index]
out["revenue after"] = [round(rev(c, alloc[c])) for c in out.index]
st.dataframe(out)

now, after = out["revenue now"].sum(), out["revenue after"].sum()
c1, c2 = st.columns(2)
c1.metric("Expected revenue (current split)", f"{now:,.0f}")
c2.metric("Expected revenue (recommended)", f"{after:,.0f}", f"{(after / now - 1):.1%}")
st.bar_chart(out[["current spend", "recommended spend"]])
st.info(f"Move budget towards **{out.change.idxmax()}** and away from **{out.change.idxmin()}**.")
