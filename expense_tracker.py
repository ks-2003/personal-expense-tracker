import csv
import os
from datetime import datetime

EXPENSES_FILE = 'expenses.csv'
FIELDNAMES = ['date', 'category', 'amount']

def load_expenses():
    expenses = []
    if os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert amount to float, keep other fields as strings
                row['amount'] = float(row['amount'])
                expenses.append(row)
    return expenses

def save_expenses(expenses):
    with open(EXPENSES_FILE, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        for exp in expenses:
            exp_copy = exp.copy()
            # Convert amount back to str for CSV
            exp_copy['amount'] = str(exp_copy['amount'])
            writer.writerow(exp_copy)

def add_expense(expenses):
    try:
        amount = float(input("Enter amount (e.g., 50.75): "))
    except ValueError:
        print("Invalid amount, please enter a number.")
        return
    category = input("Enter category (e.g., Food, Transport): ").strip()
    # Use today's date by default
    date_str = input("Enter date (YYYY-MM-DD) [leave blank for today]: ").strip()
    if date_str == '':
        date_str = datetime.today().strftime('%Y-%m-%d')
    else:
        # Validate date format
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            print("Invalid date format! Use YYYY-MM-DD.")
            return
    expenses.append({'date': date_str, 'category': category, 'amount': amount})
    save_expenses(expenses)
    print("Expense added successfully.")

def add_expenses_for_category(expenses):
    category = input("Enter category (e.g., Food, Transport): ").strip()
    while True:
        amount_input = input(f"Enter amount for {category} (or leave blank to stop): ").strip()
        if amount_input == '':
            break
        try:
            amount = float(amount_input)
        except ValueError:
            print("Invalid amount, please enter a number or leave blank to stop.")
            continue
        date_str = input("Enter date (YYYY-MM-DD) [leave blank for today]: ").strip()
        if date_str == '':
            date_str = datetime.today().strftime('%Y-%m-%d')
        else:
            try:
                datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                print("Invalid date format! Use YYYY-MM-DD. Skipping this entry.")
                continue
        expenses.append({'date': date_str, 'category': category, 'amount': amount})
        print(f"Added ${amount:.2f} to {category}.")
    save_expenses(expenses)
    print("Finished adding expenses for this category.")

def summary_by_category(expenses):
    category = input("Enter category to summarize: ").strip()
    total = sum(exp['amount'] for exp in expenses if exp['category'].lower() == category.lower())
    print(f"Total spent on {category}: ${total:.2f}")

def overall_summary(expenses):
    total = sum(exp['amount'] for exp in expenses)
    print(f"Total expenses: ${total:.2f}")

def spending_over_time(expenses):
    print("1. Daily \n2. Monthly")
    choice = input("Choose (1/2): ").strip()
    summary = {}
    if choice == '1':
        for exp in expenses:
            key = exp['date']
            summary[key] = summary.get(key, 0) + exp['amount']
    elif choice == '2':
        for exp in expenses:
            key = exp['date'][:7]  # e.g., "2024-08"
            summary[key] = summary.get(key, 0) + exp['amount']
    else:
        print("Invalid choice.")
        return
    for key in sorted(summary.keys()):
        print(f"{key}: ${summary[key]:.2f}")

def show_menu():
    print("\n***** Personal Expense Tracker *****")
    print("1. Add Expense (One at a Time)")
    print("2. Add Multiple Expenses for a Category")
    print("3. View Category Summary")
    print("4. View Total Summary")
    print("5. View Spending Over Time")
    print("6. Exit")

def main():
    expenses = load_expenses()
    while True:
        show_menu()
        choice = input("Select an option (1-6): ").strip()
        if choice == '1':
            add_expense(expenses)
        elif choice == '2':
            add_expenses_for_category(expenses)
        elif choice == '3':
            summary_by_category(expenses)
        elif choice == '4':
            overall_summary(expenses)
        elif choice == '5':
            spending_over_time(expenses)
        elif choice == '6':
            print("Goodbye! Data saved.")
            break
        else:
            print("Invalid choice. Please select a number from 1 to 6.")

if __name__ == "__main__":
    main()
