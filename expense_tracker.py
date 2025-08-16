import csv
import os
from datetime import datetime
import pandas as pd

FILENAME = "expenses.csv"

# --------------------- Add Transaction ---------------------
def add_transaction():
    date = input("Enter date (YYYY-MM-DD) [default: today]: ") or datetime.today().strftime('%Y-%m-%d')
    description = input("Description: ")
    category = input("Category (Food, Rent, etc.): ")
    try:
        amount = float(input("Amount (+ for income, - for expense): "))
    except ValueError:
        print("❌ Invalid amount.")
        return

    with open(FILENAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, description, category, amount])
    print("✅ Transaction added!")

# --------------------- View Transactions ---------------------
def view_transactions():
    if not os.path.exists(FILENAME):
        print("No transactions found. Start by adding one.")
        return

    print("\n📄 All Transactions:\n")
    total = 0
    print("Date\t\tDescription\tCategory\tAmount")
    print("-" * 50)
    with open(FILENAME, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}")
            total += float(row[3])
    print("-" * 50)
    print(f"💰 Current Balance: ₹{total:,.2f}")

# --------------------- Monthly Summary ---------------------
def monthly_summary():
    if not os.path.exists(FILENAME):
        print("No transactions found. Start by adding one.")
        return

    try:
        df = pd.read_csv(FILENAME, names=["Date", "Description", "Category", "Amount"])
        df['Date'] = pd.to_datetime(df['Date'])
        df['Month'] = df['Date'].dt.to_period('M')

        grouped = df.groupby('Month')['Amount'].sum().reset_index()
        incomes = df[df['Amount'] > 0].groupby('Month')['Amount'].sum()
        expenses = df[df['Amount'] < 0].groupby('Month')['Amount'].sum()

        print("\n📅 Summary by Month:\n")
        for month in grouped['Month']:
            income = incomes.get(month, 0)
            expense = expenses.get(month, 0)
            balance = income + expense
            print(f"{month.strftime('%B %Y')}")
            print(f" - Total Income:  ₹{income:,.2f}")
            print(f" - Total Expense: ₹{-expense:,.2f}")
            print(f" - Balance:       ₹{balance:,.2f}\n")

    except Exception as e:
        print(f"❌ Error: {e}")

# --------------------- Main Menu ---------------------
def main():
    while True:
        print("\n==== Personal Expense Tracker ====")
        print("1. Add Transaction")
        print("2. View All Transactions")
        print("3. View Monthly Summary")
        print("4. Exit")
        choice = input("Choose an option (1-4): ")

        if choice == '1':
            add_transaction()
        elif choice == '2':
            view_transactions()
        elif choice == '3':
            monthly_summary()
        elif choice == '4':
            print("👋 Exiting. Have a great day!")
            break
        else:
            print("❌ Invalid option. Try again.")

if __name__ == "__main__":
    main()
