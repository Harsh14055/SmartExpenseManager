from flask import Flask, render_template, redirect, url_for, request, flash,jsonify
from flask_login import LoginManager, login_required, current_user
from config import SQLALCHEMY_DATABASE_URI, SECRET_KEY
from models import db, Expense
from auth import auth_bp
from expense import expense_bp
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from collections import defaultdict
import joblib  # For loading the ML model
from auth import ExpenseForm  # Import expense form
import requests

# Initialize Flask app
app = Flask(__name__)

# Configure app
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = SECRET_KEY

# Initialize the database
db.init_app(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')  # Register auth blueprint
app.register_blueprint(expense_bp)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
@login_required
def dashboard():
    expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date.desc()).all()
    total_expenses = sum(exp.amount for exp in expenses)

    # Prepare Data for Pie Chart
    df = pd.DataFrame([(exp.category, exp.amount) for exp in expenses], columns=["Category", "Amount"])
    pie_chart = px.pie(df, names='Category', values='Amount', title='Expense Distribution')

    # Prepare Data for Bar Chart (Monthly Expenses)
    monthly_expenses = defaultdict(float)
    monthly_totals = defaultdict(float)  # Store total expenses per month

    for exp in expenses:
        month = exp.date.strftime('%B %Y')  # Format: "January 2025"
        monthly_expenses[exp.date.strftime('%Y-%m')] += exp.amount  # YYYY-MM format for Bar Chart
        monthly_totals[month] += exp.amount  # Month-Year format for Table

    # Sort bar chart data
    months_sorted = sorted(monthly_expenses.keys())  
    amounts_sorted = [monthly_expenses[m] for m in months_sorted]

    # Create Bar Chart
    bar_chart = go.Figure([go.Bar(x=months_sorted, y=amounts_sorted, marker_color='blue')])
    bar_chart.update_layout(title="Monthly Expenses", xaxis_title="Month", yaxis_title="Amount")

    return render_template(
        'dashboard.html',
        expenses=expenses,
        total_expenses=total_expenses,
        monthly_totals=dict(sorted(monthly_totals.items(), reverse=True)),  # Sort latest month first
        pie_chart_html=pie_chart.to_html(full_html=False),
        bar_chart_html=bar_chart.to_html(full_html=False)
    )
@app.route('/delete_account', methods=['GET', 'POST'])
@login_required
def delete_account():
    user = current_user

    # Delete all expenses linked to the user
    Expense.query.filter_by(user_id=user.id).delete()

    # Delete the user account
    db.session.delete(user)
    db.session.commit()

    flash("Your account has been deleted successfully.", "success")
    return redirect(url_for('auth.login'))

@app.route('/add_expense', methods=['GET', 'POST'])
@login_required
def add_expense():
    form = ExpenseForm()
    if form.validate_on_submit():
        new_expense = Expense(
            user_id=current_user.id,
            amount=form.amount.data,
            category=form.category.data,
            description=form.description.data,
            date=form.date.data or datetime.utcnow()
        )
        db.session.add(new_expense)
        db.session.commit()
        flash('Expense added successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_expense.html', form=form)

@app.route('/predict_category', methods=['POST'])
@login_required
def predict_category():
    model = joblib.load('category_predictor.pkl')  # Load ML model
    description = request.form.get('description', '')
    if description:
        category = model.predict([description])[0]  # Predict category
        return {'category': category}
    return {'category': 'Unknown'}
@app.route('/update_expense/<int:expense_id>', methods=['POST'])
def update_expense(expense_id):
    data = request.get_json()
    expense = Expense.query.get(expense_id)

    if expense and expense.user_id == current_user.id:
        expense.description = data.get("description", expense.description)
        db.session.commit()
        return jsonify({"success": True})

    return jsonify({"success": False}), 400
NEWS_API_KEY = "b863f8b5f9594cbb8b9ed71ae4b3aa07"  # Replace with your API key

def get_finance_news():
    url = f"https://newsapi.org/v2/top-headlines?category=business&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("articles", [])
    return []

@app.route('/finance-news')
@login_required
def finance_news():
    news_articles = get_finance_news()
    return render_template("finance_news.html", news_articles=news_articles)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)
