from models.expense import Expense

lunch = Expense(1, "2026-11-19", 250, "Food", "Lunch")
bus = Expense(2, "2026-11-19", 50, "Travel", "Bus fare")

print(lunch.amount)

print(lunch.to_dict())