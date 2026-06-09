import pandas as pd


class MultiPeriodABSSimulator:

    def __init__(self, portfolio_path="enpal_simulated_portfolio.csv"):
        # Load our core portfolio data
        self.df = pd.read_csv(portfolio_path)

        # Calculate starting totals from our asset pool
        self.initial_pool_balance = self.df["asset_value"].sum()
        self.total_monthly_scheduled_payment = self.df["monthly_payment"].sum()

        # Initialize the Debt Tranches
        self.tranche_a_principal = 160000000.00
        self.tranche_a_rate = 0.045

        self.tranche_b_principal = 40000000.00
        self.tranche_b_rate = 0.065

        # Operational Fee
        self.annual_servicing_rate = 0.005

    def run_simulation(self, annualized_default_rate=0.015, annualized_prepayment_rate=0.05) -> pd.DataFrame:
        # Convert annualized financial assumptions into monthly rates
        monthly_default_rate = annualized_default_rate / 12
        monthly_prepayment_rate = annualized_prepayment_rate / 12
        monthly_servicing_rate = self.annual_servicing_rate / 12

        # Tracks our active pool balances over time
        current_pool_balance = self.initial_pool_balance
        t_a_balance = self.tranche_a_principal
        t_b_balance = self.tranche_b_principal

        history = []

        # Loop through a 20-year horizon (Month 1 to Month 240)
        for month in range(1, 241):
            if current_pool_balance <= 0:
                break

            # 1. Account for portfolio shrinkage due to past defaults and prepayments
            defaults_this_month = current_pool_balance * monthly_default_rate
            prepayments_this_month = (
                current_pool_balance * monthly_prepayment_rate
            )

            # Pro-rate the incoming monthly collections based on remaining assets
            pool_factor = current_pool_balance / self.initial_pool_balance
            gross_cash_collected = (
                self.total_monthly_scheduled_payment * pool_factor
            ) + prepayments_this_month

            # Reduce the asset pool size for the next iteration
            current_pool_balance -= (
                defaults_this_month + prepayments_this_month
            )

            # 2. RUN THE WATERFALL
            # Step A: Pay Servicing Fee
            servicing_fee = current_pool_balance * monthly_servicing_rate
            available_cash = max(0.0, gross_cash_collected - servicing_fee)

            # Step B: Pay Tranche A Interest
            t_a_interest = t_a_balance * (self.tranche_a_rate / 12)
            available_cash -= t_a_interest

            # Step C: Pay Tranche B Interest
            t_b_interest = t_b_balance * (self.tranche_b_rate / 12)
            available_cash -= t_b_interest

            # Step D: Sequential Principal Amortization (The extra cash pays down debt)
            principal_allocated_to_a = 0.0
            principal_allocated_to_b = 0.0

            if t_a_balance > 0:
                principal_allocated_to_a = min(available_cash, t_a_balance)
                t_a_balance -= principal_allocated_to_a
                available_cash -= principal_allocated_to_a

            if t_a_balance == 0 and t_b_balance > 0:
                principal_allocated_to_b = min(available_cash, t_b_balance)
                t_b_balance -= principal_allocated_to_b
                available_cash -= principal_allocated_to_b

            # Step E: Enpal Residual Equity Cash
            enpal_residual = available_cash

            # Log this month's financial metrics
            history.append(
                {
                    "Month": month,
                    "Remaining Pool Balance": round(current_pool_balance, 2),
                    "Tranche A Balance": round(t_a_balance, 2),
                    "Tranche B Balance": round(t_b_balance, 2),
                    "Gross Cash Collected": round(gross_cash_collected, 2),
                    "Enpal Cash Flow": round(enpal_residual, 2),
                }
            )

        return pd.DataFrame(history)


if __name__ == "__main__":
    simulator = MultiPeriodABSSimulator()

    # Run simulation with 1.5% annual defaults and 5% early prepayments
    print("Executing 240-Month Macroeconomic Simulation...")
    simulation_results_df = simulator.run_simulation(
        annualized_default_rate=0.015, annualized_prepayment_rate=0.05
    )

    # Save the output timeline to a CSV report
    output_report_name = "abs_20_year_simulation_report.csv"
    simulation_results_df.to_csv(output_report_name, index=False)

    print("\n--- 20-Year Lifecycle Simulation Completed! ---")
    print(f"Full report saved as: {output_report_name}")
    print("\nTimeline Milestones Snapshot:")
    print(simulation_results_df.iloc[[0, 60, 120, 180, 239]].to_string(index=False))