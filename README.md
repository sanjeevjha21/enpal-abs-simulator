# ☀️ Golden Ray ABS Terminal | Structured Finance & Securitisation Engine

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Live-FF4B4B.svg)](https://enpal-abs-simulator-hrct24zveysbcjzmajpupc.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Live Interactive Terminal:** [Launch the Golden Ray ABS Simulator](https://enpal-abs-simulator-hrct24zveysbcjzmajpupc.streamlit.app/)

## 📖 Executive Summary

This repository houses a production-grade **Structured Finance Analytics Platform** built entirely in Python. It was engineered to reverse-engineer and stress-test the structural mechanics of Enpal and M&G's landmark €300M public ABS transaction—the first securitization of residential solar and heat pump receivables in Europe.

By moving beyond static, legacy spreadsheet models, this terminal executes stochastic asset origination, dynamic tranche-level subordination, derivative hedging, and multi-period macroeconomic stress testing in real-time. 

---

## 🏗️ Quantitative Architecture

### 1. Synthetic Collateral Underwriting
* **The Engine:** Algorithmic origination of a **€270M+ synthetic loan tape** representing 10,000 individual residential lease contracts.
* **Asset Matrix:** Enforces a rigid diversification threshold (75% Solar / 25% Heat Pump).
* **Credit Risk Modeling:** Rejects uniform default assumptions by deploying a right-skewed **Beta Statistical Distribution**. This accurately models asymmetric Conditional Default Rates (CDR) to capture long-tail credit anomalies across the consumer pool.

### 2. Liability Layering & WACC Optimization
* **Sequential-Pay Waterfall:** Maps a complete 240-month sequential cash flow distribution lifecycle.
* **Subordination:** Tranches liabilities across a €160M Senior facility and a €40M Mezzanine facility to optimize the Weighted Average Cost of Capital (WACC). 
* **First-Loss Buffer:** Explicitly models how excess spread acts as the primary credit enhancement layer, distinguishing solar ABS structures from traditional RMBS.

### 3. ALM & Derivative Hedging
* **Duration Mismatch Neutralization:** Integrates a **Fixed-for-Floating Interest Rate Swap** matrix directly into the waterfall equations.
* **Execution:** Locks the underlying floating Euribor benchmark at 3.50%, completely immunizing residual equity distributions from macroeconomic rate volatility.

### 4. Covenant Governance & Structural Cash Traps
* **Programmatic Credit Enhancement:** Continuously monitors the underlying collateral performance via the Debt Service Coverage Ratio (DSCR):

$$DSCR = \frac{\text{Gross Cash Inflows} - \text{Portfolio Servicing Fees}}{\text{Senior Interest Owed} + \text{Mezzanine Interest Owed}}$$

* **Cash Trap Activation:** If extreme macroeconomic stress compresses the DSCR below the strict **1.20x threshold**, the architecture fires a covenant breach, instantly redirecting residual cash flows to ringfence and overcollateralize bondholder principal.

### 5. Stochastic VaR Engine (Monte Carlo)
* **Risk Quantification:** Replaces static Asset-Liability Management (ALM) forecasts with an automated **200-iteration Monte Carlo engine**.
* **Tail-Risk Analysis:** Stochastically varies Constant Prepayment Rate (CPR) and Conditional Default Rate (CDR) shocks to quantify an absolute 95th-percentile **Value at Risk (VaR)** downside boundary.

---

## ⚙️ Tech Stack & Execution Alpha

* **Backend Engine:** `Python`, `Pandas`, `NumPy`
* **Frontend UI:** `Streamlit`, `Plotly Express`
* **Computational Performance:** The object-oriented architecture processes 10,000 underlying assets and simulates 200 parallel 20-year structural lifecycles in **<1.5 seconds**, proving the scalability of code-native securitization structuring.

---

## 💻 Local Installation & Setup

To pull this simulator down to your local machine and run the backend engine:

1. **Clone the repository:**
```bash
   git clone [https://github.com/sanjeevjha21/enpal-abs-simulator.git](https://github.com/sanjeevjha21/enpal-abs-simulator.git)
   cd enpal-abs-simulator

```

2. **Install the required dependencies:**

```bash
   pip install -r requirements.txt

```

3. **Launch the Streamlit Terminal:**

```bash
   streamlit run abs_dashboard.py

```

---

## 📂 Repository Structure

* `generate_portfolio.py` — The algorithmic data factory that underwrites the foundational loan tape.
* `abs_multi_period_simulator.py` — The core object-oriented financial engine governing the waterfall, swap mechanics, and Monte Carlo logic.
* `abs_dashboard.py` — The Streamlit deployment file rendering the institutional UI and parameter toggles.
* `requirements.txt` — Cloud deployment dependency manifest.

---


