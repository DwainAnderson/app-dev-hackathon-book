from flask import Flask, session
from src.sessions import process_session_params

app = Flask(__name__)
app.secret_key = 'z'  # Set a secret key for session security

# Initialize and open database
import sqlite3

def init_sqlite_db(db_filename, init_sql_filename):
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    with open(init_sql_filename, 'r') as f:
        sql = f.read()
        cursor.executescript(sql)
    conn.commit()
    return conn

db = init_sqlite_db("db/site.sqlite", "db/init.sql")

# Check login/logout params
session_messages = []
process_session_params(db, session_messages)


if __name__ == '__main__':
    app.run(debug=True)
