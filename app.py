import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import random

st.set_page_config(
    page_title="Transaction Insights • Emergent",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

PAGE_STYLE = """
<style>
:root {
    color-scheme: dark;
}
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top left, rgba(16, 185, 129, 0.18), transparent 22%),
                radial-gradient(circle at bottom right, rgba(59, 130, 246, 0.12), transparent 18%),
                linear-gradient(180deg, #020817 0%, #06152f 35%, #061c38 100%);
}
.hero-panel {
    position: relative;
    overflow: hidden;
    margin-bottom: 1.5rem;
    border-radius: 28px;
    box-shadow: 0 40px 120px rgba(0, 0, 0, 0.35);
    background: rgba(8, 23, 44, 0.92);
    border: 1px solid rgba(255, 255, 255, 0.08);
}
.hero-panel::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at 20% 20%, rgba(16, 185, 129, 0.25), transparent 20%),
                radial-gradient(circle at 80% 20%, rgba(59, 130, 246, 0.15), transparent 18%),
                radial-gradient(circle at 70% 80%, rgba(139, 92, 246, 0.12), transparent 25%);
    pointer-events: none;
}
.hero-content {
    position: relative;
    padding: 3rem 3rem 3rem 2.5rem;
    display: grid;
    grid-template-columns: 1.6fr 1fr;
    align-items: center;
    gap: 2rem;
    min-height: 320px;
}
.hero-copy h1 {
    margin: 0 0 0.75rem;
    font-size: clamp(2rem, 4vw, 3.2rem);
    line-height: 1.05;
    letter-spacing: -0.04em;
    color: #f8fafc;
}
.hero-copy p {
    margin: 0;
    max-width: 640px;
    font-size: 1.05rem;
    opacity: 0.88;
    color: #dbeafe;
}
.hero-badges {
    margin-top: 1.5rem;
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
}
.hero-badge {
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 999px;
    padding: 0.85rem 1.2rem;
    font-size: 0.92rem;
    color: #e2e8f0;
    backdrop-filter: blur(10px);
}
.hero-animation {
    position: relative;
    min-height: 260px;
    display: flex;
    align-items: center;
    justify-content: center;
}
.cube-scene {
    width: 220px;
    height: 220px;
    position: relative;
    transform-style: preserve-3d;
    animation: rotateCube 12s linear infinite;
}
.cube-side {
    position: absolute;
    width: 200px;
    height: 200px;
    border-radius: 24px;
    border: 2px solid rgba(255, 255, 255, 0.14);
    background: rgba(14, 100, 172, 0.38);
    box-shadow: inset 0 0 30px rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(8px);
}
.cube-side.front { transform: translateZ(100px); background: rgba(16, 185, 129, 0.2); }
.cube-side.back { transform: rotateY(180deg) translateZ(100px); background: rgba(59, 130, 246, 0.18); }
.cube-side.right { transform: rotateY(90deg) translateZ(100px); background: rgba(139, 92, 246, 0.18); }
.cube-side.left { transform: rotateY(-90deg) translateZ(100px); background: rgba(16, 185, 129, 0.15); }
.cube-side.top { transform: rotateX(90deg) translateZ(100px); background: rgba(59, 130, 246, 0.15); }
.cube-side.bottom { transform: rotateX(-90deg) translateZ(100px); background: rgba(139, 92, 246, 0.12); }
.pulse-ring {
    position: absolute;
    width: 360px;
    height: 360px;
    border-radius: 50%;
    box-shadow: 0 0 0 0 rgba(56, 189, 248, 0.24);
    animation: pulseRing 2.8s ease-out infinite;
}
.tiny-dot {
    position: absolute;
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: #10b981;
    box-shadow: 0 0 18px rgba(16, 185, 129, 0.65);
    top: 18%;
    left: 72%;
    animation: floatDot 5.4s ease-in-out infinite alternate;
}
.tiny-dot:nth-child(2) {
    top: 70%;
    left: 20%;
    background: #38bdf8;
    box-shadow: 0 0 18px rgba(56, 189, 248, 0.65);
    animation-duration: 6.2s;
}
@keyframes rotateCube {
    from { transform: rotateX(-25deg) rotateY(0deg); }
    to { transform: rotateX(-25deg) rotateY(360deg); }
}
@keyframes pulseRing {
    0% { box-shadow: 0 0 0 0 rgba(56, 189, 248, 0.35); }
    70% { box-shadow: 0 0 0 60px rgba(56, 189, 248, 0.06); }
    100% { box-shadow: 0 0 0 0 transparent; }
}
@keyframes floatDot {
    from { transform: translateY(0px); }
    to { transform: translateY(-18px); }
}
@media (max-width: 900px) {
    .hero-content {
        grid-template-columns: 1fr;
        padding: 2rem 1.5rem;
    }
    .hero-animation {
        margin-top: 1.5rem;
    }
}
</style>
"""

HERO_HTML = """
<div class="hero-panel">
  <div class="hero-content">
    <div class="hero-copy">
      <h1>📊 Transaction Insights</h1>
      <p>Real-time retail performance dashboard with immersive 3D visuals, animated analytics, and fast data-driven decision support.</p>
      <div class="hero-badges">
        <div class="hero-badge">Live sales tracking</div>
        <div class="hero-badge">3D analytics visual</div>
        <div class="hero-badge">AI-powered recommendations</div>
      </div>
    </div>
    <div class="hero-animation">
      <div class="cube-scene">
        <div class="cube-side front"></div>
        <div class="cube-side back"></div>
        <div class="cube-side right"></div>
        <div class="cube-side left"></div>
        <div class="cube-side top"></div>
        <div class="cube-side bottom"></div>
      </div>
      <div class="pulse-ring"></div>
      <div class="tiny-dot"></div>
      <div class="tiny-dot"></div>
    </div>
  </div>
</div>
"""

st.markdown(PAGE_STYLE + HERO_HTML, unsafe_allow_html=True)

if "transactions" not in st.session_state:
    st.session_state.transactions = pd.DataFrame(
        {
            "date": pd.to_datetime(["2026-04-10", "2026-04-11", "2026-04-12", "2026-04-13"]),
            "product": ["Wireless Earbuds", "Smart Watch", "Laptop Sleeve", "Wireless Earbuds"],
            "category": ["Electronics", "Electronics", "Accessories", "Electronics"],
            "quantity": [12, 8, 25, 15],
            "price": [49.99, 49.99, 15.00, 49.99],
            "cost": [22.50, 22.50, 7.50, 22.50],
        }
    )

if "products" not in st.session_state:
    st.session_state.products = pd.DataFrame(
        {
            "product": ["Wireless Earbuds", "Smart Watch", "Laptop Sleeve"],
            "units_sold": [124, 87, 203],
            "revenue": [6199.76, 4349.13, 3045.00],
            "percent": [28, 20, 14],
        }
    )

if "show_form" not in st.session_state:
    st.session_state.show_form = False

if "insight" not in st.session_state:
    st.session_state.insight = "Add transactions to unlock AI-powered insights!"


def update_product_percent():
    if not st.session_state.products.empty:
        total_units = st.session_state.products["units_sold"].sum()
        if total_units > 0:
            st.session_state.products["percent"] = (
                st.session_state.products["units_sold"] / total_units * 100
            ).round(0)

update_product_percent()

col_header1, col_header2 = st.columns([4, 1])
with col_header1:
    st.caption("🔴 Live • Last updated just now")
with col_header2:
    if st.button("➕ Add New Transaction", use_container_width=True, type="primary"):
        st.session_state.show_form = True

with st.expander("🧠 AI Insights", expanded=True):
    st.write(st.session_state.insight)
    if st.button("✨ Generate New Insight"):
        insights = [
            "✅ Sales are up **34%** this week. Wireless Earbuds are your star performer!",
            "🔥 Customers who buy Electronics spend **2.4x** more on average.",
            "💡 Recommendation: Launch a bundle offer on Earbuds + Charger to boost revenue by ~18%.",
            "📈 Average order value increased by $12.50 since last month.",
        ]
        st.session_state.insight = random.choice(insights)
        st.experimental_rerun()

st.subheader("Key Metrics")
df = st.session_state.transactions.copy()
if not df.empty:
    df["revenue"] = df["quantity"] * df["price"]
    df["profit"] = df["revenue"] - (df["quantity"] * df["cost"])
    total_revenue = df["revenue"].sum()
    total_profit = df["profit"].sum()
    total_orders = len(df)
    avg_order = total_revenue / total_orders if total_orders > 0 else 0
else:
    total_revenue = total_profit = total_orders = avg_order = 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Revenue", f"${total_revenue:,.2f}", "↑ 12%")
c2.metric("Gross Profit", f"${total_profit:,.2f}", "↑ 18%")
c3.metric("Total Orders", total_orders, "↑ 4")
c4.metric("Avg Order Value", f"${avg_order:,.2f}", "↑ $3.20")

st.divider()

tab1, tab2 = st.tabs(["📈 Sales Performance", "🏆 Top Products"])

with tab1:
    st.subheader("Sales Performance")
    if not df.empty:
        df_daily = df.groupby("date", as_index=False)["revenue"].sum()
        line_fig = px.line(
            df_daily,
            x="date",
            y="revenue",
            title="Daily Revenue Trend",
            markers=True,
            line_shape="spline",
            color_discrete_sequence=["#10b981"],
        )
        line_fig.update_layout(height=420, template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(line_fig, use_container_width=True)

        scatter_3d_fig = px.scatter_3d(
            df,
            x="quantity",
            y="revenue",
            z="profit",
            color="category",
            size="quantity",
            hover_name="product",
            title="3D Revenue vs Quantity vs Profit",
            color_discrete_sequence=["#10b981", "#3b82f6", "#8b5cf6", "#f97316"],
        )
        scatter_3d_fig.update_layout(
            scene={
                "xaxis_title": "Quantity",
                "yaxis_title": "Revenue",
                "zaxis_title": "Profit",
                "xaxis": {"backgroundcolor": "rgba(0,0,0,0)"},
                "yaxis": {"backgroundcolor": "rgba(0,0,0,0)"},
                "zaxis": {"backgroundcolor": "rgba(0,0,0,0)"},
            },
            template="plotly_dark",
            margin={"l": 0, "r": 0, "t": 50, "b": 0},
            height=520,
        )
        st.plotly_chart(scatter_3d_fig, use_container_width=True)
    else:
        st.warning("No data yet. Add transactions to see the charts!")

with tab2:
    st.subheader("Top Performing Products")
    if not st.session_state.products.empty:
        st.dataframe(
            st.session_state.products.style.format(
                {
                    "revenue": "${:,.2f}",
                    "percent": "{:.0f}%",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No products yet.")

st.subheader("⚠️ Inventory Alerts")
alerts = [
    "🔴 Low stock: Wireless Earbuds (only 8 units left)",
    "🟡 Restock recommended: Smart Watch (projected out of stock in 5 days)",
    "🟢 Bluetooth Speaker is performing well – consider increasing stock",
]
for alert in alerts:
    st.warning(alert)

if st.session_state.show_form:
    with st.form("add_transaction", clear_on_submit=True):
        st.subheader("Add New Transaction")
        col_a, col_b = st.columns(2)
        with col_a:
            date = st.date_input("Date", value=datetime.today())
            product = st.text_input("Product Name", value="Wireless Earbuds")
        with col_b:
            category = st.selectbox(
                "Category",
                ["Electronics", "Fashion", "Home & Kitchen", "Beauty", "Accessories"],
            )
            quantity = st.number_input("Quantity", min_value=1, value=1)

        col_c, col_d = st.columns(2)
        with col_c:
            price = st.number_input("Selling Price ($)", min_value=0.01, value=49.99, step=0.01)
        with col_d:
            cost = st.number_input("Cost Price ($)", min_value=0.01, value=22.50, step=0.01)

        submitted = st.form_submit_button("Save Transaction", type="primary")
        if submitted:
            new_row = pd.DataFrame(
                [
                    {
                        "date": pd.to_datetime(date),
                        "product": product,
                        "category": category,
                        "quantity": quantity,
                        "price": price,
                        "cost": cost,
                    }
                ]
            )
            st.session_state.transactions = pd.concat(
                [st.session_state.transactions, new_row], ignore_index=True
            )

            existing = st.session_state.products[
                st.session_state.products["product"] == product
            ]
            if not existing.empty:
                idx = existing.index[0]
                st.session_state.products.at[idx, "units_sold"] += quantity
                st.session_state.products.at[idx, "revenue"] += quantity * price
            else:
                new_product = pd.DataFrame(
                    [
                        {
                            "product": product,
                            "units_sold": quantity,
                            "revenue": quantity * price,
                            "percent": 0,
                        }
                    ]
                )
                st.session_state.products = pd.concat(
                    [st.session_state.products, new_product], ignore_index=True
                )

            update_product_percent()
            st.success("✅ Transaction saved!")
            st.session_state.show_form = False
            st.experimental_rerun().