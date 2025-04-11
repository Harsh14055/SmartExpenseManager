from datetime import datetime
from models import db, Expense  # Adjust import based on your project structure

def calculate_last_month_expense():
    last_month = datetime.now().month - 1
    total = db.session.query(db.func.sum(Expense.amount)).filter(db.extract('month', Expense.date) == last_month).scalar()
    return total if total else 0

def calculate_today_expense():
    today = datetime.now().date()
    total = db.session.query(db.func.sum(Expense.amount)).filter(Expense.date == today).scalar()
    return total if total else 0

def get_biggest_expense():
    biggest = db.session.query(Expense).order_by(Expense.amount.desc()).first()
    return {"category": biggest.category, "amount": biggest.amount} if biggest else {"category": "None", "amount": 0}
