from flask import Flask, render_template, redirect, url_for, flash, request
from models import db, User, Expense, Category
from forms import RegistrationForm, LoginForm, ExpenseForm
from flask_login import login_user, logout_user, login_required, current_user, LoginManager
from config import Config
from flask_migrate import Migrate
from utils.decorators import login_required
import io
import matplotlib.pyplot as plt
import base64

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def home():
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    return render_template('home.html', expenses=expenses)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    form = ExpenseForm()
    if form.validate_on_submit():
        expense = Expense(category=form.category.data, amount=form.amount.data, date=form.date.data, description=form.description.data, owner=current_user)
        db.session.add(expense)
        db.session.commit()
        flash('Expense added!', 'success')
        return redirect(url_for('home'))
    return render_template('expense_form.html', form=form)

@app.route('/summary')
@login_required
def summary():
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    
    # Calculate total amount and summarize expenses by category
    expense_summary = {}
    total_amount = 0
    for expense in expenses:
        total_amount += expense.amount
        if expense.category in expense_summary:
            expense_summary[expense.category] += expense.amount
        else:
            expense_summary[expense.category] = expense.amount

    # Generate pie chart
    categories = list(expense_summary.keys())
    amounts = list(expense_summary.values())

    fig, ax = plt.subplots()
    ax.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Save pie chart to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_b64 = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close(fig)

    return render_template('summary.html', total_amount=total_amount, expense_summary=expense_summary, img_data=img_b64)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
