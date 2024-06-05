import csv
import os
from datetime import datetime

class BudgetTracker:
    def __init__(self, filename='budget_data.csv'):
        self.filename = filename
        self.transactions = []
        self.load_transactions()

    def load_transactions(self):
        if os.path.exists(self.filename):
            with open(self.filename, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                self.transactions = list(reader)
            for transaction in self.transactions:
                transaction['amount'] = float(transaction['amount'])

    def save_transaction(self, transaction):
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['type', 'amount', 'description', 'category', 'date'])
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(transaction)

    def add_income(self, amount, description):
        transaction = {
            'type': 'income',
            'amount': amount,
            'description': description,
            'category': 'income',
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.transactions.append(transaction)
        self.save_transaction(transaction)
        print(f"Income added: {amount} - {description}")

    def add_expense(self, amount, description, category):
        transaction = {
            'type': 'expense',
            'amount': amount,
            'description': description,
            'category': category,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.transactions.append(transaction)
        self.save_transaction(transaction)
        print(f"Expense added: {amount} - {description} - {category}")

    def show_summary(self):
        total_income = sum(item['amount'] for item in self.transactions if item['type'] == 'income')
        total_expense = sum(item['amount'] for item in self.transactions if item['type'] == 'expense')
        balance = total_income - total_expense

        print("\nBudget Summary")
        print("----------------")
        print(f"Total Income: ${total_income:.2f}")
        print(f"Total Expenses: ${total_expense:.2f}")
        print(f"Balance: ${balance:.2f}\n")

        if any(item['type'] == 'expense' for item in self.transactions):
            print("Expenses by Category:")
            categories = {}
            for transaction in self.transactions:
                if transaction['type'] == 'expense':
                    category = transaction['category']
                    if category not in categories:
                        categories[category] = 0
                    categories[category] += transaction['amount']

            for category, amount in categories.items():
                print(f"{category}: ${amount:.2f}")

def main():
    tracker = BudgetTracker()

    while True:
        print("\nBudget Tracker")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. Show Summary")
        print("4. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == '1':
            amount = float(input("Enter income amount: "))
            description = input("Enter income description: ")
            tracker.add_income(amount, description)
        
        elif choice == '2':
            amount = float(input("Enter expense amount: "))
            description = input("Enter expense description: ")
            category = input("Enter expense category: ")
            tracker.add_expense(amount, description, category)
        
        elif choice == '3':
            tracker.show_summary()
        
        elif choice == '4':
            print("Exiting Budget Tracker. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
    