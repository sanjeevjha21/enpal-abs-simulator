import streamlit as st
import pandas as pd
import plotly.express as px

# I import the custom backend engine I built to process the 240-month sequential amortization
from abs_multi_period_simulator import MultiPeriodABSSimulator

# --- 1. UI Configuration & Branding ---
# I configure the main Streamlit page layout and title to give the dashboard a professional, wide-screen footprint.
st.set_page_config(page_title="Enpal ABS Simulator", layout="wide")

st.title("☀️ Enpal 'Golden Ray' ABS Simulator")
st.markdown(
    "Interactive Cashflow Waterfall & Amortization Dashboard simulating a €200M securitization over 240 months."
)

# --- 2. Interactive Macroeconomic Stress Testing ---
# I build the interactive sidebar where users can inject macroeconomic stress tests into my model.
st.sidebar.header("Macroeconomic Stress Tests")
st.sidebar.markdown(
    "Adjust these parameters to simulate how varying default and prepayment speeds impact the cashflow waterfall."
)

# I capture the Constant Default Rate (CDR) to simulate customers who permanently stop paying.
annual_default_rate = st.sidebar.slider(
    "Annual Default Rate (CDR)", 
    min_value=0.0, max_value=0.15, value=0.015, step=0.005, format="%.3f"
)

# I capture the Conditional Prepayment Rate (CPR) to simulate customers who pay off their systems early.
annual_prepayment_rate = st.sidebar.slider(
    "Annual Prepayment Rate (CPR)", 
    min_value=0.0, max_value=0.20, value=0.05, step=0.01, format="%.2f"
)

# --- 3. Backend Execution & Caching ---
# I use Streamlit's caching decorator (@st.cache_data) so my engine doesn't reload the heavy 10,000-row CSV 
# every time a user tweaks a UI slider. This drastically improves dashboard performance.
@st.cache_data 
def load_data(cdr, cpr):
    # I initialize my backend engine and execute the 20-year loop using the dynamic user inputs.
    simulator = MultiPeriodABSSimulator()
    df = simulator.run_simulation(
        annualized_default_rate=cdr, annualized_prepayment_rate=cpr
    )
    # I return the full 240-month timeline alongside the starting totals to populate the top-level KPI metrics.
    return df, simulator.initial_pool_balance, simulator.tranche_a_principal, simulator.tranche_b_principal

# I extract the results into distinct variables for immediate rendering.
results_df, start_pool, start_t_a, start_t_b = load_data(annual_default_rate, annual_prepayment_rate)

# --- 4. Key Performance Indicators (KPIs) ---
# I dynamically render the top-line KPI metrics so the user instantly grasps the initial scale of the portfolio.
st.header("Initial Portfolio Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Asset Value", f"€{start_pool:,.0f}")
col2.metric("Tranche A (Senior Debt)", f"€{start_t_a:,.0f}")
col3.metric("Tranche B (Mezzanine Debt)", f"€{start_t_b:,.0f}")

st.divider()

# --- 5. Amortization Data Visualization ---
st.subheader("20-Year Debt Paydown Trajectory")

# I transform (melt) my wide dataframe into a long format so Plotly can easily render multiple time-series lines on the same graph.
melted_df = results_df.melt(
    id_vars=["Month"], 
    value_vars=["Remaining Pool Balance", "Tranche A Balance", "Tranche B Balance"],
    var_name="Asset Class", 
    value_name="Balance (€)"
)

# I plot the sequential paydown logic, proving visually that Tranche A is retired before Tranche B.
fig1 = px.line(
    melted_df, 
    x="Month", 
    y="Balance (€)", 
    color="Asset Class",
    title="Sequential Amortization: Assets vs. Liabilities"
)
st.plotly_chart(fig1, width="stretch")

# --- 6. Residual Equity Visualization ---
st.subheader("Enpal Residual Equity Cash Flow")
st.markdown("This represents the pure profit flowing back to Enpal after all structural debt obligations are serviced.")

# Finally, I plot the residual cash flow as an area chart to visually demonstrate the recurring revenue Enpal retains.
fig2 = px.area(
    results_df, 
    x="Month", 
    y="Enpal Cash Flow",
    title="Monthly Free Cash Flow Output",
    color_discrete_sequence=["#2ecc71"] # I enforce Enpal's brand green for visual alignment.
)
st.plotly_chart(fig2, width="stretch")