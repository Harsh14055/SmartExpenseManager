from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Expense
from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, SubmitField,DateField
from wtforms.validators import InputRequired,DataRequired

expense_bp = Blueprint('expense', __name__)

# Expense Form
# class ExpenseForm(FlaskForm):
#     amount = FloatField('Amount', validators=[InputRequired()])
#     category = StringField('Category', validators=[InputRequired()])
#     description = StringField('Description')
#     submit = SubmitField('Add Expense')
class ExpenseForm(FlaskForm):
    amount = FloatField('Amount', validators=[InputRequired()])
    category = StringField('Category', validators=[InputRequired()])
    description = StringField('Description')
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Add Expense')

# Add Expense Route
# @expense_bp.route('/add_expense', methods=['GET', 'POST'])
# @login_required
# def add_expense():
#     form = ExpenseForm()
#     if form.validate_on_submit():
#         new_expense = Expense(
#             user_id=current_user.id,
#             amount=form.amount.data,
#             category=form.category.data,
#             description=form.description.data
#         )
#         db.session.add(new_expense)
#         db.session.commit()
#         flash('Expense added successfully!', 'success')
#         return redirect(url_for('dashboard'))
#     return render_template('add_expense.html', form=form)
@expense_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    form = ExpenseForm()
    
    if form.validate_on_submit():
        new_expense = Expense(
            user_id=current_user.id,
            amount=form.amount.data,
            category=form.category.data,
            description=form.description.data,
            date=form.date.data  # Store user-provided date
        )

        db.session.add(new_expense)
        db.session.commit()
        flash('Expense added successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_expense.html', form=form)
@expense_bp.route('/delete/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense(expense_id):
    expense = Expense.query.get(expense_id)

    if expense and expense.user_id == current_user.id:
        db.session.delete(expense)
        db.session.commit()
        flash('Expense deleted successfully!', 'success')
    else:
        flash('Error: Expense not found or unauthorized.', 'danger')

    return redirect(url_for('dashboard'))