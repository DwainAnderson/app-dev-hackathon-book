import os
from flask import session, request, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
from init import app, db


# User Messages
session_messages = []
signup_messages = []

# Cookie duration expiration time in seconds
SESSION_COOKIE_DURATION = 60 * 60 * 1  # 1 hour

# Find user's record from user_id
def find_user(user_id):
    record = db.exec_sql_query("SELECT * FROM users WHERE id = ?;", (user_id,)).fetchone()
    return record


# Find user's record from session hash
def find_session(session_id):
    if not session_id:
        return None

    record = db.exec_sql_query("SELECT * FROM sessions WHERE session = ?;", (session_id,)).fetchone()
    return record


def current_user():
    return session.get('current_user')

# Did the user log in?
def is_user_logged_in():
    return current_user() is not None

# Login with username and password
def password_login(username, password):
    global current_user

    username = username.strip()
    password = password.strip()

    if not username or not password:
        session_messages.append("No username or password given.")
        return None

    record = db.exec_sql_query("SELECT * FROM users WHERE username = ?;", (username,)).fetchone()
    if not record:
        session_messages.append("Invalid username or password.")
        return None

    if not check_password_hash(record['password'], password):
        session_messages.append("Invalid username or password.")
        return None

    session_id = os.urandom(24).hex()
    result = db.exec_sql_query(
        "INSERT INTO sessions (user_id, session, last_login) VALUES (?, ?, ?);",
        (record['id'], session_id, datetime.now())
    )
    if not result:
        session_messages.append("Log in failed.")
        return None

    session['session'] = session_id
    session.permanent = True
    app.permanent_session_lifetime = timedelta(seconds=SESSION_COOKIE_DURATION)
    session['current_user'] = record

    return record

# Logout
def logout():
    if 'current_user' in session:
        session.pop('current_user')
    if 'session' in session:
        db.exec_sql_query("DELETE FROM sessions WHERE session = ?;", (session['session'],))
        session.pop('session')

    # Remove the session from the cookie and force it to expire (go back in time).
    response = redirect(url_for('index'))
    response.set_cookie('session', '', expires=0)
    return response

# Check for login, logout requests. Or check to keep the user logged in.
def process_session_params():
    # Is there a session? If so, find it!
    session_id = session.get('session')
    session = find_session(session_id)

    if 'logout' in request.args or 'logout' in request.form:  # Check if we should logout the user
        return logout()
    elif 'login' in request.form:  # Check if we should login the user
        return password_login(request.form['login_username'], request.form['login_password'])
    elif session:  # Check if logged in already via cookie
        current_datetime = datetime.now()
        login_expiration = session['last_login'] + timedelta(seconds=SESSION_COOKIE_DURATION)
        if login_expiration >= current_datetime:
            # session has not expired
            return find_user(session['user_id'])
        else:
            # session has expired
            logout()
            session_messages.append("Session expired. Please log in again.")
            return None


def create_account(name, username, password, password_confirmation):
    global signup_messages

    name = name.strip()
    username = username.strip()
    password = password.strip()
    password_confirmation = password_confirmation.strip()

    signup_messages = []  # Reset signup messages

    if not username:
        signup_messages.append("Please provide a username.")
    else:
        record = db.exec_sql_query("SELECT username FROM users WHERE username = ?;", (username,)).fetchone()
        if record:
            signup_messages.append("Username is already taken. Please pick another username.")

    if not password:
        signup_messages.append("Please provide a password.")

    if password != password_confirmation:
        signup_messages.append("Password confirmation doesn't match your password. Please reenter your password.")

    if not signup_messages:
        hashed_password = generate_password_hash(password)
        result = db.exec_sql_query(
            "INSERT INTO users (name, username, password) VALUES (?, ?, ?);",
            (name, username, hashed_password)
        )
        if result:
            return password_login(username, password)
        else:
            signup_messages.append("Account creation failed. Please try again.")
    return None
