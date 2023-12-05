from flask import Flask, render_template, request, g,redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Define the database name
DATABASE = 'my_database.db'  # Replace 'your_database_name' with the actual database name


# Function to connect to the database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


# Function to close the database connection
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# Define the route for the home page
@app.route('/')
def home():
    return render_template('index.html')


# Define the route for employee login
@app.route('/employee_login', methods=['GET', 'POST'])
def employee_login():
    if request.method == 'POST':
        password = request.form['password']

        # For simplicity, use a fixed password '123' for all employees
        if password == '123':
            # Fetch all companies from the database
            cursor = get_db().cursor()
            cursor.execute('SELECT DISTINCT category FROM my_table')
            companies = cursor.fetchall()
            return render_template('employee_dashboard.html', companies=companies)
        else:
            return "Invalid password. Please try again."

    return render_template('employee_login.html')  # Display the login form for GET requests



# Define the route for customer login

@app.route('/customer_login', methods=['GET', 'POST'])
def customer_login():
    if request.method == 'POST':
        customer_category = request.form['customer_category']

        # Fetch customer information from the database
        cursor = get_db().cursor()
        cursor.execute('SELECT category FROM my_table WHERE category = ?', (customer_category,))
        category = cursor.fetchone()

        if category:
            # Redirect to the appropriate category route
            return redirect(f'/company_info/{category[0]}')
        else:
            return "Customer not found. Please check the category and try again."

    return render_template('customer_login.html')  # Display the login form for GET requests


# Define the route for new user signup
@app.route('/new_user_signup', methods=['GET', 'POST'])
def new_user_signup():
    if request.method == 'POST':
        # Generate a unique consecutive ID (assuming it's the next available ID in the database)
        cursor = get_db().cursor()
        cursor.execute('SELECT MAX(id) FROM my_table')
        last_id = cursor.fetchone()[0]
        new_id = last_id + 1 if last_id is not None else 1

        # Get other form data
        company = request.form['company']
        amount = request.form['amount']

        # Pass the current year to the template
        current_year = datetime.now().year

        # Insert new user data into the database
        cursor.execute('INSERT INTO my_table VALUES (?, ?, ?, ?, ?, ?)',
                       (new_id, company, amount, None, 'unpaid', f'{current_year}-01-15'))

        # Commit the changes to the database
        get_db().commit()

        return f"New user with ID {new_id} successfully created!", 200, {'Content-Type': 'text/plain'}

    return render_template('new_user_signup.html', current_year=datetime.now().year)

@app.route('/company_info/<company>')
def company_info(company):
    print("Company:", company)  # Add this line for debugging
    # Fetch company information from the database
    cursor = get_db().cursor()
    cursor.execute('SELECT * FROM my_table WHERE category = ?', (company,))
    company_info = cursor.fetchall()
    print("Company Info:", company_info)  # Add this line for debugging
    return render_template('company_info.html', company_info=company_info, company=company)


# Define the route for paying the invoice
@app.route('/pay_here', methods=['POST'])
def pay_here():
    payment_id = request.form['payment_id']

    # Update the payment status in the database
    cursor = get_db().cursor()
    cursor.execute('UPDATE my_table SET status = "paid" WHERE id = ?', (payment_id,))
    get_db().commit()

    return "You've successfully paid. Thanks for being an amazing Taxpayer!"


# Edit record
@app.route('/edit_record/<record_id>', methods=['GET', 'POST'])
def edit_record(record_id):
    success_message = None
    if request.method == 'POST':
        new_amount = request.form['new_amount']
        due_date_str = request.form['due_date']
        month, day = due_date_str.split()
        month_number = datetime.strptime(month, '%B').month
        current_year = datetime.now().year
        next_year = current_year + 1
        due_date = datetime(next_year, month_number, int(day))

        cursor = get_db().cursor()
        cursor.execute('UPDATE my_table SET amount = ?, due_date = ? WHERE id = ?',
                       (new_amount, due_date, record_id))
        get_db().commit()
        success_message = 'Changes successfully submitted!'

        # Fetch the company category for the edited record
        cursor.execute('SELECT category FROM my_table WHERE id = ?', (record_id,))
        category = cursor.fetchone()[0]

        return redirect(f'/company_info/{category}?success_message={success_message}')

    cursor = get_db().cursor()
    cursor.execute('SELECT * FROM my_table WHERE id = ?', (record_id,))
    record = cursor.fetchone()
    return render_template('edit_record.html', record=record, success_message=success_message)


# Delete record
@app.route('/delete_record/<record_id>')
def delete_record(record_id):
    cursor = get_db().cursor()
    cursor.execute('DELETE FROM my_table WHERE id = ?', (record_id,))
    get_db().commit()
    return redirect('/')

# Save record
@app.route('/save_record', methods=['POST'])
def save_record():
    record_id = request.form['record_id']
    new_amount = request.form['new_amount']
    cursor = get_db().cursor()
    cursor.execute('UPDATE my_table SET amount = ? WHERE id = ?', (new_amount, record_id))
    get_db().commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
