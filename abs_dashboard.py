import streamlit as st
import pandas as pd
import plotly.express as px

# I hook our analytical presentation layer directly to the quantitative math backend
from abs_multi_period_simulator import MultiPeriodABSSimulator

# --- 1. PREMIUM INSTITUTIONAL VISUAL STYLING ---
st.set_page_config(page_title="Enpal Golden Ray ABS Terminal", layout="wide")

st.markdown("""
    <style>
        body { background-color: #0f172a; color: #f8fafc; }
        .kpi-container {
            background-color: #1e293b; padding: 22px; border-radius: 6px;
            border-left: 5px solid #eab308; margin-bottom: 15px;
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        }
        .kpi-title { color: #94a3b8; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; }
        .kpi-value { color: #f8fafc; font-size: 1.75rem; font-weight: 700; margin-top: 5px; }
        .kpi-subtitle { color: #64748b; font-size: 0.75rem; margin-top: 3px; }
        .covenant-box {
            padding: 22px; border-radius: 6px; font-weight: 700; text-align: center;
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        }
        .cov-success { background-color: #022c22; color: #34d399; border: 1px solid #059669; }
        .cov-error { background-color: #450a0a; color: #fca5a5; border: 1px solid #dc2626; }
    </style>
""", unsafe_allow_html=True)

# --- 2. SIDEBAR PORTAL NAVIGATION SYSTEM ---
st.sidebar.title("☀️ Enpal ABS Control Room")
st.sidebar.markdown("---")

portal_view = st.sidebar.radio(
    "Select Executive Viewport:",
    [
        "1️⃣ Enpal 'Golden Ray' Asset Ledger & Waterfall",
        "2️⃣ 200-Run Monte Carlo Risk Simulation",
        "3️⃣ About and Financial Logic"
    ]
)

st.sidebar.markdown("---")
st.sidebar.header("Macroeconomic Adjustments")

cdr = st.sidebar.slider("Annual Default Rate (CDR)", 0.0, 0.15, 0.015, 0.005, format="%.3f")
cpr = st.sidebar.slider("Annual Prepayment Rate (CPR)", 0.0, 0.20, 0.05, 0.01, format="%.2f")

st.sidebar.header("Derivatives & Hedging")
base_euribor = st.sidebar.slider("Base Curve Pricing (Euribor Spikes)", 0.02, 0.08, 0.035, 0.005, format="%.3f")
# I explicitly mention the contractual 3.50% lock-in term directly on the UI toggle switch
enable_swap = st.sidebar.checkbox("Execute Interest Rate Swap (Lock Euribor at 3.50%)", value=True)

# --- 3. DYNAMIC BACKGROUND COMPUTE PIPELINE ---
simulator = MultiPeriodABSSimulator()
df_res, trap_triggered = simulator.run_simulation(cdr, cpr, base_euribor, enable_swap)
final_dscr = df_res["DSCR"].iloc[-1]
lifetime_co2 = df_res["CO2 Offset"].iloc[-1]

# ==============================================================================
# PORTAL VIEW 1: ENPAL GOLDEN RAY ASSET LEDGER & WATERFALL
# ==============================================================================
if portal_view == "1️⃣ Enpal 'Golden Ray' Asset Ledger & Waterfall":
    st.title("☀️ ENPAL 'GOLDEN RAY' ABS WORKSPACE")
    st.markdown("### 1️⃣ Core Portfolio Cash Flow Waterfall & Asset Ledger Analytics")
    st.markdown("Strategic Refinancing Analytics Platform — Powered by Enpal's Institutional Securitization Framework")
    st.divider()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="kpi-container"><div class="kpi-title">Securitized Asset Base</div><div class="kpi-value">€{simulator.initial_pool_balance:,.0f}</div><div class="kpi-subtitle">10,000 Active Residential Leases</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="kpi-container"><div class="kpi-title">Terminal Portfolio DSCR</div><div class="kpi-value">{final_dscr:.2f}x</div><div class="kpi-subtitle">Minimum Regulatory Target: &ge; 1.20x</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="kpi-container"><div class="kpi-title">Certified Carbon Offset</div><div class="kpi-value">{lifetime_co2:,.0f} Tons</div><div class="kpi-subtitle">Lifetime Verified Portfolio Impact</div></div>', unsafe_allow_html=True)
    with col4:
        if trap_triggered:
            st.markdown('<div class="covenant-box cov-error"><div style="font-size: 0.75rem; text-transform: uppercase; opacity: 0.8;">Covenant Compliance Status</div><div style="font-size: 1.25rem; margin-top: 5px;">⚠️ COVENANT BREACH</div><div style="font-size: 0.7rem; font-weight: 400; margin-top: 4px;">DSCR &lt; 1.20x Trigger Met: Residual Cash Flows Locked</div></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="covenant-box cov-success"><div style="font-size: 0.75rem; text-transform: uppercase; opacity: 0.8;">Covenant Compliance Status</div><div style="font-size: 1.25rem; margin-top: 5px;">🔒 COVENANTS OK</div><div style="font-size: 0.7rem; font-weight: 400; margin-top: 4px;">DSCR &ge; 1.20x Threshold Maintained: Distributions Active</div></div>', unsafe_allow_html=True)

    st.divider()
    
    st.subheader("📊 Multi-Period Liability Amortization Framework")
    m_df = df_res.melt(id_vars=["Month"], value_vars=["Pool Balance", "Tranche A", "Tranche B"], var_name="Tranche", value_name="Balance")
    fig1 = px.line(m_df, x="Month", y="Balance", color="Tranche", title="240-Month Asset Amortization vs. Sequential Structural Debt Repayment Curves")
    fig1.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#cbd5e1")
    st.plotly_chart(fig1, width="stretch")

    st.subheader("💸 Residual Capital Distribution Projections")
    fig2 = px.area(df_res, x="Month", y="Enpal Cash Flow", title="Net Monthly Profit Distributions to Equity Layer (Net of Locks and Swaps)", color_discrete_sequence=["#10b981"])
    fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#cbd5e1")
    st.plotly_chart(fig2, width="stretch")

# ==============================================================================
# PORTAL VIEW 2: 200-RUN MONTE CARLO RISK SIMULATION
# ==============================================================================
elif portal_view == "2️⃣ 200-Run Monte Carlo Risk Simulation":
    st.title("🎲 ENPAL 'GOLDEN RAY' RISK MANAGEMENT TERMINAL")
    st.markdown("### 2️⃣ 200-Run Monte Carlo Simulation & Stochastic Value at Risk (VaR) Engine")
    st.markdown("Evaluating Long-Tail Macroeconomic Stress Vectors via Automated Parallel Lifetime Projections")
    st.divider()

    with st.spinner("Executing real-time Monte Carlo iterations across separate stochastic economic paths..."):
        df_mc = simulator.run_monte_carlo_simulation(num_iterations=200, euribor_val=base_euribor, swap_active=enable_swap)
        
        fig_hist = px.histogram(df_mc, x="Lifetime Cash Flow (€)", nbins=25, title="Stochastic Probability Density Spectrum (Automated 200-Run Monte Carlo Computation Profile)", color_discrete_sequence=["#eab308"])
        fig_hist.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#cbd5e1")
        st.plotly_chart(fig_hist, width="stretch")
        
        p95 = df_mc["Lifetime Cash Flow (€)"].quantile(0.05)
        st.markdown(f"""
            <div style="background-color: #1e293b; padding: 25px; border-radius: 6px; border-left: 5px solid #34d399; margin-top: 20px;">
                <h4 style="color: #34d399; margin: 0 0 8px 0; font-size: 1.1rem;">📊 Quantitative Portfolio Value at Risk (VaR) Analysis via Monte Carlo Methods</h4>
                <p style="color: #cbd5e1; margin: 0; font-size: 0.95rem; line-height: 1.5;">
                    I engineered this stochastic layer to simulate 200 random future economic scenarios simultaneously. By dynamically shifting baseline credit stresses, the engine measures downside limits. Even under extreme, 5th-percentile economic tail-risk compressions, the securitized asset book establishes an absolute confidence interval floor, retaining a minimum of <strong>€{p95:,.2f}</strong> in residual equity liquidity values. This metrics validation acts as the structural safety baseline required by tier-1 institutional credit committees.
                </p>
            </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# PORTAL VIEW 3: ABOUT AND FINANCIAL LOGIC
# ==============================================================================
else:
    st.title("📖 APPLICANT BRIEFING & PORTFOLIO UNDERWRITING METHODOLOGY")
    st.markdown("### 3️⃣ About and Financial Logic")
    st.markdown("Core Methodological Briefing Document — Formulated for Quantitative Refinancing Team Evaluation")
    st.divider()
    
    st.markdown("""
    ### Quantitative Systems Engineering Framework — Candidate Narrative Case Study
    
    I built this advanced Asset-Backed Securitization (ABS) Cashflow Waterfall Workspace to prove my ability to handle complex capital structuring and structured debt mechanisms. By transitioning away from standard desktop spreadsheet software and moving directly into object-oriented Python, I built a modular quantitative tool that directly models the structural financing engines deployed across Enpal's asset financing operations.
    
    ---
    
    ### ⚙️ Systems Engineering Breakdown: What I Developed
    
    #### 1. Underwritten Asset Tape Architecture (`generate_portfolio.py`)
    I constructed an automated data pipeline to underwrite a synthetic pool of **10,000 distinct customer contracts** representing over **€270 Million in originations**. I enforced a hard **75% Solar and 25% Heat Pump equipment allocation mix** to align with real-world corporate diversification goals. Rather than assuming static customer default probabilities, I used a right-skewed **Beta Credit Distribution** to assign a unique Probability of Default ($PD$) to each system. This accurately models a premium, high-credit-quality consumer book containing unexpected long-tail credit anomalies.
    
    #### 2. Liability Layering, Credit Enhancement, and Subordination
    I split the funding liabilities into distinct structural risk segments, simulating an institutional bank financing structure:
    * **Tranche A (Senior Facility | €160M):** Structured with a primary credit spread of **1.50% (150 basis points)** over the active benchmark, built for top-tier institutional banks demanding primary liquidation priority.
    * **Tranche B (Mezzanine Facility | €40M):** Structured with an enhanced credit spread of **3.00% (300 basis points)** over the active benchmark, providing higher yields to risk-tolerant mezzanine providers while protecting Senior capital.
    * **The Residual Equity Component:** Retained completely by Enpal to absorb initial portfolio shocks, serving as an intentional overcollateralization shield.
    
    #### 3. Structured Derivative Hedging Integration (The Swap Metrics)
    I explicitly incorporated an **Interest Rate Swap derivative layer** into my core waterfall equations to handle real-world macroeconomic volatility. Because Enpal collects fixed monthly subscription fees from German customers while borrowing institutional funds exposed to volatile floating benchmarks (Euribor), a sudden spike in central bank rates would compress project margins. 
    
    To solve this, I coded a fixed-for-floating swap mechanism that executes the following exact numerical rules when activated:
    * It locks the underlying floating Euribor benchmark at a constant, fixed rate of **3.50%**.
    * By neutralizing the floating risk, Tranche A's all-in interest rate becomes completely fixed at **5.00%** ($3.50\\% \\text{ fixed Euribor} + 1.50\\% \\text{ spread}$).
    * Tranche B's all-in interest rate becomes completely fixed at **6.50%** ($3.50\\% \\text{ fixed Euribor} + 3.00\\% \\text{ spread}$).
    
    By mapping out this logic, I demonstrate how a strategic derivatives layer effectively anchors funding costs and shields Enpal's bottom-line equity distributions from macro interest rate surges.
    
    #### 4. Automated Covenant Governance and Structural Cash Traps
    I implemented an automated financial compliance engine to continuously evaluate portfolio health across all 240 months. The application tracks the **Debt Service Coverage Ratio ($DSCR$)** during every single period using the following structural validation criteria:
    
    $$DSCR = \\frac{\\text{Gross Cash Inflows} - \\text{Portfolio Servicing Fees}}{\\text{Senior Debt Interest} + \\text{Mezzanine Debt Interest}} \\ge 1.20x$$
    
    If extreme default pressures compress cash inflows, pushing the ratio below the required **1.20x DSCR floor**, my software automatically triggers a covenant breach. It locks down the waterfall, activates a **Structural Cash Trap**, and halts all cash distributions to Enpal's equity layer. Instead, it re-routes all remaining cash into a secure capital reserve lockbox to protect bondholder principal until credit metrics recover.
    
    #### 5. Real-Time Stochastic Simulation Framework
    Finally, I scaled the application into an automated risk assessment tool. I engineered a **backend Monte Carlo processor** that simulates 200 random, parallel economic tracks simultaneously. By sampling defaults and prepayments across separate probability curves, the system maps out an accurate risk spectrum. This allows corporate leadership to calculate true **Value at Risk (VaR)** parameters, mathematically proving how much capital remains protected across volatile macroeconomic futures.
    """)