import numpy as np
import pandas as pd


class EnpalPortfolioGenerator:

    def __init__(self, num_contracts=10000, seed=42):
        self.num_contracts = num_contracts
        # Setting a random seed ensures we get the exact same data every time we run it
        self.seed = seed
        np.random.seed(seed)

    def generate(self) -> pd.DataFrame:
        print(f"Generating {self.num_contracts} synthetic lease contracts...")

        # 1. Randomly assign asset type (75% Solar, 25% Heat Pump)
        asset_types = np.random.choice(
            ["Solar", "Heat Pump"],
            size=self.num_contracts,
            p=[0.75, 0.25],
        )

        # 2. Set up empty lists to store our contract data
        portfolio_data = []

        for i, asset in enumerate(asset_types):
            contract_id = f"ENP-{2026}-{i+1:05d}"

            if asset == "Solar":
                # Average asset size around €25,000 with minor random variations
                asset_value = round(np.random.normal(25000, 2000), 2)
                interest_rate = round(np.random.normal(0.058, 0.005), 4)
                monthly_payment = round(np.random.normal(180, 15), 2)
            else:
                # Average heat pump asset size around €35,000
                asset_value = round(np.random.normal(35000, 3000), 2)
                interest_rate = round(np.random.normal(0.065, 0.004), 4)
                monthly_payment = round(np.random.normal(260, 20), 2)

            # Generate a baseline Probability of Default (PD) between 0.5% and 8%
            prob_of_default = round(np.random.beta(2, 20) * 0.3, 4)

            # Build the individual contract row
            contract = {
                "contract_id": contract_id,
                "asset_type": asset,
                "asset_value": asset_value,
                "interest_rate": interest_rate,
                "monthly_payment": monthly_payment,
                "remaining_term_months": 240,  # 20-year fixed standard lease
                "probability_of_default": prob_of_default,
            }
            portfolio_data.append(contract)

        # Convert the array of contracts into a clean Pandas DataFrame table
        df = pd.DataFrame(portfolio_data)
        return df


if __name__ == "__main__":
    # Initialize the generator
    generator = EnpalPortfolioGenerator(num_contracts=10000)
    portfolio_df = generator.generate()

    # Save the generated portfolio as a clean CSV database file
    output_filename = "enpal_simulated_portfolio.csv"
    portfolio_df.to_csv(output_filename, index=False)

    print("\n--- Portfolio Successfully Generated! ---")
    print(f"File saved as: {output_filename}")
    print("\nPortfolio Quick Summary Statistics:")
    print(
        portfolio_df.groupby("asset_type")[["asset_value", "monthly_payment"]]
        .mean()
        .round(2)
    )