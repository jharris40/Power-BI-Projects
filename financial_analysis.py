import pandas as pd
import matplotlib.pyplot as plt
import os

# Function to collect financial data
def collect_data():
    data = {}
    print("Enter the following data for financial analysis:")

    data['project_name'] = input("Project/Company Name: ")
    data['revenue'] = float(input("Total Revenue ($): "))
    data['cost_of_goods_sold'] = float(input("Cost of Goods Sold (COGS) ($): "))
    data['operating_expenses'] = float(input("Operating Expenses ($): "))
    data['interest_expenses'] = float(input("Interest Expenses ($): "))
    data['taxes'] = float(input("Taxes ($): "))
    data['initial_investment'] = float(input("Initial Investment ($): "))
    data['units_sold'] = int(input("Total Units Sold: "))
    data['price_per_unit'] = float(input("Price per Unit ($): "))
    data['fixed_costs'] = float(input("Fixed Costs ($): "))
    data['variable_cost_per_unit'] = float(input("Variable Cost per Unit ($): "))

    return data

# Function to perform financial analysis
def financial_analysis(data):
    metrics = {}
    metrics['gross_profit'] = data['revenue'] - data['cost_of_goods_sold']
    metrics['operating_profit'] = metrics['gross_profit'] - data['operating_expenses']
    metrics['net_profit'] = metrics['operating_profit'] - data['interest_expenses'] - data['taxes']
    metrics['profit_margin'] = (metrics['net_profit'] / data['revenue']) * 100
    metrics['roi'] = (metrics['net_profit'] / data['initial_investment']) * 100
    metrics['ebitda'] = metrics['gross_profit'] - data['operating_expenses']
    metrics['contribution_margin'] = data['price_per_unit'] - data['variable_cost_per_unit']
    metrics['break_even_point'] = data['fixed_costs'] / metrics['contribution_margin']

    return metrics

# Function to save data to a CSV file
def save_data(data, metrics, filename="financial_data.csv"):
    df = pd.DataFrame([data | metrics])
    if os.path.exists(filename):
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        df.to_csv(filename, index=False)
    print(f"Data saved to {filename}.")

# Function to load data from a CSV file
def load_data(filename="financial_data.csv"):
    if os.path.exists(filename):
        return pd.read_csv(filename)
    else:
        print(f"No data file found at {filename}.")
        return None

# Function to display results
def display_results(data, metrics):
    print("\n--- Financial Analysis Report ---")
    print(f"Project/Company Name: {data['project_name']}")
    print(f"Gross Profit: ${metrics['gross_profit']:.2f}")
    print(f"Operating Profit: ${metrics['operating_profit']:.2f}")
    print(f"Net Profit: ${metrics['net_profit']:.2f}")
    print(f"Profit Margin: {metrics['profit_margin']:.2f}%")
    print(f"Return on Investment (ROI): {metrics['roi']:.2f}%")
    print(f"EBITDA: ${metrics['ebitda']:.2f}")
    print(f"Contribution Margin: ${metrics['contribution_margin']:.2f} per unit")
    print(f"Break-Even Point: {metrics['break_even_point']:.2f} units")

# Function to plot financial data
def plot_financials(data, metrics):
    categories = ['Revenue', 'COGS', 'Operating Expenses', 'Net Profit']
    values = [
        data['revenue'], 
        data['cost_of_goods_sold'], 
        data['operating_expenses'], 
        metrics['net_profit']
    ]
    
    plt.figure(figsize=(8, 6))
    plt.bar(categories, values, color=['blue', 'red', 'orange', 'green'])
    plt.title("Financial Overview")
    plt.ylabel("Amount ($)")
    plt.show()

# Main function to run the program
def main():
    print("Welcome to the Financial Analysis Software!")
    while True:
        print("\nOptions:")
        print("1. Enter new data")
        print("2. Load data from file")
        print("3. Exit")
        choice = input("Choose an option (1/2/3): ")

        if choice == '1':
            data = collect_data()
            metrics = financial_analysis(data)
            display_results(data, metrics)
            save_data(data, metrics)
            plot_financials(data, metrics)
        elif choice == '2':
            df = load_data()
            if df is not None:
                print("\nLoaded Data:")
                print(df)
        elif choice == '3':
            print("Exiting the software. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the program
if __name__ == "__main__":
    main()
