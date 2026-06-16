import pandas as pd
import numpy as np

class MultiPeriodABSSimulator:

    def __init__(self, portfolio_path="enpal_simulated_portfolio.csv"):
        # I ingest the underlying historical loan tape asset rows
        self.df = pd.read_csv(portfolio_path)

        # I aggregate the baseline cash flows generated across the portfolio
        self.initial_pool_balance = self.df["asset_value"].sum()
        self.total_monthly_scheduled_payment = self.df["monthly_payment"].sum()

        # I structure the initial debt boundaries for Senior and Mezzanine layers
        self.tranche_a_principal = 160000000.00
        self.tranche_b_principal = 40000000.00
        self.annual_servicing_rate = 0.005

    def run_simulation(self, cdr_val, cpr_val, euribor_val, swap_active) -> tuple[pd.DataFrame, bool]:
        # I break down annual assumptions into compounding monthly calculation periods
        m_default = cdr_val / 12
        m_prepay = cpr_val / 12
        monthly_servicing_rate = self.annual_servicing_rate / 12
        
        # INTEREST RATE DERIVATIVE LOGIC
        # If I execute the swap, I lock the underlying floating Euribor benchmark at a fixed 3.50%.
        # Otherwise, the model exposes the portfolio to the volatile floating Euribor market curve.
        effective_euribor = 0.035 if swap_active else euribor_val
        
        # I apply the fixed contractual institutional spreads over the active benchmark:
        # Tranche A Spread = 1.50% (150 bps) | Tranche B Spread = 3.00% (300 bps)
        t_a_rate = effective_euribor + 0.015
        t_b_rate = effective_euribor + 0.030
        
        current_pool = self.initial_pool_balance
        t_a_bal = self.tranche_a_principal
        t_b_bal = self.tranche_b_principal
        
        history = []
        cumulative_co2 = 0.0
        cash_trap_active = False

        # I process the 240-month waterfall loop sequentially
        for month in range(1, 241):
            if current_pool <= 0: 
                break
            
            # I track ongoing portfolio decay caused by defaults and early customer payoffs
            def_amt = current_pool * m_default
            prep_amt = current_pool * m_prepay
            pool_factor = current_pool / self.initial_pool_balance
            
            # I compile gross cash receipts arriving from the active asset base
            gross_cash = (self.total_monthly_scheduled_payment * pool_factor) + prep_amt
            current_pool -= (def_amt + prep_amt)
            
            # I track verified carbon offsets dynamically (assuming 3.5 metric tons offset per household annually)
            active_systems = 10000 * pool_factor
            monthly_co2_offset = (active_systems * 3.5) / 12
            cumulative_co2 += monthly_co2_offset
            
            # WATERFALL TIER 1: I subtract operational portfolio servicing asset fees
            servicing_fee = current_pool * monthly_servicing_rate
            available_cash = max(0.0, gross_cash - servicing_fee)
            
            # WATERFALL TIER 2: I track current debt interest service demands
            t_a_interest = t_a_bal * (t_a_rate / 12)
            t_b_interest = t_b_bal * (t_b_rate / 12)
            total_debt_service = t_a_interest + t_b_interest
            
            # I evaluate covenant health via the Debt Service Coverage Ratio (DSCR)
            dscr = (available_cash / total_debt_service) if total_debt_service > 0 else 3.0
            
            # If the DSCR breaches the required 1.20x threshold boundary, I force lockbox protection
            if dscr < 1.20:
                cash_trap_active = True
                
            available_cash -= min(available_cash, t_a_interest)
            available_cash -= min(available_cash, t_b_interest)
            
            # WATERFALL TIER 3: I route cash flows to pay down principal debt balances
            p_a = min(available_cash, t_a_bal)
            t_a_bal -= p_a
            available_cash -= p_a
            
            p_b = min(available_cash, t_b_bal)
            t_b_bal -= p_b
            available_cash -= p_b
            
            # WATERFALL TIER 4: I distribute equity cash flows back to Enpal
            enpal_payout = 0.0 if cash_trap_active else available_cash
            
            history.append({
                "Month": month, "Pool Balance": current_pool,
                "Tranche A": t_a_bal, "Tranche B": t_b_bal,
                "Enpal Cash Flow": enpal_payout, "DSCR": dscr,
                "CO2 Offset": cumulative_co2, "Cash Trap Triggered": cash_trap_active
            })
            
        return pd.DataFrame(history), cash_trap_active

    def run_monte_carlo_simulation(self, num_iterations=200, euribor_val=0.035, swap_active=True) -> pd.DataFrame:
        # I establish a stochastic testing track to assess macro-risk distributions
        sim_profits = []
        
        for sim in range(num_iterations):
            # I pull randomized macro shock waves using a credit-skewed log-normal distribution curve
            random_cdr = np.random.lognormal(mean=np.log(0.018), sigma=0.35)
            random_cpr = np.random.normal(loc=0.05, scale=0.008)
            
            df_sim, _ = self.run_simulation(
                cdr_val=np.clip(random_cdr, 0, 0.20), 
                cpr_val=np.clip(random_cpr, 0, 0.25), 
                euribor_val=euribor_val, 
                swap_active=swap_active
            )
            sim_profits.append(df_sim["Enpal Cash Flow"].sum())
            
        return pd.DataFrame({"Lifetime Cash Flow (€)": sim_profits})
