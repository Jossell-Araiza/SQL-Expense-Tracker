from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For sessions/flash; use env var in production
load_dotenv()  # Load .env variables
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_id, username FROM users WHERE user_id = %s;", (user_id,))
    user_data = cur.fetchone()
    cur.close()
    conn.close()
    if user_data:
        return User(user_data[0], user_data[1])
    return None

# Database connection function
def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST')
    )
    return conn

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT user_id, password_hash FROM users WHERE username = %s;", (username,))
        user_data = cur.fetchone()
        cur.close()
        conn.close()
        if user_data and bcrypt.check_password_hash(user_data[1], password):
            user = User(user_data[0], username)
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid credentials')
    return render_template('login.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Protect dashboard
@app.route('/')
@login_required
def index():
    return render_template('index.html', user_id=current_user.id)

# API: Get monthly spending by category
@app.route('/api/spending/<int:user_id>', methods=['GET'])
@login_required
def get_monthly_spending(user_id):
    if user_id != int(current_user.id):
        return jsonify({'error': 'Unauthorized'}), 403
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
        SELECT 
            c.name AS category,
            EXTRACT(YEAR FROM e.expense_date) AS year,
            EXTRACT(MONTH FROM e.expense_date) AS month,
            SUM(e.amount) AS total_amount
        FROM expenses e
        JOIN categories c ON e.category_id = c.category_id
        WHERE e.user_id = %s
        GROUP BY c.name, EXTRACT(YEAR FROM e.expense_date), EXTRACT(MONTH FROM e.expense_date)
        ORDER BY year DESC, month DESC, total_amount DESC;
    """, (user_id,))
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

# API: Add a new expense
@app.route('/api/expenses', methods=['POST'])
@login_required
def add_expense():
    data = request.json
    if data['user_id'] != int(current_user.id):
        return jsonify({'error': 'Unauthorized'}), 403
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO expenses (user_id, category_id, amount, expense_date, description)
        VALUES (%s, %s, %s, %s, %s) RETURNING expense_id;
    """, (data['user_id'], data['category_id'], data['amount'], data['expense_date'], data['description']))
    expense_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'expense_id': expense_id}), 201

# API: Get recent expenses for a user
@app.route('/api/expenses/<int:user_id>', methods=['GET'])
@login_required
def get_recent_expenses(user_id):
    if user_id != int(current_user.id):
        return jsonify({'error': 'Unauthorized'}), 403
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
        SELECT 
            e.expense_id,
            c.name AS category,
            e.amount,
            e.expense_date,
            e.description
        FROM expenses e
        JOIN categories c ON e.category_id = c.category_id
        WHERE e.user_id = %s
        ORDER BY e.expense_date DESC
        LIMIT 10;
    """, (user_id,))
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

# Example: Edit expense
@app.route('/api/expenses/<int:expense_id>', methods=['PUT'])
@login_required
def update_expense(expense_id):
    data = request.json
    if data['user_id'] != int(current_user.id):
        return jsonify({'error': 'Unauthorized'}), 403
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE expenses
        SET amount = %s, description = %s, category_id = %s, expense_date = %s
        WHERE expense_id = %s AND user_id = %s
        RETURNING expense_id;
    """, (data['amount'], data['description'], data['category_id'], data['expense_date'], expense_id, data['user_id']))
    updated_id = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if updated_id:
        return jsonify({'message': 'Updated successfully'})
    return jsonify({'error': 'Not found'}), 404

# Example: Delete expense
@app.route('/api/expenses/<int:expense_id>', methods=['DELETE'])
@login_required
def delete_expense(expense_id):
    user_id = request.args.get('user_id', type=int)
    if user_id != int(current_user.id):
        return jsonify({'error': 'Unauthorized'}), 403
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM expenses WHERE expense_id = %s AND user_id = %s;", (expense_id, user_id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)