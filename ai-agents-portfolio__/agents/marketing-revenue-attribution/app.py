import numpy as np
import pandas as pd
import streamlit as st

st.title("Marketing-to-Revenue Attribution")
st.caption("Sample data. Shows where the funnel leaks and which channel deserves the credit.")

# ---- 1. Sample leads: each has 1-3 marketing touches and reaches a funnel stage (1=Lead ... 4=Won)
rng = np.random.default_rng(3)
channels = ["Search", "Social", "Email", "Webinar", "Referral"]
rows = []
for _ in range(2000):
    touches = list(rng.choice(channels, rng.integers(1, 4)))
    p = [.30, .30, .20, .20] if "Referral" in touches else [.50, .28, .14, .08]
    stage = rng.choice([1, 2, 3, 4], p=p)
    rows.append([touches, stage, rng.uniform(2000, 9000) if stage == 4 else 0])
df = pd.DataFrame(rows, columns=["touches", "stage", "revenue"])

# ---- 2. Funnel
funnel = pd.Series({"Lead": len(df), "MQL": (df.stage >= 2).sum(),
                    "SQL": (df.stage >= 3).sum(), "Won": (df.stage == 4).sum()})
conv = (funnel / funnel.shift(1)).dropna()
st.subheader("Funnel")
st.bar_chart(funnel)
st.dataframe(conv.rename("conversion from previous stage").map("{:.0%}".format))
worst = conv.idxmin()
st.error(f"Biggest leak: only {conv[worst]:.0%} of leads move on to **{worst}**.")

# ---- 3. Who gets the credit? Compare three attribution rules
won = df[df.stage == 4]
first = won.groupby(won.touches.str[0]).revenue.sum()
last = won.groupby(won.touches.str[-1]).revenue.sum()
linear = {}
for t, r in zip(won.touches, won.revenue):
    for c in t:
        linear[c] = linear.get(c, 0) + r / len(t)
attr = pd.DataFrame({"first touch": first, "last touch": last, "linear (equal split)": pd.Series(linear)}).fillna(0).round()
st.subheader("Revenue credit by channel")
st.dataframe(attr)
st.bar_chart(attr)
st.caption("If the three rules disagree, no single model is the truth. Treat the results as a range.")
