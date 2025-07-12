# Expense Tracker Dashboard

A full-stack web application for managing personal expenses, featuring user authentication, data visualizations, and secure PostgreSQL integration. Built with Flask, PostgreSQL, and Bootstrap, this project demonstrates practical use of SQL aggregations, backend routing, and frontend chart rendering.

## 🔗 Live Demo
👉 [View Deployed App on Render](https://your-render-url.onrender.com)  
*(Login credentials below)*

## Tech Stack
- **Database**: PostgreSQL (schema design, secure parameterized queries, aggregations)
- **Backend**: Python, Flask, Flask-Login, Bcrypt
- **Frontend**: HTML, CSS, JavaScript, Bootstrap, Chart.js
- **Other Tools**: python-dotenv, psycopg2

## Features
- **CRUD Operations**: Add, edit, and delete expenses (date, amount, category, description)
- **Dashboard Visuals**: Pie chart and table showing monthly spend by category (via Chart.js)
- **Recent Expenses**: View latest entries with inline edit/delete actions
- **Authentication**: Secure login/logout (users only see their own expenses)
- **SQL Proficiency**: Advanced queries using `JOIN`, `GROUP BY`, `EXTRACT`, and parameterized statements

## Prerequisites (for local setup)
- Python 3.8+
- PostgreSQL installed and running
- Basic familiarity with terminal/command line

## Local Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/expense-tracker-dashboard.git
cd expense-tracker-dashboard
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
.\venv\Scripts\activate  # On Windows
# OR
source venv/bin/activate  # On macOS/Linux

pip install -r requirements.txt
```

### 3. Set Up PostgreSQL Database
```sql
psql -U postgres
CREATE USER expense_user WITH PASSWORD 'your_password';
CREATE DATABASE expense_tracker;
GRANT ALL PRIVILEGES ON DATABASE expense_tracker TO expense_user;
\q
```

Run the SQL script to create tables and insert sample data:
```bash
psql -U expense_user -d expense_tracker -f expense_tracker.sql
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:
```env
DB_USER=expense_user
DB_PASSWORD=your_password
DB_NAME=expense_tracker
DB_HOST=localhost
```

### 5. Run the Application
```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

## Sample Login Credentials

These accounts are preloaded via the SQL seed file:

| Username    | Password   |
|-------------|------------|
| john_doe    | password1  |
| jane_smith  | password2  |

> 🔒 Passwords are hashed using Bcrypt. These demo credentials are for testing only.

## Usage
- Log in with a sample user
- Add new expenses via the input form
- Review entries in the recent transactions table
- View monthly totals and breakdown by category (chart)
- Edit or delete expenses inline
- Logout to end session

## Screenshots
> *(Replace these with actual image links if stored in the repo)*

- **Login Page**  
  `![Login Page](screenshots/login.png)`

- **Dashboard View**  
  `![Dashboard](screenshots/dashboard.png)`

## Deployment (Live Version)

The live version of this app is hosted on [Render.com](https://render.com).

- Backend runs on a Python web service using Gunicorn
- Environment variables securely configured
- PostgreSQL database hosted through Render’s integrated service
- Demo SQL data auto-seeded for convenience

To access the deployed version:
1. Visit the [Live Demo](https://your-render-url.onrender.com)
2. Use the provided credentials to log in
3. Explore functionality, including expense tracking, charting, and session-based login

> 📝 If the Render service is “spinning up” after inactivity, please allow a few seconds for the backend to fully start.

## License
This project is open-source under the [MIT License](LICENSE).

## Author
Developed by Jossell Araiza on July 10, 2025.
