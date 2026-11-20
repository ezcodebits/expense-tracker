from pathlib import Path
from datetime import datetime
from models.expense import Expense
import json
import math

project_folder = Path(__file__).resolve().parent

data_folder = project_folder / "data"
data_folder.mkdir(exist_ok=True)

log_file = data_folder / "activity.log"
expenses_file = data_folder / "expenses.json"

# Write logs in activity.log file
def write_log(message):
    with open(log_file, "a", encoding="utf-8") as file:
        current_time = datetime.now()
        timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"[{timestamp}] {message}\n")

# Save Exepenses in file
def save_expenses(expenses):
    temp_file = expenses_file.with_suffix(".tmp")
    with open(temp_file, "w", encoding="utf-8") as file:
        json.dump(expenses, file, indent=4)
    temp_file.replace(expenses_file)

# Get all expenses from file
def load_expenses():
    try:
        with open(expenses_file, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("expenses.json contains invalid JSON.")
        return None

#-------------------Add Expense Start--------------------------
def add_expense():
    expenses = load_expenses()
    if expenses is None:
        return

    category = input("Enter category: ").strip()
    if not category:
        print("category can not be empty")
        return
    
    note = input("Enter note: ").strip()

    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("Please enter a valid amount")
        return

    if not math.isfinite(amount) or amount <= 0:
        print("Amount must be a finite number greater than zero.")
        return
    
    existing_ids = (item["id"] for item in expenses)
    next_id = max(existing_ids, default=0) + 1

    expense_date = datetime.now().strftime("%Y-%m-%d")

    new_expense = Expense(
        expense_id=next_id,
        date=expense_date,
        amount=amount,
        category=category,
        note=note
    )
    expenses.append(new_expense.to_dict())
    save_expenses(expenses)
    print("Expense added successfully")
    write_log(f"Expense added successfully: ID {next_id}")
#-------------------Add Expense End------------------------------

#-------------------View Expenses Start--------------------------
def view_expenses():
    loaded_expenses = load_expenses() 
    if loaded_expenses is None:
        return

    if not loaded_expenses:
        print("No expenses found.")
        return
    
    for item in loaded_expenses:
        print(f"ID: {item['id']} | Date: {item['date']} | Amount: {item['amount']:.2f} | Category: {item['category']} | Note: {item['note']}")
#-------------------View Expenses End-----------------------------

#-------------------Search Expense Start--------------------------
def search_with_category(category, expenses):
    matches = []
    for item in expenses:
        if item['category'].strip().casefold() == category:
            matches.append(item)
    return matches

def search_with_date(date, expenses):
    matches = []
    for item in expenses:
        if item['date'] == date:
            matches.append(item)
    return matches

def search_expenses():
    expenses = load_expenses()
    if expenses is None:
        return

    if not expenses:
        print("No expenses found.")
        return

    search_choice = input("Search by category (1) or date (2): ").strip()

    if search_choice == "1":
        category = input("Enter category: ").strip().casefold()
        matched_data = search_with_category(category, expenses)
    elif search_choice == "2":
        date_text = input("Enter date (YYYY-MM-DD): ").strip()
        try:
            parsed_date = datetime.strptime(date_text, "%Y-%m-%d")
        except ValueError:
            print("Invalid date. Use YYYY-MM-DD.")
            return

        search_date = parsed_date.strftime("%Y-%m-%d")
        if search_date != date_text:
            print("Use YYYY-MM-DD with a four-digit year and two-digit month and day.")
            return
        matched_data = search_with_date(search_date, expenses)
    else:
        print("Invalid search choice")
        return

    if not matched_data:
        print("No matching data found")
        return
    
    for item in matched_data:
        print(f"ID: {item['id']} | "
              f"Date: {item['date']} | "
              f"Amount: {item['amount']:.2f} | "
              f"Category: {item['category']} | "
              f"Note: {item['note']}")
#-------------------Search Expense End----------------------------

#-------------------Update Expense Start--------------------------   
def update_expense():
    expenses = load_expenses()
    if expenses is None:
        return

    if not expenses:
        print("No expenses found.")
        return
    
    try:
        expense_id = int(input("Enter expense ID: "))
    except ValueError:
        print("Please enter a valid numeric id")
        return

    selected_expense = None

    for item in expenses:
        if item['id'] == expense_id:
            selected_expense = item
            break

    if selected_expense is None:
        print("Expense not found")
        return

    print(f"Current expense — ID: {selected_expense['id']} | "
          f"Date: {selected_expense['date']} | "
          f"Amount: {selected_expense['amount']:.2f} | "
          f"Category: {selected_expense['category']} | "
          f"Note: {selected_expense['note']}")

    category_text = input("New category (Enter to keep Current): ").strip()
    note_text = input("New note (Enter to keep Current): ").strip()
    amount_text = input("New amount (Enter to keep Current): ").strip()

    if amount_text:
        try:
            new_amount = float(amount_text)
        except ValueError:
            print("Please enter valid amount")
            return

        if not math.isfinite(new_amount) or new_amount <= 0:
            print("Amount must be a finite number greater than zero.")
            return
    else:
        new_amount = selected_expense['amount']

    #if new is empty then keep previous
    new_category = category_text or selected_expense['category']
    new_note = note_text or selected_expense['note']

    selected_expense['category'] = new_category
    selected_expense['note'] = new_note
    selected_expense['amount'] = new_amount

    save_expenses(expenses)

    write_log(f"Expense updated: ID {expense_id}")
    print("Expense updated successfully.")
#-------------------Update Expense End----------------------------

#-------------------Delete Expense Start--------------------------
def delete_expense():
    expenses = load_expenses()
    if expenses is None:
        return

    if not expenses:
        print("No expenses found.")
        return

    try:
        expense_id = int(input("Enter expense ID: "))
    except ValueError:
        print("Please enter a valid numeric id")
        return

    selected_expense = None
    
    for item in expenses:
        if item['id'] == expense_id:
            selected_expense = item
            break

    if selected_expense is None:
        print("Expense not found")
        return

    print(f"Current expense — ID: {selected_expense['id']} | "
          f"Date: {selected_expense['date']} | "
          f"Amount: {selected_expense['amount']:.2f} | "
          f"Category: {selected_expense['category']} | "
          f"Note: {selected_expense['note']}")

    confirmation = input("Delete this expense? (y/n): ").strip().casefold()
    if confirmation != "y":
        print("Deletion cancelled!")
        return

    remaining_expenses = []
    for item in expenses:
        if item['id'] != expense_id:
            remaining_expenses.append(item)

    save_expenses(remaining_expenses)
    write_log(f"Expense deleted: ID {expense_id}")
    print("Expense deleted successfully.")
#-------------------Delete Expense End--------------------------
    
write_log("Application Started")

while True:
    print("\n1. Add expense")
    print("2. View expenses")
    print("3. Search expenses")
    print("4. Update expense")
    print("5. Delete expense")
    print("6. Exit")

    choice = input("Enter a choice: ").strip()

    if choice == "1":
        add_expense()
    elif choice == "2":
        view_expenses()
    elif choice == "3":
        search_expenses()
    elif choice == "4":
        update_expense()
    elif choice == "5":
        delete_expense()
    elif choice == "6":
        break
    else:
        print("Invalid choice")

write_log("Application Closed")

# with open(log_file, "r", encoding="utf-8") as file:
#     for number, line in enumerate(file, start=1):
#         clean_line = line.rstrip("\n")
#         print(f"{number}. {clean_line}")

# print(f"log file ready: {log_file}")