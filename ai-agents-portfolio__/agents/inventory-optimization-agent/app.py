import numpy as np
import pandas as pd
import streamlit as st

st.title("Inventory Optimization Agent")
st.caption("Sample data. Forecasts demand, then recommends when and how much to order.")

# ---- 1. Sample sales: 1 year of daily sales for 6 products with seasonality
rng = np.random.default_rng(10)
days = np.arange(365)
season = 1 + 0.3 * np.sin(2 * np.pi * days / 365)
products = {"P1": (50, 20, 5), "P2": (20, 50, 10), "P3": (80, 8, 3),
            "P4": (10, 200, 14), "P5": (35, 30, 7), "P6": (5, 120, 21)}   # base demand, unit cost, lead time
sales = pd.DataFrame({p: rng.poisson(v[0] * season) for p, v in products.items()})

# ---- 2. Settings
service = st.selectbox("Service level", [90, 95, 99], index=1)
z = {90: 1.28, 95: 1.65, 99: 2.33}[service]
approval_limit = st.number_input("Orders above this value need manager approval", value=5000)
ORDER_COST, HOLD_RATE = 50, 0.2

# ---- 3. Calculate
rows = []
for p, (base, cost, lead) in products.items():
    d = sales[p].tail(30).mean()                       # forecast: recent daily average
    sd = sales[p].tail(90).std()
    safety = z * sd * np.sqrt(lead)
    rop = d * lead + safety                            # reorder point
    eoq = np.sqrt(2 * d * 365 * ORDER_COST / (cost * HOLD_RATE))   # economic order quantity
    stock = int(rng.integers(0, int(rop * 2.5)))
    if stock < rop:
        status, qty = "Reorder now", int(np.ceil(eoq))
    elif stock > rop + 2 * eoq:
        status, qty = "Overstock - stop buying", 0
    else:
        status, qty = "OK", 0
    value = qty * cost
    rows.append([p, round(d, 1), round(safety), round(rop), round(eoq), stock, status, qty, value,
                 "Needs approval" if value > approval_limit else ""])
out = pd.DataFrame(rows, columns=["product", "daily demand", "safety stock", "reorder point", "EOQ",
                                  "stock now", "status", "order qty", "order value", "approval"])
st.dataframe(out)
st.line_chart(sales.rolling(14).mean())
