from backend.init import app
from database.db import DatabaseDriver, init_sqlite_db
from sessions import *
from flask import Flask, g, request
import json


import sys

def is_in_virtual_environment():
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

if is_in_virtual_environment():
    print("Running in a virtual environment")
else:
    print("Not running in a virtual environment")


# Initialize database
db_connection = init_sqlite_db("db/site.sqlite", "db/init.sql")
db = DatabaseDriver(app.config['DATABASE'], app.config['INIT_SQL'])

# Check login/logout params
session_messages = []
process_session_params(db, session_messages)

# Connect to the database
def get_db():
    if 'db' not in g:
        g.db = db.conn
    return g.db

def success_response(body, code=200):
    """
    Success response function
    """
    return json.dumps(body), code

def failure_response(message, code=404):
    """
    Failure response function
    """
    error_message = {'error': message}
    return json.dumps(error_message), code

# Close database connection
@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# Routes - User Login/Logout Section -----------------
@app.route('/login', methods=['POST'])
def login():
    # Receive login data from request
    username = request.form.get('username')
    password = request.form.get('password')

    # Check if username and password are provided
    if not username or not password:
        return failure_response('Username or password not provided', 400)

    # Call password_login function from sessions.py to verify credentials
    response = password_login(username, password)

    # Check if login was successful
    if response:
        return success_response({'message': 'Login successful', 'user': response}, 200)
    else:
        return failure_response('Invalid username or password', 401)


@app.route('/logout', methods=['POST'])
def logout():
    response = logout()
    if response:
        return success_response({'message': 'Logout successful', 'user': response}, 200)
    else:
        return failure_response('Logout Error', 401)

@app.route('/create-account', methods=['POST'])
def create_user():
    # Receive login data from request
    username = request.form.get('username')
    name = request.form.get('name')
    password = request.form.get('password')
    password_confirmation = request.form.get('password-confirmation')
    user = create_account(name, username, password, password_confirmation)
    # Check if create account was successful
    if user:
        return success_response({'message': 'Login successful', 'user': user}, 200)
    else:
        return failure_response('Invalid username or password', 401)

def update_user():
    pass


# Routes - CRUD opps for books -----------------
@app.route('/favorite-book', methods=['POST'])
def favorite_book():
    pass

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6000, debug=True)
