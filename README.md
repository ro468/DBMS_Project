
# Tax Tracker Company

Tax Tracker Company is a web application built with Flask and SQLite for tracking and managing tax-related information for companies and customers.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)


## Introduction

Tax Tracker Company is designed to streamline the process of managing and tracking tax-related data for different companies and customers. The application allows employees to log in, view company information, and manage records. Customers can log in to view and interact with their specific information.

## Features

- Employee Login: Employees can log in using a password to access the employee dashboard.
- Customer Login: Customers can log in using their company category to access their specific information.
- New User Signup: New users can sign up to create a new record with the company and amount details.
- Company Information: Displays detailed information about a specific company, including payment status, due dates, and the ability to pay invoices.
- Edit Record: Allows users to edit existing records, including updating the amount and due date.
- Delete Record: Enables the deletion of records with a confirmation popup.

1. **db.py:**
   - Creates an SQLite database named 'my_database.db.'
   - Defines a table named 'my_table' with columns (id, category, amount, date_paid, status, due_date).
   - Inserts sample data into the table.

2. **app.py:**
   - Initializes a Flask web application.
   - Connects to the SQLite database.
   - Defines routes for home, employee login, customer login, new user signup, displaying company information, paying invoices, editing records, deleting records, saving records, and fetching summary.
   - Uses Flask templates (Jinja2) for rendering HTML pages.
   - Implements functions for database connection, closing, and rendering HTML pages.
   - Handles login authentication based on a fixed password for employees.
   - Displays a list of companies for employees.
   - Allows customers to log in, redirecting them to their respective company information.
   - Enables new user sign-up, inserting data into the database.
   - Displays and edits company information, deletes records, saves record changes, and fetches a summary table.

3. **HTML Templates:**
   - Templates are provided for various pages, such as 'company_info.html,' 'customer_dashboard.html,' 'customer_login.html,' 'edit_record.html,' 'employee_dashboard.html,' 'employee_login.html,' 'index.html,' 'new_user_signup.html,' and 'summary.html.'
   - These templates use Jinja2 templating to embed dynamic data and logic within HTML.

4. **JavaScript:**
   - Includes JavaScript functions in the templates for handling actions like editing records, confirming record deletions, and fetching summary data asynchronously.

5. **CSS Styling:**
   CSS styling is applied for front-end page aesthetics.


