Expense Tracker Dashboard
A full-stack web application for tracking personal expenses, with a focus on SQL data modeling and complex queries. Built using PostgreSQL for the database, Flask for the backend, and Bootstrap/HTML/JS for the frontend. Features include adding/editing/deleting expenses, monthly aggregations with charts, and user authentication.

Features
CRUD Operations: Add, edit, and delete expense entries (date, amount, category, description).
Dashboard Visuals: Monthly spending by category displayed in a table and pie chart (using Chart.js).
Recent Expenses: List of recent expenses with edit/delete buttons.
Authentication: User login/logout to ensure data privacy (each user sees only their expenses).
SQL Proficiency: Uses advanced queries like GROUP BY, JOIN, EXTRACT for date parts, and parameterized statements for security.
Tech Stack
Database: PostgreSQL (SQL for schema, queries, aggregations).
Backend: Python with Flask (API routes for CRUD, authentication with Flask-Login and Bcrypt).
Frontend: HTML/CSS/JavaScript with Bootstrap (responsive UI) and Chart.js (visualizations).
Other: python-dotenv for environment variables, psycopg2 for DB connection.
Prerequisites
Python 3.8+
PostgreSQL installed and running.
Basic knowledge of terminal commands.
Local Setup Instructions
Clone the Repository:
text

Collapse

Wrap

Copy
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
Set Up Virtual Environment:
text

Collapse

Wrap

Copy
python -m venv venv
.\venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On macOS/Linux
pip install -r requirements.txt
Set Up PostgreSQL Database:
Create a user and database (if not already done):
text

Collapse

Wrap

Copy
psql -U postgres
CREATE USER expense_user WITH PASSWORD 'your_password';
CREATE DATABASE expense_tracker;
GRANT ALL PRIVILEGES ON DATABASE expense_tracker TO expense_user;
\q
Run the SQL script to create tables and sample data:
text

Collapse

Wrap

Copy
psql -U expense_user -d expense_tracker -f expense_tracker.sql
(Enter the password when prompted. This drops existing tables if they exist and inserts sample users/expenses.)
Configure Environment Variables:
Create a .env file in the root:
text

Collapse

Wrap

Copy
DB_USER=expense_user
DB_PASSWORD=your_password
DB_NAME=expense_tracker
DB_HOST=localhost
Run the Application:
text

Collapse

Wrap

Copy
python app.py
Visit http://localhost:5000/ in your browser.
You'll be redirected to the login page.
Sample Login Credentials
Use these to log in (created in expense_tracker.sql):

Username: john_doe | Password: password1 (plain text—do not use the hashed value from the SQL script; the app hashes it during comparison).
Username: jane_smith | Password: password2
Note: Passwords are stored as bcrypt hashes in the database for security. The plain text passwords above are for demo purposes only. In a production app, users would register with their own credentials.

Usage
Log in with sample credentials.
Add expenses via the form—they appear in the recent table and update monthly totals/chart.
Edit/delete from the recent table (edit uses a simple prompt for new amount; customizable).
Logout via the button.
Screenshots
Login Page: [Add screenshot here]
Dashboard: [Add screenshot here, showing table and chart]
Deployment (Optional)
Deploy to Render.com for a live demo:

Push to GitHub.
On Render: New Web Service > Connect repo.
Settings: Runtime Python, Build pip install -r requirements.txt, Start gunicorn app:app.
Add env vars from .env.
Add PostgreSQL database, run SQL script via Render console.
Get the URL and test.
License
MIT License. See LICENSE file for details.