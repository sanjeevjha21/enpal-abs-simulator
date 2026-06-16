import pandas as pd


class ABSWaterfallEngine:

    def __init__(self, portfolio_path="enpal_simulated_portfolio.csv"):
        # Load the CSV data we generated in Step 2
        self.df = pd.read_csv(portfolio_path)

        # Define the structure of our debt (The Tranches)
        # We borrowed €200M total against our €272M+ portfolio
        self.tranche_a_principal = 160000000.00  # Senior Debt (Low Risk)
        self.tranche_a_rate = 0.045  # 4.5% Annual Interest

        self.tranche_b_principal = 40000000.00  # Mezzanine Debt (Medium Risk)
        self.tranche_b_rate = 0.065  # 6.5% Annual Interest

        # Operational Fees
        self.monthly_servicing_fee_rate = (
            0.005 / 12
        )  # 0.5% annually for maintaining systems

    def simulate_month_one(
        self, default_rate_override=None
    ) -> dict[str, float]:
        print("Running Month 1 Cashflow Waterfall Simulation...")

        # 1. Calculate Gross Cash Inflow from active customers
        # If a customer's individual probability of default is higher than a threshold,
        # or if we override it globally, they miss their payment this month.
        total_gross_inflow = 0.0

        for _, row in self.df.iterrows():
            # Check if customer defaults this month
            is_defaulted = False
            if default_rate_override is not None:
                # Simple global probabilistic check
                if pd.Series(
                    [True, False]
                ).sample(weights=[default_rate_override, 1 - default_rate_override]).values[0]:
                    is_defaulted = True
            else:
                # Use the unique customer risk profile we generated
                if pd.Series(
                    [True, False]
                ).sample(weights=[row["probability_of_default"], 1 - row["probability_of_default"]]).values[0]:
                    is_defaulted = True

            if not is_defaulted:
                total_gross_inflow += row["monthly_payment"]

        # Total portfolio value for asset calculations
        total_portfolio_value = self.df["asset_value"].sum()

        # 2. WATERFALL STEP 1: Pay Servicing Fees (Enpal's operations team gets paid first)
        servicing_fee = total_portfolio_value * self.monthly_servicing_fee_rate
        available_cash = total_gross_inflow - servicing_fee

        # 3. WATERFALL STEP 2: Pay Tranche A (Senior Investor Interest)
        tranche_a_interest = (
            self.tranche_a_principal * (self.tranche_a_rate / 12)
        )
        tranche_a_paid = min(available_cash, tranche_a_interest)
        available_cash -= tranche_a_paid

        # 4. WATERFALL STEP 3: Pay Tranche B (Mezzanine Investor Interest)
        tranche_b_interest = (
            self.tranche_b_principal * (self.tranche_b_rate / 12)
        )
        tranche_b_paid = min(available_cash, tranche_b_interest)
        available_cash -= tranche_b_paid

        # 5. WATERFALL STEP 4: Enpal's Residual Profit (Whatever is left over)
        enpal_residual_cash = max(0.0, available_cash)

        # Return the results as a dictionary
        return {
            "Gross Inflow": round(total_gross_inflow, 2),
            "Servicing Fees Paid": round(servicing_fee, 2),
            "Tranche A Interest Paid": round(tranche_a_paid, 2),
            "Tranche B Interest Paid": round(tranche_b_paid, 2),
            "Enpal Residual Cash": round(enpal_residual_cash, 2),
        }


if __name__ == "__main__":
    engine = ABSWaterfallEngine()

    # Scenario A: Normal Business Operations
    print("\n--- SCENARIO A: Normal Market Conditions ---")
    normal_results = engine.simulate_month_one()
    for key, val in normal_results.items():
        print(f"{key}: €{val:,.2f}")

    # Scenario B: Severe Economic Stress (e.g., 12% default rate)
    print("\n--- SCENARIO B: Severe Macroeconomic Stress (12% Defaults) ---")
    stress_results = engine.simulate_month_one(default_rate_override=0.12)
    for key, val in stress_results.items():
        print(f"{key}: €{val:,.2f}")